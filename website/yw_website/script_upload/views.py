# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from script_upload.models import Document
from script_upload.forms import DocumentForm
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
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'script_upload/upload_form.html', {
        'form': form
    })


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


