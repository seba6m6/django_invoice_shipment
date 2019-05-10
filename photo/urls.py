from django.urls import path
from django.urls import re_path
from . import views

app_name = 'photo'

urlpatterns = [
    path('', views.main, name='main'),
    path('photos/', views.newphotoview , name='photos'),
    path('ship-photos/', views.newshipphotoview, name='ship_photos'),
    path('product-photos/', views.productview, name='products'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.PhotoDetailView.as_view(), name='photo_detail'),
    re_path(r'^ship-photo/(?P<pk>[0-9]+)/$', views.ShipPhotoDetailView.as_view(), name='ship_photo_detail'),
    re_path(r'^product-detail/(?P<pk>[0-9]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/photo', views.PhotoCreateNew.as_view(), name='add_photo'),
    path('add/ship-photo', views.ShipPhotoCreate.as_view(), name='add_ship_photo'),
    path('add/product', views.ProductCreate.as_view(), name='add_product'),
    re_path(r'^update/(?P<pk>[0-9]+)/$', views.PhotoUpdate.as_view(), name='update_photo'),
    re_path(r'^update-ship/(?P<pk>[0-9]+)/$', views.ShipPhotoUpdate.as_view(), name='update_ship_photo'),
    re_path(r'^update-product/(?P<pk>[0-9]+)/$', views.ProductUpdate.as_view(), name='update_product'),
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.PhotoDelete.as_view(), name='delete_photo'),
    re_path(r'^delete-ship-photo/(?P<pk>[0-9]+)/$', views.ShipPhotoDelete.as_view(), name='delete_ship_photo'),
    ]