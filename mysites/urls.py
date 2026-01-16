"""
URL configuration for mysites project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# Wagtail Imports
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# Spectacular Imports
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from mywebsite import views # Import para sa index view mo

urlpatterns = [
    # 1. Admin Interfaces
    path('admin2/', admin.site.urls),          # Django Admin
    path('admin/', include(wagtailadmin_urls)), # Wagtail Admin
    path('documents/', include(wagtaildocs_urls)),

    # 2. Authentication
    path('auth/', include('django.contrib.auth.urls')),

    # 3. API Endpoints (Dito papasok ang /posts/ at /hello/)
    # Ginamit natin ang 'api/v1/' para malinis ang versioning
    path('api/v1/', include('mywebsite.urls')),

    # 4. API Schema & Documentation (Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # 5. Main Website Index (HTML)
    path('', include('mywebsite.urls')),

    # 6. Wagtail Pages (Dapat laging huli dahil ito ay "catch-all")
    re_path(r'', include(wagtail_urls)),
]

# Static at Media Files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)