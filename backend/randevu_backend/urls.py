from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('randevu_app.urls')),
]

# Medya dosyalarını servis etmek için
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Geliştirme ortamında statik dosyaları servis et
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)