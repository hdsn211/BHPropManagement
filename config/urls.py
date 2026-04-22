from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('properties.urls')),
    path('', include('tenants.urls')),
    path('', include('payments.urls')),
    path('', include('core.urls')),
]

#Media URLs for uploaded images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)