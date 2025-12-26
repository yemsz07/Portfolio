from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import myweb
from .forms import Webform



def index(request):
    mywebs = myweb.objects.all().order_by('-pub_date')
    return render(request, 'index.html', {
        'title': 'Mywebsite',
        'mywebs': mywebs,
    }
    )
@login_required
def admin2_dashboard(request):
    mywebs = myweb.objects.all().order_by('-pub_date')
    return render(request, 'dashboard/home.html',{'mywebs': mywebs,})


@login_required
def add_myweb(request):
    form = Webform(request.POST or None, request.FILES or None)
    if form.is_valid():
        myweb = form.save(commit=False)
        myweb.user = request.user   
        myweb.save()   
        return redirect('mywebsite:admin2_dashboard')
    return render(request, 'dashboard/add.html', {'form': form})

@login_required
def edit_myweb(request, id):
    myweb_instance = get_object_or_404(myweb, id=id)
    
    if request.method == 'POST':
        form = Webform(request.POST, request.FILES, instance=myweb_instance)
        if form.is_valid():
            form.save()
            return redirect('mywebsite:admin2_dashboard')
    else:
        form = Webform(instance=myweb_instance)
    
    return render(request, 'dashboard/edit.html', {'form': form, 'myweb': myweb_instance}) 
    

@login_required
def delete_myweb(request, id):
    myweb_instance = get_object_or_404(myweb, id=id)
    myweb_instance.delete()
    return redirect('mywebsite:admin2_dashboard')


def logout_view(request):
    logout(request)
    return redirect('/auth/login/')

