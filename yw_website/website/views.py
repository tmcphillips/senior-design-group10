from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from yw_db.models import Run, Version, Workflow


def home(request):
    workflow_list = Workflow.objects.all().exclude(version__isnull=True)
    for workflow in workflow_list:
        latest_version = Version.objects.filter(workflow=workflow).order_by('last_modified').first()
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

    return render(request, 'pages/home_page.html', { 'workflow_list': workflows, 'host': host  })

@login_required(login_url='/accounts/login/')
def my_workflows(request):
    workflow_list = Workflow.objects.all().filter(user=request.user).exclude(version__isnull=True)
    for workflow in workflow_list:
        latest_version = Version.objects.filter(workflow=workflow).order_by('last_modified').first()
        if latest_version is None:
            workflow_list = workflow_list.exclude(pk=workflow.id)
        else:
            workflow.graph = latest_version.yw_graph_output
            workflow.version_id = latest_version.id

    paginator = Paginator(workflow_list, 10)
    page = request.GET.get('page')
    workflows = paginator.get_page(page)
    host = request.get_host()

    return render(request, 'pages/home_page.html', { 'workflow_list': workflows, 'host': host  })
def detailed_workflow(request, workflow_id, version_id):
    try:
        if request.method == "GET":
            form = request.POST
            workflow = Workflow.objects.get(pk=workflow_id)
            version = Version.objects.get(pk=version_id)
            versions = Version.objects.filter(workflow=workflow)

            runs = Run.objects.filter(version=version)
            info = {'workflow': workflow, 'version': version, 'versions':versions ,'run_list':runs, 'form': form}
            return render(request, 'pages/detailed_workflow.html', info)
        elif request.method == "POST":
            new_version = request.POST['version_id']
            return redirect('/detailed_workflow/{}/{}/'.format(workflow_id, new_version))
    
    except ObjectDoesNotExist:
        return Response(status=404, data={'error':'workflow not found'})

def run_detail(request, run_id):
    try:
        document = Run.objects.get(pk=run_id)
    except Run.DoesNotExist:
        return Response(status=404, data={'error':'run not found'})

    return render(request, 'pages/run_detail.html', { 'document': document })

