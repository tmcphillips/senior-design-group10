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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

import website.views as views
from website.views import *

### 
# DATABASE PATHS
###
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
    ### 
    # YESWORKFLOW WEBSERVER PATHS
    ###
    path('', views.home, name='home'),
    path('my_workflows/', views.my_workflows, name='my_workflows'),
    path('detailed_workflow/<int:workflow_id>/version/<int:version_id>/', views.detailed_workflow, name='detailed_workflow'),
    path('run_detail/<int:run_id>/', views.run_detail, name='run_detail'),

    ###
    # YESWORKFLOW SAVE PATHS
    ###
    path('save/', views.create_workflow, name='create'),
    path('save/<int:workflow_id>/', views.update_workflow, name='update'),
    path('save/ping/', views.yw_save_ping, name='ping'),

    ###
    # REST API PATHS
    ###
    path('api/v1/', include(router.urls)),

    ###
    # USER PATHS
    ###
    path('admin/', admin.site.urls,),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
