from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_2022_knfp/', admin.site.urls),
    path(r'', include('odontologico.urls')),
]
