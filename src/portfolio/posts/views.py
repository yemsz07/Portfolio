from django.shortcuts import render
from .models import Post
    
def index(request):
    posts = Post.objects.all()
    context = {'title': 'My First Portfolio', 'posts': posts}
    return render(request, 'index.html', context)


