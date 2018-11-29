from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import parser_classes
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from yw_db.models import *
from yw_db.serializers import *
from django.contrib.auth.models import User
import datetime



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
        last_modified=datetime.datetime.now()
    )
    v.save()
    r = Run(
        version = Version.objects.get(pk=v.id),
        yw_recon_output = request.data.get('recon', ''),
        run_time_stamp = datetime.datetime.now()
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

    
 



