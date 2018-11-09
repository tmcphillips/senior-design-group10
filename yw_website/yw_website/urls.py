"""yw_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from script_upload import views as script_upload_views
from yw_rest_services import views as yw_rest_services_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.DocumentListView.as_view(), name='home'),
    # path('home/', views.home, name='home'),
    path('home/', include('django.contrib.auth.urls'), name ='login'),
    path('home/register/', views.register, name='register'),
    path('home/users/', views.users, name = 'users'),
    # path('upload/', views.model_form_upload, name='upload'),
    #test path- remove later
    path('home/test', views.home, name='test')
    path('', script_upload_views.home, name='home'),
    path('upload/', script_upload_views.model_form_upload, name='upload'),
    path('save/ping', yw_rest_services_views.yw_save_ping, name='ping'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
