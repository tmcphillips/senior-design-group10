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

from website import views as yw_website_views
from yw_db.views import *
from yw_rest_services import views as yw_rest_services_views

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
    path('', yw_website_views.home, name='home'),
    path('my_workflows/', yw_website_views.my_workflows, name='my_workflows'),
    path('detailed_workflow/<int:workflow_id>/', yw_website_views.detailed_workflow, name='detailed_workflow'),
    path('run_detail/<int:run_id>/', yw_website_views.run_detail, name='run_detail'),

    ###
    # YESWORKFLOW SAVE PATHS
    ###
    path('save/', yw_rest_services_views.create_workflow, name='create'),
    path('save/<int:workflow_id>/', yw_rest_services_views.update_workflow, name='update'),
    path('save/ping/', yw_rest_services_views.yw_save_ping, name='ping'),

    ###
    # REST API PATHS
    ###
    path('api/v1/', include(router.urls)),

    ###
    # USER PATHS
    ###
    path('', include('django.contrib.auth.urls'), name='login'),
    path('register/', yw_website_views.register, name='register'),
    path('logout/', yw_website_views.logout, name='logout'),
    path('admin/', admin.site.urls,),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
