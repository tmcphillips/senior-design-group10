# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from script_upload.models import Document
from script_upload.forms import DocumentForm


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
