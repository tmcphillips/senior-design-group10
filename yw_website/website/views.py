# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import generic
from django.core.paginator import Paginator

from website.models import Document
from yw_db.models import Workflow, Run, Version
from website.forms import DocumentForm
from website.forms import VersionsForm
from website.forms import ImageUploadForm
from website.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as user_logout
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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

def myworkflows(request):
    documents_list = Workflow.objects.all()
    for document in documents_list:
        latest_version = Version.objects.filter(workflow_id=document.id).order_by('last_modified').first()
        document.graph = latest_version.yw_graph_output if latest_version is not None else ""
    
    paginator = Paginator(documents_list, 10)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    return render(request, 'pages/myworkflows_page.html', { 'document_list': documents })

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        form2 = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form2.is_valid():
                m = ExampleModel.objects.get(pk=course_id)
                m.workflow = form.cleaned_data['image']
                form2.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'script_upload/upload_form.html', {
        'form': form
    })

# Added this
def detailed_workflow(request):
    try:
        # if request.method == "POST":
        #     task_id = QueryDict(request.body).get('task_id')
        #     document = Document.objects.get(pk=task_id).update(completed=True)
        document = Workflow.objects.get(id="1")
        form = VersionsForm(request.POST, request.FILES)
        info = {'document': document, 'form': form}
        return render(request, 'website/detailed_workflow.html', info)
    except Document.DoesNotExist:
      # we have no object!  
      return redirect('home')

def run_detail(request):
    document = Run.objects.get(id="1")
    return render(request, 'website/run_detail.html', { 'document': document })

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('website/home.html')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def users(request):
    users = User.objects.all()
    return render(request, 'users.html', { 'users': users })

# def forgot_password(request):
#     if request.method == 'POST':
#         return password_reset(request, 
#             from_email=request.POST.get('email'))
#     else:
#         return render(request, 'website/forgot_password.html')

def logout(request):
    user_logout(request)
    return render(request,'website/home.html')
