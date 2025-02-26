from django.urls import path, include
from .views import CustomLoginView, DashboardView, NewsView, PersonalizacionView, ServicioCreateView, ServicioUpdateView,SocialMediaView,ServicesView, custom_upload_function, agregar_categoria, eliminar_noticia, editar_noticia
from django.contrib.auth.views import LogoutView
from .views import TransparenciaView, crear_seccion, EjercicioFiscalListView, EjercicioFiscalCreateView, DocumentoTransparenciaListView, registrar_documento, SeccionTransparenciaUpdateView, eliminar_seccion, EjercicioFiscalUpdateView, eliminar_ejercicio_fiscal, DocumentoTransparenciaUpdateView, eliminar_documento_transparencia
from . import views

urlpatterns = [
    path("", CustomLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),  name='logout'),      
    path('mi-panel/', DashboardView.as_view(), name='dashboard'),
    path('personalizacion/', PersonalizacionView.as_view(), name='personalizacion_view'),
    path('social-media/', SocialMediaView.as_view(), name='social_view'),
    path('noticias/', NewsView.as_view(), name='noticias_view'),
    path("upload/", custom_upload_function, name="custom_upload_file"),
    path('agregar-categoria/', agregar_categoria, name='agregar_categoria'),
    path('editar-noticia/<int:noticia_id>/', editar_noticia, name='editar_noticia'),
    path('eliminar-noticia/<int:noticia_id>/', eliminar_noticia, name='eliminar_noticia'),
    path('transparencia/', TransparenciaView.as_view(), name='transparencia_view'),
    path('crear/', crear_seccion, name='crear_seccion'),
    path('ejercicios/<int:seccion_id>/', EjercicioFiscalListView.as_view(), name='ejercicio_list'),
    path('nuevo_ejercicio/<int:seccion_id>/', EjercicioFiscalCreateView.as_view(), name='ejercicio_create'),
    path('documentos/<int:seccion_id>/<int:ejercicio_id>/', DocumentoTransparenciaListView.as_view(), name="documento_list"),
    path('documento_nuevo/<int:seccion_id>/<int:ejercicio_id>/', registrar_documento, name='documento_nuevo'),
    path('editar_seccion/<int:pk>/', SeccionTransparenciaUpdateView.as_view(), name='editar_seccion'),
    path('eliminar_seccion/<int:pk>/', eliminar_seccion, name='eliminar_seccion'),
    path('editar_ejercicio/<int:pk>/', EjercicioFiscalUpdateView.as_view(), name='editar_ejercicio'),
    path('eliminar_ejercicio/<int:pk>/', eliminar_ejercicio_fiscal, name='eliminar_ejercicio'),
    path('editar_documento/<int:pk>/', DocumentoTransparenciaUpdateView.as_view(), name='editar_documento_transparencia'),
    path('eliminar_documento/<int:pk>/', eliminar_documento_transparencia, name='eliminar_documento_transparencia'),
    
    path('servicios/', ServicesView.as_view(), name='servicios_view'),
    path('servicios/eliminar/<uuid:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('servicios/crear/', ServicioCreateView.as_view(), name='crear_servicio'),
    path('servicios/editar/<uuid:pk>/', ServicioUpdateView.as_view(), name='editar_servicio'),
]