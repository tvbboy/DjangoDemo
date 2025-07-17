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
from . import views as mysite_views
from . import userView
from userModel import views as userModel_views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", mysite_views.hello, name="hello"),
    path("nick/", mysite_views.nick, name="nick"),
    path("myname/", mysite_views.myname, name="myname"),
    path("myfavors/", mysite_views.myfavors, name="myfavors"),
    path("myfilters/", mysite_views.myfilters, name="myfilters"),
    path("mybooks/", mysite_views.mybooks, name="mybooks"),
    path("getpara/", mysite_views.getpara, name="getpara"),
    path("user_profile/", mysite_views.user_profile, name="user_profile"),

    
   
    
    path("login/", userModel_views.login, name="login"),
    path("login_withSQL/", userModel_views.login_withSQL, name="login_withSQL"),
    path("login_withORM/", userModel_views.login_withORM, name="login_withORM"),
    
    path("reg/", userModel_views.reg, name="reg"),
    path("register/", userModel_views.register, name="register"),    
    path("reg_withoutdatabase/", userModel_views.reg_withoutdatabase, name="reg_withoutdatabase"),
    path("reg_withORM/", userModel_views.reg_withORM, name="reg_withORM"),
    path("reg_withSQL/", userModel_views.reg_withSQL, name="reg_withSQL"),
]

