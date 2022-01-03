from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nmap.urls')),
    path('submit/', include('nmap.urls')),
    path('api/scans/', include('nmap.urls')),
]

urlpatterns += staticfiles_urlpatterns()