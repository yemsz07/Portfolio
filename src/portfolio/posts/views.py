# C:\Users\Dell\projects\Portfolio\src\portfolio\posts\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model # KRITIKAL: Para sa User Logic
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Kuhanin ang User Model para sa default user assignment
User = get_user_model() 

def index(request):
    """ Public Home Page """
    posts = Post.objects.all().order_by('-created_at') # I-order para mas updated ang posts
    context = {'title': 'My First Portfolio', 'posts': posts}
    # Tiyakin na ang template ay nasa tamang lokasyon (e.g., templates/index.html)
    return render(request, 'index.html', context)

@login_required
def admin_dashboard(request):
    """ Custom Admin Dashboard (View ng lahat ng posts) """
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts
    }
    # Tiyakin na ang template ay nasa tamang lokasyon (e.g., templates/admin/home.html)
    return render(request, 'admin/home.html', context)

def post_detail(request, id):
    """ Detalye ng isang post """
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post
    }
    return render(request, 'admin/post_detail.html', context)

def edit_post(request, id): 
    """ Pag-update ng isang post """
    # Maaaring magdagdag ng login_required decorator dito sa huli
    post = get_object_or_404(Post, id=id)
    
    # Gumagamit ng request.POST or None at request.FILES or None
    form = PostForm(request.POST or None, request.FILES or None, instance=post) 

    if request.method == 'POST':
        if form.is_valid():
            # Hindi na kailangan ng commit=False dito, maliban kung baguhin ang ibang fields
            form.save() 
            return redirect('post_detail', id=post.id) 
        
    context = {
        'form': form, 
        'post': post
    }
    return render(request, 'admin/edit.html', context)

def add_post(request):
    """ Paglikha ng bagong post (Create) """
    # Maaaring magdagdag ng login_required decorator dito sa huli
    form = PostForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        new_post = form.save(commit=False)
        
        # 🛑 KRITIKAL NA PAG-AAYOS: User Assignment 🛑
        if request.user.is_authenticated:
            new_post.user = request.user 
        else:
            # Gamitin ang default user (Tiyakin na may 'default_user' sa DB)
            try:
                default_user = User.objects.get(username='default_user') 
            except User.DoesNotExist:
                # Mag-handle ng error o ituro sa login/registration page
                return render(request, 'admin/error.html', {'message': 'Kailangan ng default user para mag-post.'})
                
            new_post.user = default_user
        
        new_post.save() # Final save kasama ang user
        
        return redirect('post_detail', id=new_post.id)

    return render(request, 'admin/add.html', {
        'form': form,
        'title': 'Add New Items'
    })

@login_required
def delete_post(request, id):
    """ Delete a post with confirmation page """
    post = get_object_or_404(Post, id=id)
    
    # Check if the current user is the author or has permission
    if request.user != post.user and not request.user.is_superuser:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        post.delete()
        return redirect('admin_dashboard')  # This should now work
    
    return render(request, 'admin/delete.html', {'post': post})