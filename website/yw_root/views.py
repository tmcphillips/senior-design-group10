# Create your views here.

from django.shortcuts import render



def index(request):
    context = {}
    return render(request, 'yw_website/index.html', context)