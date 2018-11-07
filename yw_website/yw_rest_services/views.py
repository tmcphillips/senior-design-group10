from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def yw_save_ping(request):
    return HttpResponse(content=b"You connected to yw web components.")
