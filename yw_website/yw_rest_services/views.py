import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import (action, api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from yw_db.models import *
from yw_db.serializers import *

# Create your views here.

@api_view(['get',])
@permission_classes((permissions.AllowAny,))
def yw_save_ping(request):
    return Response(status=200, data={"data":"You connected to yw web components."})

@api_view(['post'])
@permission_classes((permissions.AllowAny,))
def create_workflow(request):
    username = User.objects.filter(username=request.data.get('username', None))
    if not username:
        return Response(status=500, data={'error':'bad username'})
    username = username[0]
    w = Workflow(
        user=User.objects.get(username=username),
        title=request.data.get('title', 'Title'),
        description=request.data.get('description','Description')
    )
    w.save()
    v = Version(
        workflow=Workflow.objects.get(pk=w.id),
        script_check_sum=request.data.get('script_checksum', ''),
        yw_model_check_sum=request.data.get('model_checksum', ''),
        yw_model_output=request.data.get('model', ''),
        yw_graph_output=request.data.get('graph', ''),
        last_modified=datetime.datetime.now(tz=timezone.utc)
    )
    v.save()
    r = Run(
        version = Version.objects.get(pk=v.id),
        yw_recon_output = request.data.get('recon', ''),
        run_time_stamp = datetime.datetime.now(tz=timezone.utc)
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
def update_workflow(request):
    username = User.objects.filter(username=request.data.get('username', None))
    if not username:
        return Response(status=500, data={'error':'bad username'})
    username = username[0]

    try:
        w = Workflow.objects.get(pk=request.data.get('workflow_id'))
    except Workflow.DoesNotExist:
        return Response(status=500, data={'error':'workflow does not exist'})

    v = Version(
        workflow=Workflow.objects.get(pk=w.id),
        script_check_sum=request.data.get('script_checksum', ''),
        yw_model_check_sum=request.data.get('model_checksum', ''),
        yw_model_output=request.data.get('model', ''),
        yw_graph_output=request.data.get('graph', ''),
        last_modified=datetime.datetime.now(tz=timezone.utc)
    )
    v.save()
    r = Run(
        version = Version.objects.get(pk=v.id),
        yw_recon_output = request.data.get('recon', ''),
        run_time_stamp = datetime.datetime.now(tz=timezone.utc)
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
