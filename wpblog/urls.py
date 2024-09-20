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
from wpblog import views
from .views import deleteuser, deletepost, deletecategory,importsettings

urlpatterns = [
path('category/', views.category),
path('posts/',views.post),
path('home/',views.home),
path('users/',views.users),
path('users/delete/',deleteuser,name='deleteuser'),
path('posts/delete/',deletepost,name='deletepost'),
path('category/delete/<int:category_id>/',deletecategory,name='deletecategory'),
path('settings/',views.settingspage),
path('import/', importsettings, name='importsettings'),
path('posts/<int:post_id>/',views.postview),
path('posts/edit/<int:post_id>/',views.editpost),
path('posts/save/<int:post_id>/',views.savepost),
path('users/edit/<int:user_id>/',views.edituser)
]
