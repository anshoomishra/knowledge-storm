from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
# Create your views here.

def test(request):
    return HttpResponse("Hello Golu Bitti")

