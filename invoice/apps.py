from django.apps import AppConfig
from django.contrib import admin
from invoice.models import *
class InvoiceConfig(AppConfig):
    name = 'invoice'

admin.site.register(Product, Invoice, Batch)