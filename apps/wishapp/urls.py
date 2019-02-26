"""wishes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views
#from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'wishes$', views.wishes),
    url(r'wishes/new$', views.new),
    url(r'wishes/edit/(?P<id>\d+)$', views.edit),
    url(r'wishes/addwish$', views.addwish),
    url(r'wishes/addgrant$', views.addgrant),
    url(r'wishes/addlike$', views.addlike),
    url(r'update$', views.update),
    url(r'wishes/remove$', views.remove),
    url(r'logout$', views.logout),
    url(r'wishes/stats$', views.stats),
    
    
    
    # url(r'wishes$', views.wishes),
    # url(r'edit/(?<id>\d+)$', views.edit),
    # url(r'wishes/new$', views.new),
    # url(r'wishes/stats$', views.stats),
]
