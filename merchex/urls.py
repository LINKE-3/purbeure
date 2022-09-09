"""merchex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from listings import views
from django.conf.urls import handler500, handler404

handler500 = 'listings.views.handler500'
handler404 = 'listings.views.handler404'

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello),
    path('admin/', admin.site.urls),
    path('search/', views.search, name='search'),
    path('product/<path:product_name>', views.product, name='product'),
    path('save-alt', views.save_alt, name='save_alt'),
    path('register', views.registration, name='register'),
    path('connection', views.connection, name="connection"),
    path('disconnection', views.disconnection, name='logout'),
    path('account', views.account, name='account'),
    path('aliments', views.aliments, name="aliments"),
    path('mentions', views.mentions, name="mentions"),
    path('contact', views.contact, name='contact')
]
