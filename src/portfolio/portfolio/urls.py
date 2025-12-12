# C:\Users\Dell\projects\Portfolio\src\portfolio\portfolio\urls.py

from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    # DJANGO ADMIN SITE
    path('admin/', admin.site.urls),
    
    # AUTHENTICATION (Login Override)
    path('accounts/login/', 
          auth_views.LoginView.as_view(template_name='registration/login.html'), 
          name='login'), 
          
    # Lahat ng URL ng 'posts' app ay gagamit ng root
    # Dapat ito ang pinakahuling path para ma-capture ang mga apps
    path('', include('posts.urls')), 
    
    # Optional: built-in authentication URLs (para sa logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')), 

    # 🛑 TINANGGAL ANG DAHILAN NG ERROR at MALING LOCATION: path('add/', views.add_post, name='add_post'),
]


if settings.DEBUG:
    # 🛑 KRITIKAL: Dapat kasama ang STATIC files dito para sa development server 🛑
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)