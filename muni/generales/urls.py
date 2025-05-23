from django.urls import path, include

from .views import AvisoDePrivacidadCreateView, AvisoDePrivacidadUpdateView, CrearCategoriaView, CrearSeccionPlusView, CustomLoginView, DashboardView, EditarRequisitoView, DetailMunicipioView, EditarSeccionPlusView, EliminarRequisitoView, EliminarSeccionPlusView, EnQueConsisteView, EncuestaDetailView, EncuestasView, GeneralesDashboardView, GestionarServicioView, GroupCreateView, GroupUpdateView, GruposView, NewsView, PersonalizacionView, PrivacidadView, ReportesView, RequisitosImagenView, RequisitosView, SeccionPlusDetailView, SeccionesNuevasView, SeccionesUpdateView, SeccionesView, ServicioCreateView, ServicioUpdateView,SocialMediaView,ServicesView, UsuarioCreateView, UsuarioEditView, UsuarioEditView, UsuarioPasswordChangeView, UsuariosView, VideoCreateView, VideoUpdateView, VideoView, VideosView, actualizar_video, crear_dependencia_ajax, create_social_network, custom_upload_function, agregar_categoria, delete_group, delete_social_network, editar_convocatoria, elemento_api, eliminar_noticia, editar_noticia, informacion_ciudad_api, list_social_networks, toggle_favorite, toggle_user_status, video_delete
from django.contrib.auth.views import LogoutView
from .views import TransparenciaView, crear_seccion, EjercicioFiscalListView, EjercicioFiscalCreateView, DocumentoTransparenciaListView, registrar_documento, SeccionTransparenciaUpdateView, eliminar_seccion, EjercicioFiscalUpdateView, eliminar_ejercicio_fiscal, DocumentoTransparenciaUpdateView, eliminar_documento_transparencia
from . import views
from .views import CrearCarpetaView, SubirArchivoView, ListarCarpetasView, EditarCarpetaView, GestionarCarpetaView, EliminarCarpetaView, EditarArchivoView, eliminar_archivo
from .views import ListaObligacionesView, ListaObligacionesCreateView, ListaObligacionesUpdateView, ListaObligacionesDeleteView, GestionarArticulosView, CrearArticuloView, EditarArticuloView, EliminarArticuloView, actualizar_orden_articulos, convocatoriaHome, filtrar_convocatorias, GestionarArticulosArView, CrearArticuloLigaView, EditarArticuloLigaArchivoView, ArticuloUpdateView
from .views import crear_noticia, HablaHome, ArticuloCreateView, eliminar_articulo

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

    #-------------------------------- SERVICIOS ----------------------------------------------
    path('servicios/', ServicesView.as_view(), name='servicios_view'),
    path('servicios/eliminar/<uuid:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('servicios/crear/', ServicioCreateView.as_view(), name='crear_servicio'),
    path('servicios/editar/<uuid:pk>/', ServicioUpdateView.as_view(), name='editar_servicio'),
    path('servicios/gestionar/<uuid:pk>/', GestionarServicioView.as_view(), name='gestionar_servicio'),
    path('servicios/<uuid:servicio_id>/consiste/', EnQueConsisteView.as_view(), name='gestionar_consiste'),
    path('servicios/<uuid:servicio_id>/requisitos/', RequisitosView.as_view(), name='gestionar_requisitos'),
    path('servicio/<uuid:servicio_id>/requisitos/<int:requisito_id>/editar/', EditarRequisitoView.as_view(), name='editar_requisito'),
    path('servicio/<uuid:servicio_id>/requisitos/<int:requisito_id>/eliminar/', EliminarRequisitoView.as_view(), name='eliminar_requisito'),
    path('servicio/<uuid:servicio_id>/requisitos-imagen/', RequisitosImagenView.as_view(), name='gestionar_requisitos_imagen'),
    path('servicios/<uuid:servicio_id>/realizo/', views.RealizoView.as_view(), name='gestionar_realizo'),
    path('servicios/<uuid:servicio_id>/realizo/<int:paso_id>/', views.RealizoView.as_view(), name='editar_realizo'),  
    path('servicios/pasos/<int:paso_id>/eliminar/', views.EliminarPasoView.as_view(), name='eliminar_paso'),
    path('servicios/<uuid:servicio_id>/costos/', views.CostosView.as_view(), name='gestionar_costos'),
    path('servicios/<uuid:servicio_id>/costos/<int:costo_id>/', views.CostosView.as_view(), name='editar_costo'),
    path('costos/<int:costo_id>/eliminar/', views.EliminarCostoView.as_view(), name='eliminar_costo'),
    path('organismo/nuevo/', crear_dependencia_ajax, name='crear_dependencia_ajax'),

    #--------------------------------GENERALES----------------------------------------------
    path('generales/', GeneralesDashboardView.as_view(), name='generalesDashboard'),
    path('generales/detalle', DetailMunicipioView.as_view(), name='DetailMunicipioView'),
    path('api/informacion-ciudad/', informacion_ciudad_api,
         name='info_ciudad_api'),
    path("api/elemento/",elemento_api,name="elemento_api"),
    path("api/elemento/<int:pk>/", elemento_api,            name="elemento_api_pk"),


    path('generales/video', VideoView.as_view(), name='VideoView'),
    path('generales/secciones', SeccionesView.as_view(), name='SeccionesView'),

    path('generales/usuarios', UsuariosView.as_view(), name='UsuariosView'),
    path('generales/privacidad', PrivacidadView.as_view(), name='PrivacidadView'),

    path('generales/reportes', ReportesView.as_view(), name='ReportesView'),
    path('actualizar_video/', actualizar_video, name='actualizar_video'),
    path('generales/usuarios/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('generales/usuarios/create/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('generales/usuarios/edit/<int:pk>/', UsuarioEditView.as_view(), name='usuario_edit'),
    path('generales/usuarios/change_password/<int:pk>/', UsuarioPasswordChangeView.as_view(), name='usuario_change_password'),
    path('generales/grupos/', GruposView.as_view(), name='GruposView'),
    path('api/grupos/<int:pk>/', delete_group, name='delete_group'),
    path('generales/grupos/nuevo/', GroupCreateView.as_view(), name='group_create'),
    path("generales/grupos/<int:pk>/editar/", GroupUpdateView.as_view(), name="GrupoEditar"),
    path('generales/secciones/habilitar/', SeccionesUpdateView.as_view(), name='secciones_update'),

    path('generales/privacidad', PrivacidadView.as_view(), name='PrivacidadView'),

    path(
        'generales/privacidad/nuevo/',
        AvisoDePrivacidadCreateView.as_view(),
        name='crear_aviso_privacidad'
    ),
    path(
        'avisos/<int:pk>/editar/',
        AvisoDePrivacidadUpdateView.as_view(),
        name='editar_aviso_privacidad'
    ),
    path('generales/secciones-nuevas', SeccionesNuevasView.as_view(), name='SeccionesNuevasView'),
    path('secciones/nueva/', CrearSeccionPlusView.as_view(), name='crear_seccion_plus'),
    path('secciones/editar/<uuid:pk>/', EditarSeccionPlusView.as_view(), name='editar_seccion_plus'),
    path('secciones/eliminar/<uuid:pk>/', EliminarSeccionPlusView.as_view(), name='eliminar_seccion_plus'),

    #----------------------------------SEVAC-------------------------------------------------
    path('crear-carpeta/', CrearCarpetaView.as_view(), name='crear_carpeta'),
    path('subir-archivo/', SubirArchivoView.as_view(), name='subir_archivo'),
    path('lista-sevac/', ListarCarpetasView.as_view(), name='listar_carpetas'),
    path('editar-carpeta/<int:carpeta_id>/', EditarCarpetaView.as_view(), name='editar_carpeta'),
    path('gestionar-carpetas/<int:carpeta_id>/', GestionarCarpetaView.as_view(), name='gestionar_carpetas'),
    path('eliminar-carpeta/<int:carpeta_id>/', EliminarCarpetaView.as_view(), name='eliminar_carpeta'),
    path('editar-archivo/<int:archivo_id>/', EditarArchivoView.as_view(), name='editar_archivo'),
    path('eliminar-archivo/<int:id>/', eliminar_archivo, name='eliminar_archivo'),
    path('sevac/categorias/nueva/', CrearCategoriaView.as_view(), name='crear_categoria'),
    path('categorias/crear/ajax/', views.crear_categoria_ajax_sevac, name='crear_categoria_ajax_sevac'),
    path('editar-categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar-categoria/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),

    #-------------------------------TRANSPARENCIA---------------------------------------------
    path('lista-obligaciones/', ListaObligacionesView.as_view(), name='lista_obligaciones'),


    path('crear_lista_obligaciones/', ListaObligacionesCreateView.as_view(), name='crear_lista_obligaciones'),

    
    path('editar_lista_obligaciones/<int:pk>/', ListaObligacionesUpdateView.as_view(), name='editar_lista_obligaciones'),
    path('eliminar_lista_obligaciones/<int:pk>/', ListaObligacionesDeleteView.as_view(), name='eliminar_lista_obligaciones'),
    path('gestionar_articulos/<int:lista_id>/', GestionarArticulosView.as_view(), name='gestionar_articulos'),
    path('crear_articulo/<int:lista_obligacion_id>/', CrearArticuloView.as_view(), name='crear_articulo'),
    path('editar_articulo/<int:lista_obligacion_id>/<int:articulo_id>/', EditarArticuloView.as_view(), name='editar_articulo'),
    path('eliminar_articulo/<int:articulo_id>/', EliminarArticuloView.as_view(), name='eliminar_articulo'),
    path('actualizar_orden/', actualizar_orden_articulos, name='actualizar_orden'),
    path('gestionar_articulo_la/<int:id>/', GestionarArticulosArView.as_view(), name='gestionarArchivoLa'),
    path('crear_articulo_liga/<int:id>/', CrearArticuloLigaView.as_view(), name='crear_articulo_liga'),
    path('editar_articulo_liga/<int:pk>/', EditarArticuloLigaArchivoView.as_view(), name='editar_articulo_liga'),
    path('eliminar_articulo_liga/<int:articulo_id>/', views.eliminar_articulo_liga, name='eliminar_articulo_liga'),


    #--------------------------------SOCIAL MEDIA ---------------------------------------------
    path('list-media/', list_social_networks, name='list_social_networks'),
    path('create-media/', create_social_network, name='create_social_network'),
    path('toggle-favorite-media/<int:pk>/', toggle_favorite, name='toggle_favorite'),
    path('delete-media/<int:pk>/', delete_social_network, name='delete_social_network'),


    #---------------------------------- CONVOCATORIAS ---------------------------------
    path('convocatorias/', convocatoriaHome.as_view(), name='convocatorias'),
    path('filtrar/', filtrar_convocatorias, name='filtrar_convocatorias'),
    path('convocatorias/nueva/', views.crear_convocatoria, name='crear_convocatoria'),
    path('convocatorias/editar/<int:pk>/', editar_convocatoria, name='editar_convocatoria'),

    path('crear-categoria/', views.crear_categoria_ajax, name='crear_categoria_ajax'),
    path('convocatorias/<int:id>/eliminar/', views.eliminar_convocatoria, name='eliminarConvocatoria'),
    path('convocatorias/<int:id>/detalle/', views.obtener_detalle_convocatoria, name='detalle_Convocatoria'),

    path('aviso/<int:pk>/eliminar/', views.eliminar_aviso_privacidad, name='eliminar_aviso_privacidad'),


    #---------------------------------  ENCUESTAS ----------------------------------------
    path('generales/encuestas', EncuestasView.as_view(), name='EncuestasView'),

    path('encuestas/create-ajax/', views.encuesta_create_ajax, name='encuesta_create_ajax'),
    path('encuestas/<int:pk>/eliminar/', views.encuesta_eliminar, name='encuesta_eliminar'),
    path('encuestas/<int:encuesta_id>/editar/', views.encuesta_update_ajax, name='encuesta_update_ajax'),
    path('encuesta/<int:pk>/', EncuestaDetailView.as_view(), name='encuesta_view'),
    path(
        "encuestas/<int:encuesta_id>/toggle/",
        views.encuesta_toggle_estado,
        name="encuesta_toggle_estado",
    ),
    
    #--------------------------Nuevas Noticias---------------------------------
    path('crear_noticia/', crear_noticia, name='crear_noticia'),
    path('edicion_noticia/<int:pk>/', views.editar_noticia_nueva, name='edicion_noticia'),

    #--------------------------Videos---------------------------------
    path('videos/', VideosView.as_view(), name='videos'),
    path('videos/nuevo/', VideoCreateView.as_view(), name='video_add'),
    path('videos/<int:pk>/editar/', VideoUpdateView.as_view(), name='video_edit'),
    path('videos/<int:pk>/eliminar/', video_delete, name='video_delete'),




#----------------------- Habla con tus hijos ------------------------------
    path('habla_home/', HablaHome.as_view(), name='habla_home'),
    path('registro_articulo/', ArticuloCreateView.as_view(), name='registro_articulo'),
    path('agregar_categoria_habla/', views.agregar_categoria_habla, name='agregar_categoria_habla'),
    path('agregar_autor/', views.agregar_autor, name='agregar_autor'),
    path('articulo_editar/<int:pk>/', ArticuloUpdateView.as_view(), name='articulo_editar'),

    path('articulo_eliminar/<int:pk>/', eliminar_articulo, name='eliminar_articulo'),



]