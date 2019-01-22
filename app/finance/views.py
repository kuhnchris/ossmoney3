from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from .models import Ledger, InvoiceHead, LedgerTypes, LedgerClosingTypes, Vendor
from .forms import InvoiceForm, InvoiceLineForm
from dal import autocomplete


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def templateViewReturn(request, templateUrl, templateContext):
    ledgers = Ledger.objects.order_by('id')
    context = templateContext
    context['ledgers'] = ledgers
    return render(request, templateUrl, context)

def invoiceNew(request):
    selectedInvoice_balance = 0
    return templateViewReturn(request,
                              'finance/invoiceDetail.html',
                              {'editmode': True
                              })

def invoiceView(request, invoice_id):
    selectedInvoice = InvoiceHead.objects.get(pk=invoice_id)
    selectedInvoice_balance = 0
    for itm in selectedInvoice.positions.all():
        selectedInvoice_balance = selectedInvoice_balance + itm.per_amount_price
    return templateViewReturn(request,
                              'finance/invoiceDetail.html',
                              {'selectedInvoice':selectedInvoice,
                               'selectedInvoice_balance':selectedInvoice_balance
                              })

def invoiceOverview(request):
    invoices = InvoiceHead.objects.order_by('id')
    return templateViewReturn(request,
                              'finance/invoiceOverview.html',
                              {'invoices': invoices})



def ledgerView(request, ledger_id):
    selectedLedger = Ledger.objects.get(pk=ledger_id)
    selectedLedger_balance = 0
    selectedLedger_ledgerType = LedgerTypes.__dict__[selectedLedger.ledger_type].value
    for itm in selectedLedger.invoiceItems.all():
        selectedLedger_balance = selectedLedger_balance + itm.per_amount_price


    if not selectedLedger:
        return Http404.message('Invalid ledger ID')
    return templateViewReturn(request,
                              'finance/ledgerOverview.html',
                              {'selectedLedger': selectedLedger,
                               'selectedLedger_balance': selectedLedger_balance,
                               'selectedLedger_ledgerType': selectedLedger_ledgerType
                               })

def renderInvHeaderAddView(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InvoiceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/invoices/')

    else:
        # form = InvoiceHeadForm()
        form = InvoiceForm()
        invLines = [InvoiceLineForm()]
    return render(request, 'finance/forms/newInvoiceHeadForm.html', {'form': form, 'invLines': invLines})


class VendorAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Vendor.objects.none()

        qs = Vendor.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs