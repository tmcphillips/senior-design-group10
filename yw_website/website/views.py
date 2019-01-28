# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views import generic

from website.forms import SignUpForm, VersionSelectionForm
from yw_db.models import Run, Version, Workflow


# def home(request):
#     workflow_list = Workflow.objects.all()
#     version_list = Version.objects.all().order_by('workflow_id', 'last_modified').distinct('workflow_id')
#     for document in version_list:
#         latest_version = Version.objects.filter(workflow=document).order_by('last_modified').first()
#         # TODO: What is this
#         document.graph = latest_version.yw_graph_output if latest_version is not None else ""
    
#     paginator = Paginator(version_list, 10)
#     page = request.GET.get('page')
#     documents = paginator.get_page(page)
#     return render(request, 'pages/home_page.html', { 'document_list': documents })

def home(request):
    workflow_list = Workflow.objects.all()
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

@login_required()
def my_workflows(request):
    documents_list = Workflow.objects.all().filter(user=request.user)
    for document in documents_list:
        latest_version = Version.objects.filter(workflow_id=document.id).order_by('last_modified').first()
        document.graph = latest_version.yw_graph_output if latest_version is not None else ""
    
    paginator = Paginator(documents_list, 10)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    host = request.get_host()
    return render(request, 'pages/my_workflows.html', { 'document_list': documents, 'host': host })

def detailed_workflow(request, workflow_id, version_id):
   
    # html = "<html><body>Version ID: {0}, Workflow ID:{1}</body></html>".format(workflow_id, version_id)
    # return HttpResponse(html)
    try:
        if request.method == "GET":
            form = request.POST
            workflow = Workflow.objects.get(pk=workflow_id)
            version = Version.objects.get(pk=version_id)
            versions = Version.objects.filter(workflow=workflow)

            runs = Run.objects.filter(version=version)
            info = {'workflow': workflow, 'version': version, 'versions':versions ,'runs':runs, 'form': form}
            return render(request, 'pages/detailed_workflow.html', info)
        elif request.method == "POST":
            pass
    
    except ObjectDoesNotExist:
      return redirect(home)

def run_detail(request, run_id):
    try:
        document = Run.objects.get(pk=run_id)
    except Run.DoesNotExist:
        return redirect(home)
    return render(request, 'pages/run_detail.html', { 'document': document })

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(home)
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

# def forgot_password(request):
#     if request.method == 'POST':
#         return password_reset(request, 
#             from_email=request.POST.get('email'))
#     else:
#         return render(request, 'website/forgot_password.html')

def logout(request):
    user_logout(request)
    return render(request,'pages/home_page.html')
