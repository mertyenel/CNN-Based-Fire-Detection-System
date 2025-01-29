# image_classifier/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os  # 'os' modülünü ekleyin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classifier.urls')),  # Uygulamanızın URL'lerini dahil edin
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'classifier/static'))