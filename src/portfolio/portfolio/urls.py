"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import admin_dashboard, edit_post # 1. INAYOS: Binago ang 'edit_posts' sa 'edit_post'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import post_detail

urlpatterns = [
    # Path para sa Admin Dashboard
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    
    path('<int:id>/', post_detail, name='post_detail'),
    # KORAPSYON: Inayos ang ID capture sa <int:id> at pinalitan ang function name at URL name
    path('posts/edit/<int:id>/', edit_post, name="edit_post"),
    
    path('admin/', admin.site.urls),
    
    # Tiyakin na ang 'posts.urls' ay umiiral at naglalaman ng 'post_detail'
    path('', include('posts.urls')), 
]

# Tiyakin na ito ay nasa pinakadulo ng file (at kung nasa development mode ka)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

