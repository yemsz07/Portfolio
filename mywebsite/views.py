from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import myweb
from .forms import Webform
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MyWebSerializer
from .models import myweb
from django.shortcuts import get_object_or_404


#==========================================================================================
# API Views


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def myweb_list_create(request):
    if request.method == 'GET':
        posts = myweb.objects.all()
        serializer = MyWebSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MyWebSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']) 
@permission_classes([IsAuthenticated])  
def myweb_detail(request, pk):
    post = get_object_or_404(myweb, pk=pk)

    if request.method == 'GET':
        serializer = MyWebSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MyWebSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

#==================================================================================================
# Django Views
#FBV


def index(request):
    mywebs = myweb.objects.all().order_by('-pub_date')
    paginator = Paginator(mywebs, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)


    return render(request, 'index.html', {
        'title': 'Mywebsite',
        'mywebs': page_obj,
    }
    )
@login_required
def admin2_dashboard(request):
    mywebs = myweb.objects.all().order_by('-pub_date')
    paginator = Paginator(mywebs, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/home.html',{'mywebs': page_obj, 'page_obj': page_obj})


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


@api_view(['GET'])
def hello_api(request):
    return Response({
        "message": "Hello DRF",
        "status": "working"
    })