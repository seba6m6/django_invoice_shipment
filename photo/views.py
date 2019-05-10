# coding=utf-8
from django.views import generic
from .models import Photo, ShipPhoto, Product
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from datetime import datetime, timedelta
from .forms import UserForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PhotoForm, ShipPhotoForm, ProductForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ShipPhotoSerializer



# API REQUESTS

class ShipPhotoAPI(APIView):

    def get(self):
        pass
    def post(self):
        pass

###########################################################################################

@login_required
def newphotoview(request):
    object_list = Photo.objects.all().order_by('-date')
    query = request.GET.get('q')
    if query:
        object_list = object_list.filter(
            Q(名称photo_name__icontains=query)|
            Q(date__icontains=query)
            ).distinct()
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return render(request, 'photos.html', {'objects': objects})


class PhotoView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'photos.html'

    def get_queryset(self):
        return Photo.objects.all().order_by('-date')




@login_required
def newshipphotoview(request):
    object_list = ShipPhoto.objects.all().order_by('-update')
    query = request.GET.get('q')
    if query:
        object_list = object_list.filter(
            Q(订单order__icontains=query)|
            Q(运单号tracking__icontains=query)|
            Q(date__icontains=query)
            ).distinct()
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return render(request, 'ship_photos.html', {'objects': objects})


def productview(request):
    object_list = Product.objects.all().order_by('-date')
    query = request.GET.get('q')
    if query:
        object_list = object_list.filter(
            Q(product_name__icontains=query)|
            Q(date__icontains=query)|
            Q(used_in__icontains=query)|
            Q(category__icontains=query)|
            Q(ERP_number__icontains=query)
            ).distinct()
    object_list =list(enumerate(object_list, 1))
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return render(request, 'products_list.html', {'objects': objects, 'object_list':object_list})

class ProductDetailView(LoginRequiredMixin, generic.DetailView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Product
    template_name = 'product_detail.html'

class ProductCreate(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    form_class = ProductForm
    template_name = 'photo/product_form.html'

    def get(self, request):
        form =self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():  # uploader has been excluded. No more error.
            photo = form.save(commit=False)  # returns unsaved instance
            photo.user_name = request.user
            photo.save()  # real save to DB.
            return redirect('photo:main')
        return render(request,self.template_name,{})

class ProductUpdate(LoginRequiredMixin, UpdateView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Product
    fields = ['photo', 'category', 'product_name','product_name_chinese','ERP_number', 'link', 'specification','translated_spec','original_quote','price','price_pol','price_pol_eur','moq','used_in']

class ShipPhotoView(LoginRequiredMixin, generic.ListView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'ship_photos.html'

    def get_queryset(self):
        return ShipPhoto.objects.all().order_by('-date')

class PhotoDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Photo
    template_name = 'photo_detail.html'

class ShipPhotoDetailView(LoginRequiredMixin, generic.DetailView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = ShipPhoto
    template_name = 'ship_photo_detail.html'

@login_required
def main( request):

    startdate = datetime.today()
    enddate = startdate + timedelta(-2)
    photo = Photo.objects.all().order_by('-date')
    recent_photos = photo.filter(date__range=[enddate, startdate])
    return render(request, 'main.html', {'recent_photos':recent_photos})

class PhotoCreate(LoginRequiredMixin, CreateView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Photo
    fields = ['photo', '名称photo_name', '数量quantity', '状态condition', '地方place','user_name']

#NEW CREATE PHOTO FOR TESTS

class PhotoCreateNew(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    form_class = PhotoForm
    template_name = 'photo/photo_form.html'

    def get(self, request):
        form =self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():  # uploader has been excluded. No more error.
            photo = form.save(commit=False)  # returns unsaved instance
            photo.user_name = request.user
            photo.save()  # real save to DB.
            return redirect('photo:main')
        return render(request,self.template_name,{})

class ShipPhotoCreate(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    form_class = ShipPhotoForm
    template_name = 'photo/shipphoto_form.html'

    def get(self, request):
        form =self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        # print(form)
        if form.is_valid():  # uploader has been excluded. No more error.

            try:
                photo = form.save(commit=False)  # returns unsaved instance

                # print(form['step'])
                photo.user_name = request.user

                photo.save()  # real save to DB.
                #### Sending an object with shipphoto data to WorkWechat API##########################################################
                wechat_message = {
                    "touser": "seba6m6|QuanDongMei|marcin|1280|1288|1014|3224014172@qq.com",
                    "toparty": "PartyID1 | PartyID2",
                    "totag": "TagID1 | TagID2",
                    "msgtype": "news",
                    "agentid": 1000024,
                    "news": {
                        "articles": [
                            {
                                "title": '订单 ：' + str(photo.订单order) + "",
                                "description": "货柜已发 - Kontener wysłany",
                                "url": "https://zortrax.pythonanywhere.com/ship-photo/" + str(photo.pk) + '/',
                                "picurl":"https://zortrax.pythonanywhere.com"+ str(photo.照片photo.url) +''
                            }
                        ]
                    }
                }
                access_data = requests.get(
                    'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ww672289f9f183ad10&corpsecret=cN2J3Xvm5YzVqj1T5LU2DOSn43z8u_96HNo4RHIpPXI').json()
                access_token = access_data['access_token']
                requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token + '',
                              json=wechat_message)
            except:
                print(photo)
                print("Nie udalo sie wrzucic tej wysylki !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            ############################################################################################################
            return redirect('photo:main')
        return render(request,self.template_name,{})


class PhotoUpdate(LoginRequiredMixin, UpdateView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Photo
    fields = ['照片photo', '名称photo_name', '数量quantity', '状态condition', '地方place']

class ShipPhotoUpdate(LoginRequiredMixin, UpdateView):

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = ShipPhoto
    fields = ['照片photo','车牌carplates','发货名细xlsx','运单号tracking','发票invoice','发货成本transcosts','数量quantity','订单order']

# class ShipPhotoUpdate(UpdateView):
#     model = Photo
#     fields = '__all__'

class PhotoDelete(DeleteView):
    model = Photo
    success_url = reverse_lazy("photo:main")

class ShipPhotoDelete(DeleteView):
    model = ShipPhoto
    success_url = reverse_lazy("photo:ship_photos")

    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user. """
    #     obj = super(PhotoDelete, self).get_object()
    #     if not obj.user_name == self.request.user:
    #         raise Http404
    #     return obj

class UserFormView(View):
    form_class = UserForm
    template_name = 'accounts/registration_form.html'

    def get(self, request):
        form =self.form_class(None)
        return render(request, self.template_name, {'form':form})
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user= form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if username is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('photo:main')
        return render(request, self.template_name, {'form':form})


