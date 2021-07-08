from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="dashboard_url"),
    #path('stream.mjpg', views.start_stream, name="stream"),
    path('stream.mjpg', views.start_stream, name="stream"),
    path('status', views.statusUpdate, name="statusUpdate")
]