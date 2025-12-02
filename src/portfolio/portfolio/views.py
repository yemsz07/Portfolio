from django.http import HttpResponse
from django.shortcuts import render 

def index(request):
    context = {
        'title': 'Portfolio'
    }
    return render(request, 'index.html', context)

