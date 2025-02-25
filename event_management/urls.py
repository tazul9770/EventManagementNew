
from django.contrib import admin
from django.urls import path, include
from core.views import home, no_permission
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('no_permission/', no_permission, name='no-permission')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
