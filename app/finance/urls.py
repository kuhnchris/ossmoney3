from django.urls import path

from . import views
from .views import VendorAutoComplete

urlpatterns = [
    path('', views.index, name='index'),
    path('ledger/<int:ledger_id>/', views.ledgerView, name='ledger'),
    path('invoice/<int:invoice_id>/', views.invoiceView, name='invoice'),
    path('invoices/', views.invoiceOverview, name='invoiceOverview'),
    path('invoices/new', views.invoiceNew, name='invoiceNew'),
    path('invoices/add2', views.renderInvHeaderAddView, name='invoiceAdd2'),
    path('autocomplete/vendor', VendorAutoComplete.as_view(create_field='short_name'), name="vendor-autocomplete")
]
