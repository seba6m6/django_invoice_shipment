from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from photo.forms import User
from django.contrib import admin
from django.forms import ModelForm
from PIL import Image

# from webcam.fields import CameraField
# from webcam.fields import CameraField


# Create your models here.
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=40)
    province = models.CharField(max_length=20)

    def __str__(self):
        return self.supplier_name
    def get_absolute_url(self):
        return reverse('photo:supplier_detail',kwargs={'pk':self.pk})

# def suppliers_choices():
#     return Supplier.objects['supplier_name']

class Photo(models.Model):
    user_name =  models.ForeignKey(User, on_delete=models.CASCADE)
    PLACES = (('RD','研发-R&D'),('Warehouse','仓库-Warehouse'),('Gate','门卫处-Gate Guard'),('SecondFloor','2F生产部'))
    照片photo = models.ImageField()
    # photo = CameraImageField(aspect_ratio=Fraction(16, 9))
    # photo = CameraField('CameraPictureField', format='jpeg', null=True, blank=True)
    名称photo_name = models.CharField(max_length=20)
    date = models.DateField(auto_now="True")
    # quantity = models.DecimalField(max_digits=4,decimal_places=0)
    数量quantity = models.DecimalField(max_digits=4,decimal_places=0)
    # CONDITIONS = (('NG','NG'), ('GOOD', 'GOOD'))

    CONDITIONS = (('NG','不良NG'), ('GOOD', '良GOOD'))
    状态condition=models.CharField(max_length=10,choices=CONDITIONS)
    地方place = models.CharField(max_length=30,choices=PLACES,default='Warehouse')

    def __str__(self):
        return self.名称photo_name
    def get_absolute_url(self):
        return reverse('photo:photo_detail', kwargs={'pk':self.pk})
    def save(self, **kwargs):
        super(Photo, self).save()
        image = Image.open(self.照片photo)
        size = (600,500)
        # size = ( width / factor, height / factor)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.照片photo.path)



class ShipPhoto(models.Model):
    user_name      = models.ForeignKey(User, on_delete=models.CASCADE)
    照片photo      = models.ImageField(blank=True, null=True)
    车牌carplates  = models.CharField(max_length=20, blank=True, null=True)
    运单号tracking = models.CharField(max_length=20,blank=True, null=True)
    发货名细xlsx   = models.FileField(blank=True, null=True)
    发票invoice    = models.FileField(blank=True, null=True)
    发货成本transcosts = models.FileField(blank=True, null=True)
    date           = models.DateField(auto_now_add="True")
    update         = models.DateTimeField(auto_now="True")
    数量quantity   = models.DecimalField(max_digits=4,decimal_places=0,blank=True, null=True)
    订单order      = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        return self.订单order
    def get_absolute_url(self):
        return reverse('photo:ship_photo_detail', kwargs={'pk':self.pk})


    def save(self, **kwargs):
        super(ShipPhoto, self).save()
        mywidth = 440
        image = Image.open(self.照片photo)
        wpercent = (mywidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((mywidth, hsize), Image.ANTIALIAS)
        image.save(self.照片photo.path)

class Product(models.Model):
    photo                = models.ImageField(blank=True, null=True)
    CATEGORIES = (('Electronics','Electronics电子 '),('CNC','CNC'),('其他Others','Others其他'),('完成品 Products','完成品 Products'))
    category             = models.CharField(max_length=30,choices=CATEGORIES,default='Electronics')
    product_name         = models.CharField(max_length=100)
    product_name_chinese = models.CharField(max_length=100, blank=True, null=True)
    ERP_number           = models.CharField(max_length=20, blank=True, null=True )
    link                 = models.CharField(max_length=200, blank=True, null=True)
    specification        = models.FileField(blank=True, null=True)
    translated_spec      = models.FileField(blank=True, null=True)
    original_quote       = models.FileField(verbose_name="Quotation China",blank=True, null=True)
    price                = models.DecimalField(verbose_name="price in RMB (costs)", max_digits=10,decimal_places=3, blank=True, null=True)
    price_pol            = models.DecimalField(verbose_name="price in USD", max_digits=10,decimal_places=3, blank=True, null=True)
    price_pol_eur        = models.DecimalField(verbose_name="price in EUR", max_digits=10, decimal_places=3, blank=True, null=True)
    moq                  = models.DecimalField(verbose_name="MOQ", max_digits=10,decimal_places=0, blank=True, null=True)
    used_in              = models.CharField(max_length=60, blank=True, null=True)
    date                 = models.DateField(auto_now_add="True")
    update               = models.DateTimeField(auto_now="True")

    def __str__(self):
        return self.product_name
    def get_absolute_url(self):
        return reverse('photo:products')

    def save(self, **kwargs):
        super(Product, self).save()
        mywidth = 440
        if self.photo:
            image = Image.open(self.photo)
            wpercent = (mywidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((mywidth, hsize), Image.ANTIALIAS)
            image.save(self.photo.path)

    class Meta:
        ordering = ['product_name']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude= ('user_name',)

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         obj.user_name = request.user
    #     obj.save()

class ShipPhotoForm(ModelForm):
    class Meta:
        model = ShipPhoto
        exclude= ('user_name',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_name = request.user
        obj.save()

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        exclude= ('user_name',)

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         obj.user_name = request.user
    #     obj.save()

# if form_is_valid():  # uploader has been excluded. No more error.
#     photo = form.save(commit=False)  # returns unsaved instance
#     photo.uploader = request.user
#     photo.save()  # real save to DB.

class PhotoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)