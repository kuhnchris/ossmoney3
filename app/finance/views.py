from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Ledger, InvoiceHead, LedgerTypes, LedgerClosingTypes


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
