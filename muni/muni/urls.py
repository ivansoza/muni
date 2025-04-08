from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from home.views import mi_custom_error_400, mi_custom_error_403, mi_custom_error_404, mi_custom_error_500
urlpatterns = [
    path('administrador/', admin.site.urls),
    path('', include('home.urls')), 
    path('servicios/', include('servicios.urls')), 
    path('convocatorias/', include('convocatorias.urls')), 
    path('privacidad/', include('privacidad.urls')),  

    path('contactos/', include('contactos.urls')),  
    path('enlaces/', include('enlaces.urls')), 
    path('eventos/', include('eventos.urls')),   
    path('gobierno/', include('gobierno.urls')), 
    path('informacion/', include('informacion_municipal.urls')), 
    path('inicio/', include('inicio.urls')),  
    path('noticias/', include('noticias.urls')), 
    path('tramites/', include('tramites.urls')), 
    path('transparencia/', include('transparencia.urls')),
    path('sevac/', include('sevac.urls')),  
    path('admin/', include('generales.urls')), 
    path('usuario/', include('usuario.urls')), 

    path('ckeditor5/', include('django_ckeditor_5.urls')), 


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Manejo de errores
handler400 = mi_custom_error_400
handler403 = mi_custom_error_403
handler404 = mi_custom_error_404
handler500 = mi_custom_error_500