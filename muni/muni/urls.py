from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('administrador/', admin.site.urls),
    path('', include('home.urls')), 
    path('servicios/', include('servicios.urls')), 
    path('contactos/', include('contactos.urls')),  
    path('enlaces/', include('enlaces.urls')), 
    path('eventos/', include('eventos.urls')),   
    path('gobierno/', include('gobierno.urls')), 
    path('informacion/', include('informacion_municipal.urls')), 
    path('inicio/', include('inicio.urls')),  
    path('noticias/', include('noticias.urls')), 
    path('tramites/', include('tramites.urls')), 
    path('transparencia/', include('transparencia.urls')), 
    path('admin/', include('generales.urls')), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
