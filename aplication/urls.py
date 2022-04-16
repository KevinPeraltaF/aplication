from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_2022_knfp/', admin.site.urls),
    path(r'', include('odontologico.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
