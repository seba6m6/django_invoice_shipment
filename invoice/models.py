from django.db import models
import datetime
from django.urls import reverse
from photo.models import Product

# Create your models here.

class Invoice(models.Model):
    invoice_no        = models.CharField(max_length=40, default="Proforma Invoice 2019102300001")
    commercial        = models.BooleanField(blank=True, null=True, default=False)
    title             = models.CharField(max_length=60, blank=True, null=True)
    total             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_eur         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    date              = models.DateField(auto_now_add=False,auto_now=False,default=datetime.date.today)
    paid              = models.BooleanField(blank=True, null=True, default=False)
    partially_paid    = models.BooleanField(blank=True, null=True, default=False)
    remarks           = models.CharField(max_length=400, blank=True, null=True)
    batch             = models.BooleanField(blank=True, null=True, default=False)
    proof             = models.FileField(blank=True, null=True)
    proof_date        = models.DateField(auto_now_add=False,auto_now=False,default=datetime.date.today,blank=True, null=True)
    proof_partial     = models.FileField(blank=True, null=True)
    proof_partial_date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.date.today, blank=True, null=True)

    def __str__(self):
        return self.invoice_no

    def get_absolute_url(self):
        return reverse('invoice_detail',kwargs = {'pk':self.pk})

class InvoiceItem(models.Model):
    product          = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,)
    invoice          = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    quantity         = models.DecimalField(max_digits=5, decimal_places=0)
    quantity_left    = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    sent             = models.BooleanField(default=False, blank=True, null=True)
    items_total      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    items_total_eur  = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    def __str__(self):
        if self.product.product_name_chinese:
            return self.product.product_name +" "+ str(self.product.ERP_number) + " " + self.invoice.invoice_no
        else:
            return self.product.product_name

    class Meta:
        ordering = ['product']

class Shipment(models.Model):
    date         = models.DateField()
    shipping_no  = models.CharField(max_length=60, blank=True, null=True)
    shipping_pdf = models.FileField(blank=True, null=True,verbose_name='电子运单')
    invoice      = models.FileField(blank=True, null=True,verbose_name='发票')
    packing      = models.FileField(blank=True, null=True,verbose_name='包装单')
    box          = models.IntegerField(blank=True, null=True)
    total        = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_eur    = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.shipping_no

class InvoiceItemToShip(models.Model):
    invoice_item    = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE, null=True,blank=True)
    shipment        = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True)
    quantity        = models.DecimalField(max_digits=5, decimal_places=0)
    total           = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_eur       = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.invoice_item.product.product_name









