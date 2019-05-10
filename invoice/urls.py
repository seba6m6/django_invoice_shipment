from django.urls import path, re_path
from . import views

urlpatterns = [
    path('invoice-list-api/', views.invoice_list_api ),
    path('invoice-list/', views.InvoiceList.as_view(), name='invoice_list' ),
    path('invoice-list-unpaid/', views.UnpaidInvoice.as_view(), name='unpaid_invoice_list' ),
    path('invoice-list-partially-paid/', views.PartiallyPaidInvoice.as_view(), name='partially_paid_invoice_list' ),
    path('invoice-list-batch/', views.BatchInvoice.as_view(), name='batch_invoice_list' ),
    re_path(r'^invoice/(?P<pk>[0-9]+)/$', views.invoice_detail, name='invoice_detail' ),
    re_path(r'^invoice-pdf/(?P<pk>[0-9]+)/$', views.generate_pdf, name='generate_pdf'),
    re_path(r'^shipments-list-pdf/(?P<pk>[0-9]+)/$', views.generate_shipment_pdf, name='generate_shipment_pdf'),
    path('invoice-create/', views.CreateInvoice.as_view(), name='create_invoice'),
    re_path(r'^invoice-update/(?P<pk>[0-9]+)/$', views.UpdateInvoice.as_view(), name='update_invoice'),
    path('invoice-items-ship/', views.ShipmentView.as_view(), name='ship_items'),
    re_path(r'^invoice-items-ship-update/(?P<pk>[0-9]+)/$', views.ShipmentUpdate.as_view(), name='ship_items_update'),
    re_path(r'^invoice-items-ship-simple-update/(?P<pk>[0-9]+)/$', views.ShipmentSimpleUpdate.as_view(), name='ship_items_simple_update'),
    path('invoice-items-to-ship/', views.ItemsToSendList.as_view(), name='items_to_send'),
    path('invoice-items-sent/', views.ItemsSent.as_view(), name='items_sent'),
    path('shipments-list/', views.shipment_lists, name='shipment_lists'),
    re_path(r'^shipment-detail/(?P<pk>[0-9]+)/$', views.shipment_detail, name='shipment_detail'),

]