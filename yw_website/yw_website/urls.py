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
from yw_rest_services import views as yw_rest_services_views
from website import views as yw_website_views
from rest_framework import routers

from yw_db.views import *

# REST API ROUTES
router = routers.DefaultRouter()
router.register('workflows', WorkflowViewSet)
router.register('tags', TagViewSet)
router.register('versions', VersionViewSet)
router.register('runs', RunViewSet)
router.register('files', FileViewSet)
router.register('runfiles', RunFileViewSet)
router.register('tagworkflows', TagWorkflowViewSet)
router.register('tagversions', TagVersionViewSet)
router.register('tagruns', TagRunViewSet)
router.register('tagfiles', TagWorkflowViewSet)


urlpatterns = [
    path('admin/', admin.site.urls,),
    path('upload/', yw_website_views.model_form_upload, name='upload'),
    # path('save/ping', yw_rest_services_views.yw_save_ping, name='ping'),
    path('', yw_website_views.DocumentListView.as_view(), name='home'),
    path('my-workflows/', yw_website_views.PersonalWorkflowsView.as_view(), name='my-workflows'),
    path('detailed_workflow/', yw_website_views.detailed_workflow, name = 'detailed_workflow'),
    path('run_detail/', yw_website_views.run_detail, name='run_detail'),
    path('login/', include('django.contrib.auth.urls'), name ='login'),

    #REST API URLS
    path('api/v1/', include(router.urls)),


    # path('api-auth/', include('rest_framework.urls')), # This is for rest stuff that should be hidden behind authentication.
    # path('home/login/', include('django.contrib.auth.urls'), name ='password_reset'),
    path('register/', yw_website_views.register, name='register'),
    path('logout/', yw_website_views.logout, name='logout'),
    path('users/', yw_website_views.users, name = 'users'),
    # used exclusively for texting, will need to remove later
    path('upload/', yw_website_views.model_form_upload, name='upload'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
