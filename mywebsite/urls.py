from django.urls import path
from . import views

app_name = 'mywebsite'

urlpatterns = [
    path("", views.index, name="index"),
    path("admin2_dashboard/", views.admin2_dashboard, name='admin2_dashboard'),
    path("add/", views.add_myweb, name='add_myweb'),
    path("logout/", views.logout_view, name='logout'),
    path("<int:id>/edit/", views.edit_myweb, name='edit_myweb'),
    path("<int:id>/delete/", views.delete_myweb, name='delete_myweb'),
]