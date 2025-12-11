from django.shortcuts import render, redirect, get_object_or_404
# TINANGGAL: Ang 'from django.shortcuts import render' ay kalabisan dahil ito ay nasa unang linya na
from posts.models import Post
from posts.forms import PostForm # TAMA na: PostForm (malaking F) ang gamit

# Ang function name ay ginawang edit_post (walang 's') para tumugma sa urls.py
def index(request):
    posts = Post.objects.all()
    context = {'title': 'My First Portfolio', 'posts': posts}
    return render(request, 'index.html', context)

def admin_dashboard(request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request, 'admin/home.html', context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post
    }
    
    return render(request, 'admin/post_detail.html', context)


# KORAPSYON: Binago ang edit_posts sa edit_post (walang 's')
def edit_post(request, id): 
    # 1. Kuhanin ang Object
    post = get_object_or_404(Post, id=id)
    
    # 2. Form Initialization: Kasama ang request.FILES at instance=post
    form = PostForm(request.POST or None, request.FILES or None, instance=post) 

    if request.method == 'POST':
        if form.is_valid():
            
            updated_post = form.save(commit=False)
            updated_post.user = post.user 
            updated_post.save() 

            return redirect('post_detail', id=post.id) 
        
    context = {
        'form': form, 
        'post': post
    }
    # Tiyakin na tama ang template path
    return render(request, 'admin/edit.html', context)