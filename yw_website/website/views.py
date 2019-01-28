# Create your views here.
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from yw_db.models import Run, Version, Workflow

# from django.contrib.auth.views import password_reset_view


def home(request):
    documents_list = Workflow.objects.all()
    for document in documents_list:
        latest_version = Version.objects.filter(workflow_id=document.id).order_by('last_modified').first()
        document.graph = latest_version.yw_graph_output if latest_version is not None else ""
    
    paginator = Paginator(documents_list, 10)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    host = request.get_host()
    return render(request, 'pages/home_page.html', { 'document_list': documents, 'host': host })

@login_required(login_url='/accounts/login/')
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

def detailed_workflow(request, document_id):
    try:
        # TODO: change to get object or 404
        if request.method == "GET":
            document = Workflow.objects.get(pk=document_id)
            info = {'document': document}
            return render(request, 'pages/detailed_workflow.html', info)
    except Workflow.DoesNotExist:
      return redirect(home)

def run_detail(request):
    document = Run.objects.get(id="1")
    return render(request, 'pages/run_detail.html', { 'document': document })

