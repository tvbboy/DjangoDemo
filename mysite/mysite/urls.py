"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views
from . import userView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.hello, name="hello"),
    path("nick/", views.nick, name="nick"),
    path("myname/", views.myname, name="myname"),
    path("myfavors/", views.myfavors, name="myfavors"),
    path("myfilters/", views.myfilters, name="myfilters"),
    path("mybooks/", views.mybooks, name="mybooks"),
    path("getpara/", views.getpara, name="getpara"),
    path("reg/", userView.reg, name="reg"),
    path("register/", userView.register, name="register"),
    path("reg_do/", userView.reg_do, name="reg_do"),
    path("reg_withoutdatabase/", userView.reg_withoutdatabase, name="reg_withoutdatabase"),
    
    path("login/", userView.login, name="login"),
    path("login_do/", userView.login_do, name="login_do"),
    path("login_do1/", userView.login_do1, name="login_do1"),
    path("user_profile/", views.user_profile, name="user_profile"),
]

