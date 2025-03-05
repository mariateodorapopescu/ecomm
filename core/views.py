# from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    # return HttpResponse('Hello, world!')
    # return HttpResponse('<h1 style="color:red">Hello, world!</h1>')
    return render(request, 'core/index.html')
    # return None

# Django uses views, templates and urls to create a page, 
# therefore whenever you want to craete a page you have to create a view for it


