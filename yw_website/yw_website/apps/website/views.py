import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic
from rest_framework import permissions, viewsets
from rest_framework.decorators import (action, api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


#############################################################
# Website Views
#############################################################
def home(request):
    workflow_list = Workflow.objects.all().exclude(version__isnull=True)
    for workflow in workflow_list:
        latest_version = Version.objects.filter(
            workflow=workflow).order_by('last_modified').first()
        # TODO: every workflow should have at least one version
        if latest_version is None:
            workflow_list = workflow_list.exclude(pk=workflow.id)
        else:
            workflow.graph = latest_version.yw_graph_output
            workflow.version_id = latest_version.id
            workflow.version_modified = latest_version.last_modified

    paginator = Paginator(workflow_list, 10)
    page = request.GET.get('page')
    workflows = paginator.get_page(page)
    host = request.get_host()

    return render(request, 'pages/home_page.html', {'workflow_list': workflows, 'host': host})


@login_required(login_url='/accounts/login/')
def my_workflows(request):
    workflow_list = Workflow.objects.all().filter(
        user=request.user).exclude(version__isnull=True)
    for workflow in workflow_list:
        latest_version = Version.objects.filter(
            workflow=workflow).order_by('last_modified').first()
        if latest_version is None:
            workflow_list = workflow_list.exclude(pk=workflow.id)
        else:
            workflow.graph = latest_version.yw_graph_output
            workflow.version_id = latest_version.id

    paginator = Paginator(workflow_list, 10)
    page = request.GET.get('page')
    workflows = paginator.get_page(page)
    host = request.get_host()

    return render(request, 'pages/home_page.html', {'workflow_list': workflows, 'host': host})


def detailed_workflow(request, workflow_id, version_id):
    try:
        if request.method == "GET":
            form = request.POST
            workflow = Workflow.objects.get(pk=workflow_id)
            version = Version.objects.get(pk=version_id)
            versions = Version.objects.filter(workflow=workflow)

            runs = Run.objects.filter(version=version)
            info = {'workflow': workflow, 'version': version,
                    'versions': versions, 'run_list': runs, 'form': form}
            return render(request, 'pages/detailed_workflow.html', info)
        elif request.method == "POST":
            new_version = request.POST['version_id']
            return redirect('/detailed_workflow/{}/version/{}/'.format(workflow_id, new_version))

    except ObjectDoesNotExist:
        return Response(status=404, data={'error': 'workflow not found'})


def run_detail(request, run_id):
    try:
        run = Run.objects.get(pk=run_id)
    except Run.DoesNotExist:
        return Response(status=404, data={'error': 'run not found'})

    return render(request, 'pages/run_detail.html', {'run': run})

#############################################################
# REST API Views
#############################################################


@api_view(['get', ])
@permission_classes((permissions.AllowAny,))
def yw_save_ping(request):
    return Response(status=200, data={"data": "You connected to yw web components."})


@api_view(['post'])
@permission_classes((permissions.AllowAny,))
def create_workflow(request):
    username = User.objects.filter(username=request.data.get('username', None))
    if not username:
        return Response(status=500, data={'error': 'bad username'})
    username = username[0]
    w = Workflow(
        user=username,
        title=request.data.get('title', 'Title'),
        description=request.data.get('description', 'Description')
    )
    w.save()
    v = Version(
        workflow=w,
        script_check_sum=request.data.get('script_checksum', ''),
        yw_model_check_sum=request.data.get('model_checksum', ''),
        yw_model_output=request.data.get('model', ''),
        yw_graph_output=request.data.get('graph', ''),
        last_modified=datetime.datetime.now(tz=timezone.utc)
    )
    v.save()
    r = Run(
        version=v,
        yw_recon_output=request.data.get('recon', ''),
        run_time_stamp=datetime.datetime.now(tz=timezone.utc)
    )
    r.save()
    wdata = WorkflowSerializer(w).data
    wdata['id'] = w.id
    vdata = VersionSerializer(v).data
    vdata['id'] = v.id
    rdata = RunSerializer(r).data
    rdata['id'] = r.id
    return Response(status=200, data={
        "workflow": wdata,
        "version": vdata,
        'run': rdata
    })


@api_view(['post'])
@permission_classes((permissions.AllowAny,))
def update_workflow(request, workflow_id):
    try:
        w = Workflow.objects.get(pk=workflow_id)
    except Workflow.DoesNotExist:
        return Response(status=500, data={'error': 'Workflow does not exist'})

    if 'model_checksum' not in request.data:
        return Response(status=500, data={'error': 'No model checksum was recieved'})

    v, _ = Version.objects.update_or_create(
        workflow=w,
        yw_model_check_sum=request.data.get('model_checksum', ''),
        defaults={
            'script_check_sum': request.data.get('script_checksum', ''),
            'yw_model_output': request.data.get('model', ''),
            'yw_graph_output': request.data.get('graph', ''),
            'last_modified': datetime.datetime.now(tz=timezone.utc)
        }
    )
    r = Run(
        version=v,
        yw_recon_output=request.data.get('recon', ''),
        run_time_stamp=datetime.datetime.now(tz=timezone.utc)
    )
    r.save()
    wdata = WorkflowSerializer(w).data
    wdata['id'] = w.id
    vdata = VersionSerializer(v).data
    vdata['id'] = v.id
    rdata = RunSerializer(r).data
    rdata['id'] = r.id

    return Response(status=200, data={
        "workflow": wdata,
        "version": vdata,
        'run': rdata
    })

#############################################################
# Database Views
#############################################################


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
