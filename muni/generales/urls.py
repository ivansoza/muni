from django.urls import path, include
from .views import CustomLoginView, DashboardView, GeneralesDashboardView, NewsView, PersonalizacionView, ServicioCreateView, ServicioUpdateView,SocialMediaView,ServicesView, create_social_network, custom_upload_function, agregar_categoria, delete_social_network, eliminar_noticia, editar_noticia, list_social_networks, toggle_favorite
from django.contrib.auth.views import LogoutView
from .views import TransparenciaView, crear_seccion, EjercicioFiscalListView, EjercicioFiscalCreateView, DocumentoTransparenciaListView, registrar_documento, SeccionTransparenciaUpdateView, eliminar_seccion, EjercicioFiscalUpdateView, eliminar_ejercicio_fiscal, DocumentoTransparenciaUpdateView, eliminar_documento_transparencia
from . import views
from .views import CrearCarpetaView, SubirArchivoView, ListarCarpetasView, EditarCarpetaView, GestionarCarpetaView, EliminarCarpetaView, EditarArchivoView, eliminar_archivo
from .views import ListaObligacionesView, ListaObligacionesCreateView, ListaObligacionesUpdateView, ListaObligacionesDeleteView, GestionarArticulosView, CrearArticuloView, EditarArticuloView, EliminarArticuloView
urlpatterns = [
    path("", CustomLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),  name='logout'),      
    path('mi-panel/', DashboardView.as_view(), name='dashboard'),
    path('generales/', GeneralesDashboardView.as_view(), name='generalesDashboard'),
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



    #----------------------------------SEVAC-------------------------------------------------
    path('crear-carpeta/', CrearCarpetaView.as_view(), name='crear_carpeta'),
    path('subir-archivo/', SubirArchivoView.as_view(), name='subir_archivo'),
    path('lista-sevac/', ListarCarpetasView.as_view(), name='listar_carpetas'),
    path('editar-carpeta/<int:carpeta_id>/', EditarCarpetaView.as_view(), name='editar_carpeta'),
    path('gestionar-carpetas/<int:carpeta_id>/', GestionarCarpetaView.as_view(), name='gestionar_carpetas'),
    path('eliminar-carpeta/<int:carpeta_id>/', EliminarCarpetaView.as_view(), name='eliminar_carpeta'),
    path('editar-archivo/<int:archivo_id>/', EditarArchivoView.as_view(), name='editar_archivo'),
    path('eliminar-archivo/<int:id>/', eliminar_archivo, name='eliminar_archivo'),


    #-------------------------------TRANSPARENCIA---------------------------------------------
    path('lista-obligaciones/', ListaObligacionesView.as_view(), name='lista_obligaciones'),
    path('crear_lista_obligaciones/', ListaObligacionesCreateView.as_view(), name='crear_lista_obligaciones'),
    path('editar_lista_obligaciones/<int:pk>/', ListaObligacionesUpdateView.as_view(), name='editar_lista_obligaciones'),
    path('eliminar_lista_obligaciones/<int:pk>/', ListaObligacionesDeleteView.as_view(), name='eliminar_lista_obligaciones'),
    path('gestionar_articulos/<int:lista_id>/', GestionarArticulosView.as_view(), name='gestionar_articulos'),
    path('crear_articulo/<int:lista_obligacion_id>/', CrearArticuloView.as_view(), name='crear_articulo'),
    path('editar_articulo/<int:lista_obligacion_id>/<int:articulo_id>/', EditarArticuloView.as_view(), name='editar_articulo'),
    path('eliminar_articulo/<int:articulo_id>/', EliminarArticuloView.as_view(), name='eliminar_articulo'),


    #--------------------------------SOCIAL MEDIA ---------------------------------------------
    path('list-media/', list_social_networks, name='list_social_networks'),
    path('create-media/', create_social_network, name='create_social_network'),
    path('toggle-favorite-media/<int:pk>/', toggle_favorite, name='toggle_favorite'),
    path('delete-media/<int:pk>/', delete_social_network, name='delete_social_network'),

]