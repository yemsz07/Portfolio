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
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema


#==========================================================================================
# API Views

@extend_schema(
    # Pinipilit natin ang Swagger na magpakita ng Form sa halip na JSON box
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'description': {'type': 'string'},
                'image': {'type': 'string', 'format': 'binary'}, # Ito ang maglalabas ng Choose File button
            },
        },
    },
)
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
            # Sinisave ang user base sa request
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Retrieve, Update, or Delete a Web Post",
    description="Kukuha, mag-uupdate, o magbubura ng specific na post base sa Primary Key (ID).",
    responses={200: MyWebSerializer, 204: None},
)
@api_view(['GET', 'PUT', 'DELETE']) 
@permission_classes([IsAuthenticated])  
def myweb_detail(request, pk):
    post = get_object_or_404(myweb, pk=pk)

    if request.method == 'GET':
        serializer = MyWebSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # partial=True para pwedeng i-update kahit ilang fields lang
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


from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import myweb


def index(request):
    mywebs = myweb.objects.all().order_by('-pub_date')
    paginator = Paginator(mywebs, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'mywebs': page_obj, 'page_obj': page_obj})


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



    
#==================================================================================================
#CBV


#class StudentaddView(View):
#    def get(self, request):
#        form = Sampleform()
#        return render(request, 'studentadd.html',{'form':form})

#    def post(self, request):
#        form = Sampleform(request.POST or None)
#        if form.is_valid():
#            form.save()
#            return render(request, 'studentadd.html',{'form':form})

#class StudenteditView(View):
#    def get(self, request, id):
#        student = Student.objects.get(id=id)
#        form = Sampleform(instance=student)
#        return render(request, 'studentedit.html',{'form':form})
#    def post(self, request, id):
#        student = Student.objects.get(id=id)
#        form = Sampleform(request.POST or None, instance=student)
#        if form.is_valid():
#            form.save()
#            return render(request, 'studentedit.html',{'form':form})
        #student = Student.objects.get(id=id)
        #form = Sampleform(request.POST or None, instance=student)
        #if form.is_valid():
        #    form.save()
        #    return render(request, 'studentedit.html',{'form':form})

#class StudentdeleteView(View):
#    def get(self, request, id):
#        student = Student.objects.get(id=id)
#        return render(request, 'studentdelete.html',{'form':form})
#    def post(self, request, id):
#        student = Student.objects.get(id=id)
#        student.delete()
#        return redirect('myapp:studentlist')

#class StudentlistView(ListView):
#    def get_context_data(self, request):
#        context = {'student': Student.objects.all()}
#        return context
#    def get(self, request):
#        context = self.get_context_data()
        #return render(request, 'studentlist.html', context)
        

#from http.client import HttpResponse
#from django.contrib import messages
#from django.db.models import Q
#from django.views.generic import ListView, CreateView, UpdateView, DeleteView
#from django.contrib.messages.views import SuccessMessageMixin
#from django.urls import reverse_lazy


#class StudentAddView(SuccessMessageMixin,CreateView):
#    model = Student
#    fields = ['name', 'image', 'age', 'gender', 'address', 'phone', 'email', 'date']
#    template_name = 'studentadd.html'
#    success_url = reverse_lazy('student-add')
#    success_message = "Successfully added"

#class StudentListView(ListView):
#    model = Student
#    template_name = 'studentlist.html'
#    context_object_name = 'student'
#    success_url = reverse_lazy('student-list')

    #def get_queryset(self):
    #    queries = self.request.GET.get('q', '')
    #    if queries:
    #        results = Student.objects.filter(Q(name__icontains=queries) | Q(age__icontains=queries) | Q(gender__icontains=queries))
    #        return results
    #    else:
    #        return Student.objects.all()

#class StudentEditView(SuccessMessageMixin,UpdateView):
    #model = Student
    #fields = ['name', 'image', 'age', 'gender', 'address', 'phone', 'email', 'date']
    #template_name = 'studentedit.html'
    #success_url = reverse_lazy('student-list')
    #success_message = "Successfully updated"

    #def dispatch(self, request, *args, **kwargs):
    #    student_id = kwargs.get('pk')
    #    if student_id == 1:
    #        return HttpResponse('DO NOT EDIT THIS STUDENT!')
    #    return super().dispatch(request, *args, **kwargs)

#class StudentdeleteView(SuccessMessageMixin,DeleteView):
    #model = Student
    #template_name = 'studentdelete.html'
    #success_url = reverse_lazy('student-list')

    #def delete(self, request, *args, **kwargs):
    #    self.object = self.get_object()
    #    if self.object.id == 1:
    #        messages.error(request, 'DO NOT DELETE THIS STUDENT!')
    #        return redirect(self.success_url)
    #    messages.success(request, 'Successfully deleted')
    #    return super().delete(request, *args, **kwargs)
    