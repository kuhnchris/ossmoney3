from dal import autocomplete
from .models import Vendor, InvoicePosition, InvoiceHead
from django import forms


class InvoiceHeadForm(forms.Form):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.all(),
        widget=autocomplete.ModelSelect2(url='vendor-autocomplete')
    )
    notes = forms.CharField(label="Notes")
    image = forms.ImageField(label="Scan")
    useOCR = forms.BooleanField(label="Do you want to try to OCR the invoice?")


class InvoiceLineForm(forms.Form):
    class Meta:
        model = InvoicePosition


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = InvoiceHead
        exclude = [ ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        posLines = InvoicePosition.objects.filter(
            head=self.instance
        )
        for i in range(len(posLines) + 1):
            field_name = 'posLines_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = posLines[i].position
            except IndexError:
                self.initial[field_name] = ''
                field_name = 'posLines_%s' % (i + 1,)
                self.fields[field_name] = forms.CharField(required=False)
        for field_name in self.fields:
            self.fields[field_name].required = False;

    def clean(self):
        posLines = set()
        i = 0
        field_name = 'posLines_%s' % (i,)
        while self.cleaned_data.get(field_name):
            posLine = self.cleaned_data[field_name]
            if posLine in posLines:
                self.add_error(field_name, 'Duplicate')
            else:
                posLines.add(posLine)
            i += 1
            field_name = 'posLines_%s' % (i,)

        self.cleaned_data["posLines"] = posLines

    def save(self, commit=True):
        super().save(self)
        head = self.instance
        head.vendor = self.cleaned_data["vendor"]

        head.positions.all().delete()
        for posLine in self.cleaned_data["posLines"]:
            InvoicePosition.objects.create(
                head=head,
                position=posLine,
            )

    def get_interest_fields(self):
        for field_name in self.fields:
            if field_name.startswith('posLines_'):
                yield self[field_name]
