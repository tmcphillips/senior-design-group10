# Create your views here.
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views import generic

from website.forms import SignUpForm
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
    return render(request, 'pages/home_page.html', { 'document_list': documents })

def my_workflows(request):
    # TODO: Handle unathenticated user? Right now will just load an empty table.
    documents_list = Workflow.objects.all().filter(user=request.user)
    for document in documents_list:
        latest_version = Version.objects.filter(workflow_id=document.id).order_by('last_modified').first()
        document.graph = latest_version.yw_graph_output if latest_version is not None else ""
    
    paginator = Paginator(documents_list, 10)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    return render(request, 'pages/home_page.html', { 'document_list': documents })

def detailed_workflow(request, document_id):
    try:
        # TODO: change to get object or 404
        if request.method == "GET":
            document = Workflow.objects.get(pk=document_id)
            form = VersionsForm(request.POST, request.FILES)
            info = {'document': document, 'form': form}
            return render(request, 'pages/detailed_workflow.html', info)
    except Workflow.DoesNotExist:
      return redirect(home)

def run_detail(request):
    document = Run.objects.get(id="1")
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
