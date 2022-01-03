from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='nmap'),
    path('submit/', views.submitNmap, name='submit'),
    path('api/scans/', views.getHostScansAsJson, name='api/scans/')
]