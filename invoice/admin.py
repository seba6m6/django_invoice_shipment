from django.contrib import admin
from .models import Invoice,InvoiceItem,Shipment, InvoiceItemToShip
# Register your models here.

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Shipment)
admin.site.register(InvoiceItemToShip)