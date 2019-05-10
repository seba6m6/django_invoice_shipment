from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Invoice, InvoiceItem
from .models import InvoiceItemToShip, Shipment
import datetime
from django.db.models import Q
from django.forms.widgets import CheckboxSelectMultiple



class InvoiceForm(forms.ModelForm):
    invoice_no =forms.CharField(widget=forms.TextInput(attrs={'size':40}),initial='Proforma Invoice 2019102300001')
    date = forms.DateField(widget = forms.SelectDateWidget,initial=datetime.date.today)
    class Meta:
        model = Invoice
        exclude = ('total','total_eur')

# class InvoiceItemShipToShipForm(forms.ModelForm):
#     invoice_item = forms.ModelChoiceField(queryset=)
#
#     class Meta:
#         model = InvoiceItemToShip
#         fields = ('invoice_item','quantity')


class ShipmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today)
    class Meta:
        model=Shipment
        exclude = ('total', 'total_eur')

class InvoiceItemToShipForm(forms.ModelForm):
    invoice_item = forms.ModelChoiceField(queryset=InvoiceItem.objects.all().filter(
        Q(invoice__paid=True)|
        Q(invoice__partially_paid=True),
        ).filter(sent=False))

    class Meta:
        model=InvoiceItemToShip
        exclude = ()

class InvoiceItemToShipUpdateForm(forms.ModelForm):
    invoice_item = forms.ModelChoiceField(queryset=InvoiceItem.objects.all())

    class Meta:
        model=InvoiceItemToShip
        exclude = ()


InvoiceInvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, extra=50, exclude=(), can_delete=True,widgets={
        'quantity_left': forms.HiddenInput(),
        'sent': forms.HiddenInput()}
)

ShipmentFormset = inlineformset_factory(
    Shipment, InvoiceItemToShip, extra=40, can_delete=True,
    form=InvoiceItemToShipForm
)


UpdateShipmentFormset = inlineformset_factory(
    Shipment, InvoiceItemToShip, extra=40, can_delete=True,
    form=InvoiceItemToShipUpdateForm
)
