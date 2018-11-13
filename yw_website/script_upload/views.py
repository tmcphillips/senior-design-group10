# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import generic

from script_upload.models import Document
from script_upload.forms import DocumentForm
from script_upload.forms import VersionsForm
from script_upload.forms import ImageUploadForm
from script_upload.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login


def home(request):
    documents = Document.objects.all()
    return render(request, 'script_upload/base.html', { 'documents': documents })

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
        document = Document.objects.get(id="1")
        form = VersionsForm(request.POST, request.FILES)
        info = {'document': document, 'form': form}
        return render(request, 'script_upload/detailed_workflow.html', info)
    except Document.DoesNotExist:
      # we have no object!  
      return redirect('home')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def users(request):
    users = User.objects.all()
    return render(request, 'users.html', { 'users': users })


class DocumentListView(generic.ListView):
    model = Document
    context_object_name = 'document_list'
    template_name = 'script_upload/home.html'  


