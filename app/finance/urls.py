from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ledger/<int:ledger_id>/', views.ledgerView, name='ledger'),
    path('invoice/<int:invoice_id>/', views.invoiceView, name='invoice'),
    path('invoices/', views.invoiceOverview, name='invoiceOverview')

]
