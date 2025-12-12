# C:\Users\Dell\projects\Portfolio\src\portfolio\posts\urls.py

from django.urls import path
from . import views # Tiyakin na nandito ang import!

urlpatterns = [
    # Public Views
    path('', views.index, name='home'), # Ang root URL ng project (dahil sa include)
    
    # Admin Views
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('detail/<int:id>/', views.post_detail, name='post_detail'),
    
    # Action Views
    path('edit/<int:id>/', views.edit_post, name='edit_post'),
    path('add/', views.add_post, name='add_post'), # Ito ang hinahanap mong path!
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
]