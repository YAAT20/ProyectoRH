from django.contrib import admin
from django.urls import path, include
from Preguntas.views import home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # URL para la página principal
    path('', include('Preguntas.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Esto maneja login/logout


] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
