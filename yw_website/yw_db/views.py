from django.shortcuts import render
from rest_framework import viewsets

from yw_db.models import *
from yw_db.serializers import *

# Create your views here.

class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class RunFileViewSet(viewsets.ModelViewSet):
    queryset = RunFile.objects.all()
    serializer_class = RunFileSerializer

class TagWorkflowViewSet(viewsets.ModelViewSet):
    queryset = TagWorkflow.objects.all()
    serializer_class = TagWorkflowSerializer

class TagVersionViewSet(viewsets.ModelViewSet):
    queryset = TagVersion.objects.all()
    serializer_class = TagVersionSerializer

class TagRunViewSet(viewsets.ModelViewSet):
    queryset = TagRun.objects.all()
    serializer_class = TagRunSerializer

class TagFileSet(viewsets.ModelViewSet):
    queryset = TagFile.objects.all()
    serializer_class = TagFileSerializer
