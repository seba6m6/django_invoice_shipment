from django.urls import path
from django.urls import re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registration/', views.UserFormView.as_view(), name='registration'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

]