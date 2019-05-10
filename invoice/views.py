from rest_framework import status
from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from invoice.serializers import InvoiceSerializer
from django.views.generic import View, CreateView, DetailView, UpdateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import InvoiceForm, InvoiceInvoiceItemFormset
from .forms import ShipmentForm, ShipmentFormset, UpdateShipmentFormset
from .models import Invoice, InvoiceItem
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.db.models import Sum, F, Q
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib import messages

# Create your views here.

class CreateInvoice(CreateView):
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse('photo:main')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['invoiceitems'] = InvoiceInvoiceItemFormset(self.request.POST, self.request.FILES)
        else :
            data['invoiceitems'] = InvoiceInvoiceItemFormset()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        invoiceitems = context['invoiceitems']

        with transaction.atomic():
            self.object = form.save()
            if invoiceitems.is_valid():
                invoiceitems.instance = self.object
                invoiceitems.save()
                for i in self.object.invoiceitem_set.all():
                    i.items_total = i.quantity * i.product.price_pol
                    i.quantity_left = i.quantity
                    try:
                        i.items_total_eur = i.quantity * i.product.price_pol_eur
                    except:
                        i.items_total_eur= None
                    i.save()
                self.object.total = self.object.invoiceitem_set.aggregate(
                    total = Sum(F('product__price_pol')*F('quantity')))['total']
                try:
                    self.object.total_eur = self.object.invoiceitem_set.aggregate(
                        total = Sum(F('product__price_pol_eur')*F('quantity')))['total']
                except:
                    self.object.total_eur = None
        return super().form_valid(form)


class UpdateInvoice(CreateInvoice, UpdateView):
    model = Invoice
    form_class = InvoiceForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['invoiceitems'] = InvoiceInvoiceItemFormset(self.request.POST, self.request.FILES, instance=self.object)
        else :
            data['invoiceitems'] = InvoiceInvoiceItemFormset(instance=self.object)
        return data

class ShipmentView(CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'invoice/shipment_form.html'

    def get_success_url(self):
        return reverse('photo:main')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['invoiceitemstoship'] = ShipmentFormset(self.request.POST, self.request.FILES)
        else:
            data['invoiceitemstoship'] = ShipmentFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        invoiceitemstoship = context['invoiceitemstoship']


        try:

            with transaction.atomic():
                self.object = form.save()
                if invoiceitemstoship.is_valid():

                    invoiceitemstoship.instance = self.object
                    invoiceitemstoship.save()

                    for i in self.object.invoiceitemtoship_set.all():
                        i.total = i.quantity * i.invoice_item.product.price_pol
                        if i.invoice_item.product.price_pol_eur:
                            i.total_eur = i.quantity * i.invoice_item.product.price_pol_eur
                        quantity_left = i.invoice_item.quantity_left - i.quantity
                        if quantity_left < 0 :
                            raise ValueError()
                        i.invoice_item.quantity_left = i.invoice_item.quantity_left - i.quantity
                        if i.invoice_item.quantity_left == 0 :
                            i.invoice_item.sent = True
                        # i.invoice_item.save()
                        # invoiceitemstoship.save()
                        i.save()
                    self.object.total = self.object.invoiceitemtoship_set.aggregate(
                        total=Sum(F('invoice_item__product__price_pol') * F('quantity')))['total']
                    self.object.total_eur = self.object.invoiceitemtoship_set.aggregate(
                        total=Sum(F('invoice_item__product__price_pol_eur') * F('quantity')))['total']
                    return super().form_valid(form)
        except ValueError:
            messages.add_message(self.request, messages.INFO, '可发货的数量没这么多 ！！！')
            return redirect('ship_items')

class ShipmentUpdate(ShipmentView,UpdateView):
    #TODO def form_valid in update should not count quantity_left once again
    model = Shipment
    form_class = ShipmentForm
    template_name = 'invoice/shipment_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['invoiceitemstoship'] = UpdateShipmentFormset(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data['invoiceitemstoship'] = UpdateShipmentFormset(instance=self.object)
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        invoiceitemstoship = context['invoiceitemstoship']
        try:

            with transaction.atomic():
                self.object = form.save()
                if invoiceitemstoship.is_valid():

                    invoiceitemstoship.instance = self.object
                    invoiceitemstoship.save()

                    for i in self.object.invoiceitemtoship_set.all():
                            i.total = i.quantity * i.invoice_item.product.price_pol
                            if i.invoice_item.product.price_pol_eur:
                                i.total_eur = i.quantity * i.invoice_item.product.price_pol_eur
                            i.save()


                    self.object.total = self.object.invoiceitemtoship_set.aggregate(
                        total=Sum(F('invoice_item__product__price_pol') * F('quantity')))['total']
                    self.object.total_eur = self.object.invoiceitemtoship_set.aggregate(
                        total=Sum(F('invoice_item__product__price_pol_eur') * F('quantity')))['total']
                    return super(UpdateView, self).form_valid(form)
        except ValueError:
            messages.add_message(self.request, messages.INFO, '错误')
            return redirect('ship_items')

class ShipmentSimpleUpdate(UpdateView):
    model      = Shipment
    form_class = ShipmentForm

    def get_success_url(self):
        return reverse('photo:main')

class InvoiceList(View):
    unpaid = None
    batch = False
    partially_paid = False
    sent = False
    def get (self, request):
        if self.sent:
            object_list = Invoice.objects.all().order_by('-date').filter(sent=self.sent)
        elif self.partially_paid:
            object_list = Invoice.objects.all().order_by('-date').filter(partially_paid=True)
        elif self.unpaid:
            object_list = Invoice.objects.all().order_by('-date').filter(paid=False, partially_paid=False)
        elif self.batch:
            object_list = Invoice.objects.all().order_by('-date').filter(batch=True)
        else:
            object_list = Invoice.objects.all().order_by('-date')
        query = request.GET.get('q')
        if query:
            object_list = object_list.filter(
                Q(invoice_no__icontains=query)|
                Q(date__icontains=query)|
                Q(total__icontains=query)|
                Q(title__icontains=query)|
                Q(invoiceitem__product__product_name__icontains=query)
            ).distinct()
        paginator = Paginator(object_list, 25)
        page = request.GET.get('page')
        objects = paginator.get_page(page)

        return render(request, 'invoice/invoice_list.html', {'invoices':objects})

class PartiallyPaidInvoice(InvoiceList):
    partially_paid = True

class UnpaidInvoice(InvoiceList):
    unpaid = True

class BatchInvoice(InvoiceList):
    batch = True


@api_view(['GET', 'POST'])
def invoice_list_api(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InvoiceSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def invoice_detail(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    template_name = 'invoice/invoice.html'
    return render(request, template_name, {'invoice':invoice})

def generate_pdf(request, pk):
    invoice_object = Invoice.objects.get(pk=pk)
    invoice = {
        "date": invoice_object.date,
        "number": invoice_object.invoice_no,
        "total": invoice_object.total,
        "total_eur": invoice_object.total_eur,
        "title": invoice_object.title,
        "items":invoice_object.invoiceitem_set.all(),
        "commercial":invoice_object.commercial,
    }
    html_string = render_to_string('invoice/invoice_pdf.html',invoice)

    html = HTML(string=html_string)
    html.write_pdf(target = settings.ROOT + 'invoice.pdf')

    fs = FileSystemStorage(settings.ROOT)
    with fs.open('invoice.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' %invoice_object.invoice_no
        return response
def generate_shipment_pdf(request, pk):
    shipment_object = Shipment.objects.get(pk=pk)
    shipment = {
        "date": shipment_object.date,
        "number": shipment_object.shipping_no,
        "total": shipment_object.total,
        "total_eur": shipment_object.total_eur,
        "items":shipment_object.invoiceitemtoship_set.all(),

    }
    html_string = render_to_string('invoice/shipping_list_pdf.html',shipment)

    html = HTML(string=html_string)
    html.write_pdf(target = settings.ROOT + 'shipment.pdf')

    fs = FileSystemStorage(settings.ROOT)
    with fs.open('shipment.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' %shipment_object.shipping_no
        return response

def shipment_detail(request, pk):
    shipment = Shipment.objects.get(pk=pk)
    template_name = 'invoice/shipping_list.html'
    return render(request, template_name, {'shipment':shipment})

def shipment_lists(request):
    object_list = Shipment.objects.all().order_by('-date')

    query = request.GET.get('q')
    if query:
        object_list = object_list.filter(
            Q(shipping_no__icontains=query) |
            Q(date__icontains=query) |
            Q(total__icontains=query) |
            Q(total_eur__icontains=query) |
            Q(invoiceitemtoship__invoice_item__product__product_name__icontains=query)
        ).distinct()
    paginator = Paginator(object_list,3)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    template_name = 'invoice/shipping_lists.html'
    return render(request, template_name, {'shipments':objects})



@api_view(['GET'])
def invoice_detail_api(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)

    except invoice.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvoiceSerializer(invoices)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InvoiceSerializer(status, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class ItemsToSendList(View):
    paid = True
    sent = False

    def get(self, request):
        object_list = InvoiceItem.objects.all().order_by('-invoice__date').filter(Q(invoice__paid=self.paid) |
        Q(invoice__partially_paid=True),
        ).filter(sent=self.sent)
        query = request.GET.get('q')
        if query:
            object_list = object_list.filter(
                Q(product__product_name__icontains=query) |
                Q(invoice__invoice_no__icontains=query) |
                Q(invoiceitemtoship__shipment__shipping_no__icontains=query)
            ).distinct()
        paginator = Paginator(object_list, 25)
        page = request.GET.get('page')
        objects = paginator.get_page(page)

        return render(request, 'invoice/itemstosend.html', {'objects':objects, 'sent':self.sent})


class ItemsSent(ItemsToSendList):
    paid=True
    sent=True

