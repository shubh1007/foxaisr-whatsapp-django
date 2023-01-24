from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('whatsapp/', include('whatsapp.urls')),
    path('messenger/', include('messenger.urls')),
]
