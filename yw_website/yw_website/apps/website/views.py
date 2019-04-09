from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *
from .utils import search_and_create_query_set, get_block_data

from rest_framework import serializers
from django.http import HttpResponseRedirect



#############################################################
# Website Views
#############################################################
def home(request):
    if 'q' in request.GET:
        workflow_list = search_and_create_query_set(request.GET['q'])

    else:
        workflow_list = Workflow.objects.all().exclude(version__isnull=True)

    for workflow in workflow_list:
        latest_version = (
            Version.objects.filter(workflow=workflow).order_by("last_modified").first()
        )

        workflow.graph = latest_version.yw_graph_output
        workflow.version_id = latest_version.id
        workflow.version_modified = latest_version.last_modified

        workflow.tags = TagWorkflow.objects.filter(workflow=workflow)

    workflow_list = sorted(workflow_list, key=lambda t: t.version_modified, reverse=True)


    paginator = Paginator(workflow_list, 10)
    page = request.GET.get("page")
    workflows = paginator.get_page(page)
    host = request.get_host()
    return render(
        request, "pages/home_page.html", {"workflow_list": workflows, "host": host}
    )


@login_required(login_url="/accounts/login/")
def my_workflows(request):
    if 'q' in request.GET:
        workflow_list = search_and_create_query_set(request.GET['q'])

    else:
        workflow_list = Workflow.objects.all().exclude(version__isnull=True)

    for workflow in workflow_list:
        latest_version = (
            Version.objects.filter(workflow=workflow).order_by("last_modified").first()
        )
        if latest_version is None:
            workflow_list = workflow_list.exclude(pk=workflow.id)
        else:
            workflow.graph = latest_version.yw_graph_output
            workflow.version_id = latest_version.id
            workflow.version_modified = latest_version.last_modified

            workflow.tags = TagWorkflow.objects.filter(workflow=workflow)

    workflow_list = sorted(workflow_list, key=lambda t: t.version_modified, reverse=True)

    paginator = Paginator(workflow_list, 10)
    page = request.GET.get("page")
    workflows = paginator.get_page(page)
    host = request.get_host()
    return render(
        request, "pages/my_workflows.html", {"workflow_list": workflows, "host": host, "can_edit_tags":True}
    )


def edit_workflow(request, workflow_id, version_id):
    if 'q' in request.GET:
        return redirect('/?q={}'.format(request.GET['q']))

    workflow = Workflow.objects.get(pk=workflow_id)
    workflow_tags = TagWorkflow.objects.filter(workflow=workflow_id)
    if request.method == "POST":
        form = request.POST
        title = request.POST.get("title")
        tags = request.POST.getlist("tagArray")
        t = "".join(tags)
        t_str = str(t)
        tag_arr = t_str.split(",")
        if tags:
            new_tag = tag_arr
            if len(tag_arr) > 1:
                for tag in tag_arr:
                    t1 = Tag(title=tag, tag_type="w")
                    t1.save()
                    t2 = TagWorkflow(tag=t1, workflow=workflow)
                    t2.save()
            else:
                string_tag = tag_arr[0]
                t1 = Tag(title=string_tag, tag_type="w")
                t1.save()
                t2 = TagWorkflow(tag=t1, workflow=workflow)
                t2.save()
        description = request.POST.get("description")
        workflow.title = title
        workflow.description = description
        workflow.save()
        return redirect("my_workflows")
    return render(
        request,
        "pages/edit_page.html",
        {"workflow": workflow, "workflow_tags": workflow_tags},
    )


def detailed_workflow(request, workflow_id, version_id):
    edit = False
    if 'q' in request.GET:
        return redirect('/?q={}'.format(request.GET['q']))

    try:
        if request.method == "GET":
            form = request.POST
            workflow = Workflow.objects.get(pk=workflow_id)
            if workflow.user == request.user:
                edit = True
            version = Version.objects.get(pk=version_id)
            versions = Version.objects.filter(workflow=workflow)
            tags = TagWorkflow.objects.filter(workflow=workflow)

            runs = Run.objects.filter(version=version)
            info = {
                "workflow": workflow,
                "version": version,
                "versions": versions,
                "tags": tags,
                "run_list": runs,
                "form": form,
                "edit": edit,
            }
            return render(request, "pages/detailed_workflow.html", info)
        elif request.method == "POST":
            new_version = request.POST["version_id"]
            return redirect(
                "/detailed_workflow/{}/version/{}/".format(workflow_id, new_version)
            )

    except ObjectDoesNotExist:
        return Response(status=404, data={"error": "workflow not found"})


def run_detail(request, run_id):
    if 'q' in request.GET:
        return redirect('/?q={}'.format(request.GET['q']))
    try:
        run = Run.objects.get(pk=run_id)
        resource_list = Resource.objects.filter(run=run)
        runs = Run.objects.filter(version=run.version)
        block_inputs = get_block_data(run_id)
    except Run.DoesNotExist:
        return Response(status=404, data={"error": "run not found"})

    return render(
        request,
        "pages/run_detail.html",
        {"run": run, "file_list": resource_list, "runs": runs, "blocks": block_inputs, "graph_output": run.version.yw_graph_output},
    )

def delete_workflows(request, workflow_id):
    workflow = get_object_or_404(Workflow, pk=workflow_id)
    workflow.delete()
    return redirect('my_workflows')

def delete_runs(request, workflow_id, run_id, version_id):
    run = get_object_or_404(Run, pk=run_id)
    run.delete()
    return redirect(
                "/detailed_workflow/{}/version/{}/".format(workflow_id, version_id)
            )

def delete_versions(request, workflow_id, run_id, version_id):
    version = get_object_or_404(Version, pk=version_id)
    version.delete()
    return redirect(
                "/detailed_workflow/{}/version/{}/".format(workflow_id, version_id)
            )

def tag_delete(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    tag.delete()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#############################################################
# REST API Views
#############################################################

@api_view(["get"])
@permission_classes((permissions.AllowAny,))
def yw_save_ping(request):
    return Response(status=200, data={"data": "You connected to yw web components."})

@csrf_exempt
@api_view(["post"])
@authentication_classes((TokenAuthentication, BasicAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def create_workflow(request):
    user = request.user
    ws = YesWorkflowSaveSerializer(data=request.data, context={"username": user})

    if ws.is_valid():
        try:
            w_id, v_id, r_num = ws.create(ws.validated_data)
            w = Workflow.objects.get(pk=w_id)
            v = Version.objects.get(pk=v_id)
            version_num = len(Version.objects.filter(workflow=w))
            run_num = len(Run.objects.filter(version=v))

            return Response(
                status=200,
                data={
                    "workflowId": w_id,
                    "versionNumber": version_num,
                    "runNumber": run_num,
                },
            )
        except serializers.ValidationError:
            return Response(status=500, data={"error": ws.errors})
    else:
        return Response(status=500, data={"error": ws.errors})


@csrf_exempt
@api_view(["post"])
@authentication_classes((TokenAuthentication, BasicAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def update_workflow(request, workflow_id):
    user = request.user

    w = Workflow.objects.get(pk=workflow_id)
    if user != w.user:
        return Response(status=403, data={"message": "Workflow does not belong to you"})

    ws = YesWorkflowSaveSerializer(
        data=request.data, context={"workflow_id": workflow_id}
    )

    if ws.is_valid():
        w_id, v_id, r_num, new_version = ws.update(ws.validated_data)
        w = Workflow.objects.get(pk=w_id)
        v = Version.objects.get(pk=v_id)
        version_num = len(Version.objects.filter(workflow=w))
        run_num = len(Run.objects.filter(version=v))
        return Response(
            status=200,
            data={
                "workflowId": w_id,
                "versionNumber": version_num,
                "runNumber": run_num,
                "newVersion": new_version,
            },
        )
    else:
        return Response(status=500, data={"error": ws.errors})


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


class TagWorkflowViewSet(viewsets.ModelViewSet):
    queryset = TagWorkflow.objects.all()
    serializer_class = TagWorkflowSerializer


class TagVersionViewSet(viewsets.ModelViewSet):
    queryset = TagVersion.objects.all()
    serializer_class = TagVersionSerializer


class TagRunViewSet(viewsets.ModelViewSet):
    queryset = TagRun.objects.all()
    serializer_class = TagRunSerializer
    

class ProgramBlockSet(viewsets.ModelViewSet):
    class _ProgramBlockSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProgramBlock 
            fields = '__all__'
    queryset = ProgramBlock.objects.all()
    serializer_class = _ProgramBlockSerializer 

class DataSet(viewsets.ModelViewSet):
    class _DataSerializer(serializers.ModelSerializer):
        class Meta:
            model = Data 
            fields = '__all__'
    queryset = Data.objects.all()
    serializer_class = _DataSerializer 

class PortSet(viewsets.ModelViewSet):
    class _PortSerializer(serializers.ModelSerializer):
        class Meta:
            model = Port 
            fields = '__all__'
    queryset = Port.objects.all()
    serializer_class = _PortSerializer 

class ChannelSet(viewsets.ModelViewSet):
    class _ChannelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Channel 
            fields = '__all__'
    queryset = Channel.objects.all()
    serializer_class = _ChannelSerializer 

class UriVariableSet(viewsets.ModelViewSet):
    class _UriVariableSerializer(serializers.ModelSerializer):
        class Meta:
            model = UriVariable 
            fields = '__all__'
    queryset = UriVariable.objects.all()
    serializer_class = _UriVariableSerializer 

class ResourceSet(viewsets.ModelViewSet):
    class _ResourceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Resource
            fields = '__all__'
    queryset = Resource.objects.all()
    serializer_class = _ResourceSerializer 

class UriVariableValueSet(viewsets.ModelViewSet):
    class _UriVariableValueSerializer(serializers.ModelSerializer):
        class Meta:
            model = UriVariableValue 
            fields = '__all__'
    queryset = UriVariableValue.objects.all()
    serializer_class = _UriVariableValueSerializer 
