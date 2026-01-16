from django.urls import path
from . import views
from .views import hello_api
from django.conf import settings
from django.conf.urls.static import static


app_name = 'mywebsite'

urlpatterns = [
    # --- HTML / Template Views ---
    path("", views.index, name="index"),
    path("admin2_dashboard/", views.admin2_dashboard, name='admin2_dashboard'),
    path("add/", views.add_myweb, name='add_myweb'),
    path("logout/", views.logout_view, name='logout'),
    path("<int:id>/edit/", views.edit_myweb, name='edit_myweb'),
    path("<int:id>/delete/", views.delete_myweb, name='delete_myweb'),

    # --- API Endpoints (Ito ang lalabas sa Swagger) ---
    path('posts/', views.myweb_list_create, name='myweb-list-api'),
    path('posts/<int:pk>/', views.myweb_detail, name='myweb-detail-api'),
    path('hello/', views.hello_api, name='hello-api'), # Tinanggal ang extra 'api/' dito
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
