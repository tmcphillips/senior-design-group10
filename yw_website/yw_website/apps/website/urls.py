from django.urls import include, path
from rest_framework import routers

from .views import *

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
    path('', home, name='home'),
    path('my_workflows/', my_workflows, name='my_workflows'),        
    path('detailed_workflow/<int:workflow_id>/version/<int:version_id>/',
         detailed_workflow, name='detailed_workflow'),
    path('run_detail/<int:run_id>/', run_detail, name='run_detail'),

    ###
    # YESWORKFLOW SAVE PATHS
    ###
    path('save/', create_workflow, name='create'),
    path('save/<int:workflow_id>/', update_workflow, name='update'),
    path('save/ping/', yw_save_ping, name='ping'),

    ###
    # REST API PATHS
    ###
    path('api/v1/', include(router.urls)),
]
