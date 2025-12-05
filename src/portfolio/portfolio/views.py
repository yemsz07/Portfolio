from django.http import HttpResponse
from django.shortcuts import render 
from posts.models import Post

def index(request):
    posts = Post.objects.all()
    context = {
        'title': 'My First Portfolio',
        'posts': posts
    }
    return render(request, 'index.html', context)

