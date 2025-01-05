"""
URL configuration for chaiheadq project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
#import url setting
# from django.conf import settings
# from django.conf.urls.static import static
from . import views 
from .views import success
urlpatterns = [
    path('',views.tweet_list,name='tweet_list'),
    path('create/',views.tweet_create,name='tweet_create'),
    path('<int:tweet_id>/edit/',views.tweet_edit,name='tweet_edit'),
    path('<int:tweet_id>/delete/',views.tweet_delete,name='tweet_delete'),
    # path('testing/','views.index',name='tweet_list')
    path('register/',views.register,name='register'),
    path('about/',views.about,name='about') ,
    path('contact/', views.index, name="index"),
    # path('readmore',views.detail,name='tweet_detail')
    #payments integration
   
    path('success/',views.success,name="success"),
    path('paywithrazorpay/', views.paywithrazorpay, name='paywithrazorpay')
    
    
] 