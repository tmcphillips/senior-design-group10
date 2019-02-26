from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.decorators import (action, api_view, parser_classes,
                                       permission_classes)
from rest_framework.response import Response

from .models import *
from .serializers import *
from .utils import search_and_create_query_set


#############################################################
# Website Views
#############################################################
def home(request):
    edit = False
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

        workflow.tags = (
            TagWorkflow.objects.filter(workflow=workflow).values_list("tag__title", flat=True)
        )

    paginator = Paginator(workflow_list, 10)
    page = request.GET.get("page")
    workflows = paginator.get_page(page)
    host = request.get_host()
    return render(
        request, "pages/home_page.html", {"workflow_list": workflows, "host": host, "edit":edit}
    )


@login_required(login_url="/accounts/login/")
def my_workflows(request):
    edit = True
    workflow_list = (
        Workflow.objects.all().filter(user=request.user).exclude(version__isnull=True)
    )
    for workflow in workflow_list:
        latest_version = (
            Version.objects.filter(workflow=workflow).order_by("last_modified").first()
        )
        if latest_version is None:
            workflow_list = workflow_list.exclude(pk=workflow.id)
        else:
            workflow.graph = latest_version.yw_graph_output
            workflow.version_id = latest_version.id

    paginator = Paginator(workflow_list, 10)
    page = request.GET.get("page")
    workflows = paginator.get_page(page)
    host = request.get_host()
    return render(
        request, "pages/my_workflows.html", {"workflow_list": workflows, "host": host, "edit": edit}
    )

def edit_workflow(request, workflow_id, version_id):
    workflow = Workflow.objects.get(pk=workflow_id)
    workflow_tags = TagWorkflow.objects.filter(workflow=workflow_id)
    if request.method == "POST":
        form = request.POST
        title = request.POST.get("title")
        tags = request.POST.getlist("tagArray")
        t = ''.join(tags)
        t_str = str(t)
        tag_arr = t_str.split(',')
        if tags:
            new_tag = tag_arr
            if len(tag_arr) > 1:
                for tag in tag_arr:
                    t1 = Tag(title=tag, tag_type ="w")
                    t1.save()
                    t2 = TagWorkflow(tag=t1, workflow=workflow)
                    t2.save()
            else:
                string_tag = tag_arr[0]
                t1 = Tag(title=string_tag, tag_type ="w")
                t1.save()
                t2 = TagWorkflow(tag=t1, workflow=workflow)
                t2.save()
        description = request.POST.get("description")
        workflow.title = title
        workflow.description = description
        workflow.save()
        return redirect('my_workflows')
    return render(request, "pages/edit_page.html", {"workflow": workflow, "workflow_tags": workflow_tags})


def detailed_workflow(request, workflow_id, version_id):
    try:
        if request.method == "GET":
            form = request.POST
            workflow = Workflow.objects.get(pk=workflow_id)
            version = Version.objects.get(pk=version_id)
            versions = Version.objects.filter(workflow=workflow)
            tags = TagWorkflow.objects.filter(workflow=workflow).values_list("tag__title", flat=True)

            runs = Run.objects.filter(version=version)
            info = {
                "workflow": workflow,
                "version": version,
                "versions": versions,
                "tags":tags,
                "run_list": runs,
                "form": form,
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
    try:
        run = Run.objects.get(pk=run_id)
        file_list = RunFile.objects.filter(run=run_id)
        run_list = Run.objects.filter(version=run.version)
    except Run.DoesNotExist:
        return Response(status=404, data={"error": "run not found"})

    return render(request, "pages/run_detail.html", {"run": run, "file_list": file_list, "run_list": run_list})


#############################################################
# REST API Views
#############################################################


@api_view(["get"])
@permission_classes((permissions.AllowAny,))
def yw_save_ping(request):
    return Response(status=200, data={"data": "You connected to yw web components."})


@csrf_exempt
@api_view(["post"])
@permission_classes((permissions.AllowAny,))
def create_workflow(request):
    # TODO: Replace username with user auth token
    username = User.objects.filter(username=request.data.get("username", None))

    if not username:
        return Response(status=500, data={"error": "bad username"})

    ws = YesWorkflowSaveSerializer(data=request.data)

    if ws.is_valid():
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
    else:
        return Response(status=500, data={"error": ws.errors})

@csrf_exempt
@api_view(["post"])
@permission_classes((permissions.AllowAny,))
def update_workflow(request, workflow_id):
    w = Workflow.objects.get(pk=workflow_id)
    if request.user.id != w.user_id:
        return Response(status=500, data={"error": "Workflow does not belong to you"})

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
