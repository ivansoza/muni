from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group
from django.views.decorators.http import require_http_methods

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from informacion_municipal.models import Municipio, Video
from generales.models import ContadorVisitas, SocialNetwork
from servicios.forms import ServicioForm
from servicios.models import Servicio
from .forms import CustomAuthenticationForm, UserCreationWithGroupForm, UserEditForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from noticias.models import Noticia, ImagenGaleria, Categoria
from noticias.forms import NoticiaForm, ImagenGaleriaFormSet
import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from transparencia.forms import SeccionTransparenciaForm, EjercicioFiscalForm, DocumentoTransparenciaForm, ListaObligacionesForm, ArticuloLigaForm
from transparencia.models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia, ListaObligaciones, ArticuloLiga
from sevac.models import Carpeta, Archivo
from sevac.forms import CarpetaForm, ArchivoForm
# Create your views here.
from django.db.models import Count
from django.contrib.auth.models import User  # Asegúrate de importar el modelo User


from django.contrib.auth.decorators import login_required, permission_required


class VideoView(LoginRequiredMixin,TemplateView):
    template_name = 'generales/video.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('generalesDashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Video Institucional', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        context['regreso_url'] = url_configuracion 

        return context
    


class SeccionesView(LoginRequiredMixin,TemplateView):
    template_name = 'generales/secciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Secciones del Sistema', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse( 'generalesDashboard')
        context['regreso_url']= url_configuracion
        return context
    
class EncuestasView(LoginRequiredMixin,TemplateView):
    template_name = 'generales/encuestas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Encuestas', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse( 'generalesDashboard')
        context['regreso_url']= url_configuracion
        return context


class ReportesView(LoginRequiredMixin,TemplateView):
    template_name = 'generales/reportes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Reportes', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse( 'generalesDashboard')
        context['regreso_url']= url_configuracion
        return context
    
class UsuariosView(LoginRequiredMixin, TemplateView):
    template_name = 'generales/usuarios.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.has_perm('auth.add_user')):
            raise PermissionDenied  
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Generales', 'url': '/admin'},
            'child': {'name': 'Lista de Usuarios', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        context['regreso_url'] = reverse('generalesDashboard')
        # Excluir el usuario actual
        context['usuarios'] = User.objects.exclude(pk=self.request.user.pk)
        return context




class UsuarioCreateView(LoginRequiredMixin, FormView):
    template_name = 'generales/usuario_create.html'
    form_class = UserCreationWithGroupForm
    success_url = reverse_lazy('UsuariosView')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # Puedes ajustar los permisos según tu requerimiento
        if not (user.is_superuser or user.has_perm('auth.add_user')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Crear Usuario', 'url': ''}
        }
        context['sidebar'] = 'Generales'
        context['regreso_url'] = reverse('generalesDashboard')
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Usuario {user.username} creado correctamente.")
        return super().form_valid(form)
    

class UsuarioEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'generales/usuario_edit.html'
    success_url = reverse_lazy('UsuariosView')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.has_perm('auth.change_user')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el usuario que se está editando para mostrarlo en la plantilla
        context['user_to_edit'] = self.object
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Usuario', 'url': '/admin/generales/usuarios'},
            'child': {'name': 'Editar Usuario', 'url': ''}
        }
        context['regreso_url'] = reverse('UsuariosView')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"El usuario {self.object.username} ha sido actualizado correctamente.")
        return response
    

class GruposView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'grupos_view.html'  # Template para mostrar la lista de grupos en tarjetas o botones.
    context_object_name = 'groups'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # Permitir acceso si es superusuario o tiene permiso para ver, agregar o cambiar grupos.
        if not (user.is_superuser or 
                user.has_perm('auth.view_group') or 
                user.has_perm('auth.add_group') or 
                user.has_perm('auth.change_group')):
            raise PermissionDenied("No tienes permisos para ver los grupos.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Generales', 'url': '/admin/generales'},
            'child': {'name': 'Grupos', 'url': ''}
        }
        context['sidebar'] = 'Generales'
        context['regreso_url'] = reverse_lazy('generalesDashboard')
        return context
    



@login_required
@permission_required('auth.delete_group', raise_exception=True)
@require_http_methods(["DELETE"])
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_name = group.name  # Guardamos el nombre antes de eliminar
    group.delete()
    messages.success(request, f'El grupo "{group_name}" se ha eliminado con éxito.')
    # Se retorna la URL a la que redirigir tras la eliminación (por ejemplo, la vista de listado de grupos)
    return JsonResponse({'redirect': str(reverse_lazy("GruposView"))})


class UsuarioPasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'generales/usuario_change_password.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('UsuariosView')  # Ajusta el nombre de la URL según corresponda

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # Permisos: solo superusuarios o usuarios con el permiso 'auth.change_user' pueden cambiar contraseñas
        if not (user.is_superuser or user.has_perm('auth.change_user')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Obtenemos el usuario cuyo password se va a cambiar
        user_to_change = get_object_or_404(User, pk=self.kwargs['pk'])
        kwargs['user'] = user_to_change
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Usuarios', 'url': '/admin/generales/usuarios'},
            'child': {'name': 'Cambiar Contraseña', 'url': ''}
        }        
        context['regreso_url'] = reverse('UsuariosView')
        context['sidebar'] = 'Generales'

        context['user_to_change'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.save()
        user_to_change = get_object_or_404(User, pk=self.kwargs['pk'])
        messages.success(self.request, f"La contraseña del usuario {user_to_change.username} ha sido actualizada correctamente.")
        return super().form_valid(form)
    


@login_required
def toggle_user_status(request, user_id):
    # Obtener el usuario a modificar o devolver 404
    user_to_toggle = get_object_or_404(User, pk=user_id)
    
    # Evitar que el usuario se deshabilite a sí mismo
    if user_to_toggle == request.user:
        messages.error(request, "No puedes deshabilitarte a ti mismo.")
        return redirect(reverse('UsuariosView'))
    
    # Alternar el estado is_active
    user_to_toggle.is_active = not user_to_toggle.is_active
    user_to_toggle.save()
    
    # Mostrar mensaje de éxito
    if user_to_toggle.is_active:
        messages.success(request, f"El usuario {user_to_toggle.username} ha sido habilitado correctamente.")
    else:
        messages.success(request, f"El usuario {user_to_toggle.username} ha sido deshabilitado correctamente. Ya no tendrá acceso al sistema.")
    
    return redirect(reverse('UsuariosView'))

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True  # Opcional: Django redirige automáticamente si está autenticado
    success_url = reverse_lazy('dashboard')  # Redirige al dashboard después de iniciar sesión

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Redirige al dashboard si el usuario está autenticado
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = reverse_lazy('login')  # Redirige al login si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Home comisión de agua potable'}
        }
        context['sidebar'] = 'dashboard'

        try:
            # Intentar obtener el contador de visitas
            contador = ContadorVisitas.objects.get(id=1)
            context['contador_visitas'] = contador.visitas
        except ObjectDoesNotExist:
            # Si no existe, asignamos 0 como valor por defecto
            context['contador_visitas'] = 0

        return context
    

class GeneralesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'generales.html'
    login_url = reverse_lazy('login')  # Redirige al login si no está autenticado


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('dashboard')
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Generales'}
        }
        context['sidebar'] = 'Generales'
        context['regreso_url'] = url_configuracion

        return context
    
    

class PersonalizacionView(LoginRequiredMixin, TemplateView):
    template_name = "personalizacion.html"  
    login_url = reverse_lazy('login')  # Redirigir si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Personalizar', 'url': ''}
        }
        context['sidebar'] = 'perso'
        
        # Obtener todos los municipios o asignar None si no hay registros
        municipios = Municipio.objects.all()
        context['municipios'] = municipios if municipios.exists() else None
        context['regreso_url'] = url_configuracion

        return context
    

def get_municipio_data(request):
    # Se obtiene el parámetro 'id' desde la URL (si es que se envía)
    municipio_id = request.GET.get('id')
    
    try:
        if municipio_id:
            municipio = Municipio.objects.get(id=municipio_id)
        else:
            # Si no se envía id, se obtiene el primer municipio activo
            municipio = Municipio.objects.filter(status='activo').first()
    except Municipio.DoesNotExist:
        return JsonResponse({'error': 'Municipio no encontrado'}, status=404)
    
    # Se asume que existe un objeto de ColoresMunicipio relacionado
    color = municipio.colores.first()
    
    data = {
        'id': municipio.id,
        'nombre': municipio.nombre,
        'descripcion': municipio.descripcion,
        'logotipo': municipio.logotipo.url if municipio.logotipo else '',
        'banner': municipio.banner.url if municipio.banner else '',
        'ultima_actualizacion': municipio.ultima_actualizacion.isoformat(),
        'status': municipio.status,
        'colores': {
            'color_primario': color.color_primario if color else '',
            'color_secundario': color.color_secundario if color else '',
            'color_primario_dark': color.color_primario_dark if color else '',
            'color_primario_light': color.color_primario_light if color else '',
            'color_secundario_dark': color.color_secundario_dark if color else '',
            'color_secundario_light': color.color_secundario_light if color else '',
            'color_primario_rgb': color.color_primario_rgb if color else '',
            'color_secundario_rgb': color.color_secundario_rgb if color else '',
            'color_primario_dark_rgb': color.color_primario_dark_rgb if color else '',
            'color_secundario_dark_rgb': color.color_secundario_dark_rgb if color else '',
        }
    }
    return JsonResponse(data)

    

class SocialMediaView(LoginRequiredMixin, TemplateView):
    template_name = "socialmedia.html"  
    login_url = reverse_lazy('login')  # Redirigir si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Redes Sociales', 'url': ''}
        }
        context['sidebar'] = 'socialmedia'  # Cambiar a 'socialmedia' para que el sidebar refleje correctamente la sección
        context['regreso_url']= url_configuracion
        return context


from django.utils.timezone import localtime

class NewsView(LoginRequiredMixin, TemplateView):
    template_name = "noticias.html"
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NoticiaForm()
        context['imagenes_formset'] = ImagenGaleriaFormSet(queryset=ImagenGaleria.objects.none())

        noticias = Noticia.objects.all().order_by('-fecha')
        for noticia in noticias:
            noticia.fecha = localtime(noticia.fecha)

        context['noticias'] = noticias
        context['total_noticias'] = Noticia.objects.count()
        
        ultima_noticia = Noticia.objects.order_by('-fecha').first()
        if ultima_noticia:
            ultima_noticia.fecha = localtime(ultima_noticia.fecha)

        categorias = Categoria.objects.annotate(noticias_count=Count('noticias'))
        autor_destacado = Noticia.objects.values('autor').annotate(total=Count('autor')).order_by('-total').first()

        context['ultima_noticia'] = ultima_noticia
        context['categorias'] = categorias
        context['autor_destacado'] = autor_destacado

        noticia_id = self.request.GET.get('noticia_id')
        noticia = Noticia.objects.filter(id=noticia_id).first()

        if noticia:
            context['form'] = NoticiaForm(instance=noticia)
            context['imagenes_formset'] = ImagenGaleriaFormSet(queryset=noticia.imagenes_galeria.all())
        else:
            context['form'] = NoticiaForm()
            context['imagenes_formset'] = ImagenGaleriaFormSet(queryset=ImagenGaleria.objects.none())  

        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Noticias', 'url': ''}
        }
        context['sidebar'] = 'noticias'  
        context['regreso_url'] = url_configuracion 
        return context

    def post(self, request, *args, **kwargs):
        is_editing = request.POST.get('is_editing') == 'true'
        noticia_id = request.POST.get('noticia_id')

        noticia = get_object_or_404(Noticia, id=noticia_id) if is_editing and noticia_id else None

        # Si es edición, mantener la imagen principal si no se sube una nueva
        if noticia:
            form = NoticiaForm(request.POST, request.FILES, instance=noticia)
            if not request.FILES.get('imagen'):
                form.instance.imagen = noticia.imagen  
        else:
            form = NoticiaForm(request.POST, request.FILES)

        # Obtener imágenes previas asociadas a la noticia
        imagenes_previas = list(noticia.imagenes_galeria.all()) if noticia else []

        # Formset para manejar imágenes nuevas
        formset = ImagenGaleriaFormSet(request.POST, request.FILES, queryset=noticia.imagenes_galeria.all() if noticia else ImagenGaleria.objects.none())

        if form.is_valid() and formset.is_valid():
            noticia = form.save()

            imagenes_actualizadas = imagenes_previas.copy()  # Mantener todas las imágenes previas

            for i, imagen_form in enumerate(formset):
                if imagen_form.cleaned_data.get('imagen'):
                    if i < len(imagenes_previas):
                        # 🔹 Reemplazar la imagen en la misma posición
                        imagenes_actualizadas[i].imagen = imagen_form.cleaned_data['imagen']
                        imagenes_actualizadas[i].save()
                    else:
                        # 🔹 Si hay espacio, agregar la nueva imagen
                        if len(imagenes_actualizadas) < 4:
                            imagen = imagen_form.save(commit=False)
                            imagen.noticia = noticia
                            imagen.save()
                            imagenes_actualizadas.append(imagen)

            # 🔹 Asegurar que solo se mantengan las primeras 4 imágenes
            noticia.imagenes_galeria.set(imagenes_actualizadas[:4])

            return redirect('noticias_view')

        return self.get(request, *args, **kwargs)


    
def eliminar_noticia(request, noticia_id):
    if request.method == "POST":
        noticia = get_object_or_404(Noticia, id=noticia_id)

        # Eliminar imágenes asociadas en `ImagenGaleria`
        for imagen in noticia.imagenes_galeria.all():
            if imagen.imagen:
                default_storage.delete(imagen.imagen.path)  # Eliminar el archivo
            imagen.delete()  # Eliminar el registro

        # Eliminar la imagen principal de la noticia
        if noticia.imagen:
            default_storage.delete(noticia.imagen.path)

        # Eliminar la noticia
        noticia.delete()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    
    # Responder con los datos de la noticia para pre-poblar el formulario
    return JsonResponse({
        'id': noticia.id,
        'titulo': noticia.titulo,
        'contenido': noticia.contenido,
        'autor': noticia.autor,
        'categoria': noticia.categoria.id,  # Si usas un campo de relación
        'imagen': noticia.imagen.url if noticia.imagen else '',
        'imagenes_galeria': [imagen.imagen.url for imagen in noticia.imagenes_galeria.all()],
        'imagenes_galeria2': [imagen.id for imagen in noticia.imagenes_galeria.all()]

    })



@csrf_exempt
def agregar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            categoria, created = Categoria.objects.get_or_create(nombre=nombre)
            if created:
                return JsonResponse({'success': True, 'id': categoria.id, 'nombre': categoria.nombre})
            else:
                return JsonResponse({'success': False, 'error': 'La categoría ya existe.'})
    return JsonResponse({'success': False, 'error': 'Solicitud inválida'})

@csrf_exempt  # Permitir peticiones sin CSRF para subida de archivos
def custom_upload_function(request):
    if request.method == "POST" and request.FILES.get("upload"):
        upload = request.FILES["upload"]
        filename = f"{uuid.uuid4().hex}_{upload.name}"  # Genera un nombre único para el archivo
        file_path = os.path.join("media/uploads/", filename)  # Define la ruta donde se guardará el archivo
        
        # Guardar el archivo en la carpeta de "media/uploads/"
        saved_path = default_storage.save(file_path, ContentFile(upload.read()))

        # Construir la URL pública del archivo
        file_url = f"/media/{saved_path}"

        return JsonResponse({"url": file_url})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

"""
    Vistas de Servicios en el administrador
"""
class ServicesView(LoginRequiredMixin, TemplateView):
    template_name = "servicios.html"  
    login_url = reverse_lazy('login')  # Redirigir si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Servicios', 'url': ''}
        }
        context['sidebar'] = 'servicios'  # Asegura que el sidebar resalte la sección de Servicios
        context['servicios'] = Servicio.objects.all()

        return context
    
@csrf_exempt
def eliminar_servicio(request, servicio_id):
    if request.method == 'POST':
        servicio = get_object_or_404(Servicio, id=servicio_id)
        servicio.delete()
        return JsonResponse({'message': 'Servicio eliminado'}, status=200)
    return JsonResponse({'message': 'Método no permitido'}, status=405)

class ServicioCreateView(LoginRequiredMixin, CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicios/crear_servicio.html'
    success_url = reverse_lazy('servicios_view')  # Redirige al listar servicios

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_conf = reverse('servicios_view')
        context['breadcrumb'] = {
            'parent': {'name': 'Servicios', 'url': url_conf},
            'child': {'name': 'Nuevo Servicio', 'url': ''}
        }
        context['sidebar'] = 'servicios'
        return context

class ServicioUpdateView(LoginRequiredMixin, UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicios/editar_servicio.html'
    success_url = reverse_lazy('servicios_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_conf = reverse('servicios_view')
        context['breadcrumb'] = {
            'parent': {'name': 'Servicios', 'url': url_conf},
            'child': {'name': 'Editar Servicio', 'url': ''}
        }
        context['sidebar'] = 'servicios'
        return context
"""
    Terminan Vistas de Servicios en el administrador
"""

class TransparenciaView(LoginRequiredMixin, TemplateView):
    template_name = "transparencia/transparencia.html"  
    login_url = reverse_lazy('login')  # Redirigir si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Transparencia', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia

        # Obtener todas las secciones y pasarlas al contexto
        secciones = SeccionTransparencia.objects.all()
        context['secciones'] = secciones  # Agrega las secciones al contexto
        total_secciones = SeccionTransparencia.objects.count()
        total_documentos = DocumentoTransparencia.objects.count()
        ultima_documento = DocumentoTransparencia.objects.order_by('-fecha_publicacion').first()
        documentos_por_seccion = SeccionTransparencia.objects.annotate(total_docs=Count('documentos'))

        context['total_secciones'] = total_secciones
        context['total_documentos'] = total_documentos
        context['ultima_documento'] = ultima_documento
        context['documentos_por_seccion'] = documentos_por_seccion
        return context

    
def crear_seccion(request):
    # Configuración del breadcrumb y sidebar
    url_configuracion = reverse('dashboard')

    context = {
        "breadcrumb": {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Registro Sección', 'url': ''}
        },
        'sidebar': 'transparencia'
    }

    if request.method == "POST":
        form = SeccionTransparenciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sección creada correctamente.")
            return redirect("transparencia_view")  # Redirige a la vista de administración
        else:
            messages.error(request, "Error al crear la sección.")
    else:
        form = SeccionTransparenciaForm()

    # Agrega el formulario al contexto
    context['form'] = form

    return render(request, "transparencia/crear_seccion.html", context)

class SeccionTransparenciaUpdateView(UpdateView):
    model = SeccionTransparencia
    form_class = SeccionTransparenciaForm
    template_name = 'transparencia/seccion_transparencia_edit.html'
    success_url = reverse_lazy('transparencia_view')  # Redirigir a la lista tras edición

    def get_context_data(self, **kwargs):
        # Obtener el contexto base de la vista
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('transparencia_view')

        context["breadcrumb"] = {
            'parent': {'name': 'Transparencia', 'url': url_configuracion},
            'child': {'name': 'Edición de sección', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia

        return context
def eliminar_seccion(request, pk):
    seccion = get_object_or_404(SeccionTransparencia, pk=pk)
    if request.method == "POST":
        seccion.delete()
        messages.success(request, "Sección eliminada exitosamente.")
        return redirect('transparencia_view')
    
class EjercicioFiscalListView(ListView):
    model = EjercicioFiscal
    template_name = 'transparencia/ejercicio_list.html'
    context_object_name = 'ejercicios'

    def get_queryset(self):
        # Obtenemos la sección mediante la URL
        seccion_id = self.kwargs['seccion_id']
        self.seccion = get_object_or_404(SeccionTransparencia, id=seccion_id)
        # Filtramos los ejercicios fiscales de esa sección
        return EjercicioFiscal.objects.filter(seccion=self.seccion)

    def get_context_data(self, **kwargs):
        # Obtener el contexto base de la vista
        context = super().get_context_data(**kwargs)
        # Añadir más contexto adicional
        context['seccion'] = self.seccion
        context['total_ejercicios'] = self.get_queryset().count()  # Contar el número total de ejercicios
        # Puedes añadir más información si es necesario
        url_configuracion = reverse('transparencia_view')

        context["breadcrumb"] = {
            'parent': {'name': 'Transparencia', 'url': url_configuracion},
            'child': {'name': 'Ejercicios de sección', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia

        return context

class EjercicioFiscalUpdateView(UpdateView):
    model = EjercicioFiscal
    form_class = EjercicioFiscalForm
    template_name = 'transparencia/ejercicio_fiscal_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('ejercicio_list', kwargs={'seccion_id': self.object.seccion.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion'] = self.object.seccion
        url_configuracion = reverse('ejercicio_list', kwargs={'seccion_id': self.object.seccion.id})
        
        context["breadcrumb"] = {
            'parent': {'name': 'Ejercicios de sección', 'url': url_configuracion},
            'child': {'name': 'Editar Ejercicio', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia
        
        return context

def eliminar_ejercicio_fiscal(request, pk):
    ejercicio = get_object_or_404(EjercicioFiscal, pk=pk)
    seccion_id = ejercicio.seccion.id
    if request.method == "POST":
        ejercicio.delete()
        messages.success(request, "Ejercicio fiscal eliminado exitosamente.")
        return redirect('ejercicio_list', seccion_id=seccion_id)

class EjercicioFiscalCreateView(CreateView):
    model = EjercicioFiscal
    form_class = EjercicioFiscalForm
    template_name = 'transparencia/ejercicio_form.html'
    
    def form_valid(self, form):
        seccion = get_object_or_404(SeccionTransparencia, id=self.kwargs['seccion_id'])
        form.instance.seccion = seccion
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ejercicio_list', kwargs={'seccion_id': self.kwargs['seccion_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion'] = get_object_or_404(SeccionTransparencia, id=self.kwargs['seccion_id'])  # 🔹 Agregamos la sección
        url_configuracion = reverse('ejercicio_list', kwargs={'seccion_id': self.kwargs['seccion_id']})

        context["breadcrumb"] = {
            'parent': {'name': 'Ejercicios de sección', 'url': url_configuracion},
            'child': {'name': 'Crear Ejercicio', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia

        return context

class DocumentoTransparenciaListView(ListView):
    model = DocumentoTransparencia
    template_name = "transparencia/documento_list.html"
    context_object_name = "documentos"

    def get_queryset(self):
        # Obtener la sección y el ejercicio fiscal desde la URL
        seccion = get_object_or_404(SeccionTransparencia, id=self.kwargs['seccion_id'])
        ejercicio = get_object_or_404(EjercicioFiscal, id=self.kwargs['ejercicio_id'])

        # Obtener el año correctamente (si existe el campo 'año' en el modelo EjercicioFiscal)
        ejercicio_año = getattr(ejercicio, 'año', None)  # Acceder directamente al campo si existe

        # Filtrar los documentos que pertenecen a la sección y al ejercicio fiscal
        queryset = DocumentoTransparencia.objects.filter(seccion=seccion, ejercicio_fiscal=ejercicio)

        # Si hay un año en el modelo EjercicioFiscal, filtrar también por año
        if ejercicio_año:
            queryset = queryset.filter(año=ejercicio_año)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seccion"] = get_object_or_404(SeccionTransparencia, id=self.kwargs['seccion_id'])
        context["ejercicio"] = get_object_or_404(EjercicioFiscal, id=self.kwargs['ejercicio_id'])
        url_configuracion = reverse('ejercicio_list', kwargs={'seccion_id': self.kwargs['seccion_id']})

        context["breadcrumb"] = {
            'parent': {'name': 'Ejercicios de sección', 'url': url_configuracion},
            'child': {'name': 'Lista de Documentos', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia

        return context

    

def registrar_documento(request, seccion_id, ejercicio_id):
    """Vista para registrar un nuevo documento en una sección y ejercicio fiscal específicos"""
    seccion = get_object_or_404(SeccionTransparencia, id=seccion_id)
    ejercicio = get_object_or_404(EjercicioFiscal, id=ejercicio_id, seccion=seccion)  # Siempre obtenemos un ejercicio

    form = DocumentoTransparenciaForm(seccion=seccion)
    if request.method == "POST":
        form = DocumentoTransparenciaForm(request.POST, request.FILES, seccion=seccion)

        if form.is_valid():
            documento = form.save(commit=False)
            documento.seccion = seccion  # Se asigna la sección automáticamente
            documento.ejercicio_fiscal = ejercicio  # Se asigna el ejercicio fiscal
            documento.save()
            return redirect('documento_list', seccion_id=seccion.id, ejercicio_id=ejercicio.id)

    # Definir el contexto con el breadcrumb y sidebar
    context = {
        'form': form,
        'seccion': seccion,
        'ejercicio': ejercicio,
        'breadcrumb': {
            'parent': {
                'name': 'Lista de Documentos', 
                'url': reverse('documento_list', kwargs={'seccion_id': seccion.id, 'ejercicio_id': ejercicio.id})
            },
            'child': {'name': 'Registro Sección', 'url': ''}
        },
        'sidebar': 'transparencia'
    }

    return render(request, 'transparencia/documento_form.html', context)


class DocumentoTransparenciaUpdateView(UpdateView):
    model = DocumentoTransparencia
    form_class = DocumentoTransparenciaForm
    template_name = 'transparencia/documento_transparencia_edit.html'

    def get_success_url(self):
        return reverse_lazy('documento_list', kwargs={
            'seccion_id': self.object.seccion.id,
            'ejercicio_id': self.object.ejercicio_fiscal.id if self.object.ejercicio_fiscal else 0
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seccion'] = self.object.seccion
        context['ejercicio_fiscal'] = self.object.ejercicio_fiscal
        url_configuracion = reverse('documento_list', kwargs={
            'seccion_id': self.object.seccion.id,
            'ejercicio_id': self.object.ejercicio_fiscal.id if self.object.ejercicio_fiscal else 0
        })
        context["breadcrumb"] = {
            'parent': {'name': 'Documentos de sección', 'url': url_configuracion},
            'child': {'name': 'Editar Documento', 'url': ''}
        }
        context['sidebar'] = 'transparencia'
        return context
    
def eliminar_documento_transparencia(request, pk):
    documento = get_object_or_404(DocumentoTransparencia, pk=pk)
    seccion_id = documento.seccion.id
    ejercicio_id = documento.ejercicio_fiscal.id if documento.ejercicio_fiscal else 0
    if request.method == "POST":
        documento.delete()
        messages.success(request, "Documento eliminado exitosamente.")
        return redirect('documento_list', seccion_id=seccion_id, ejercicio_id=ejercicio_id)


class CrearCarpetaView(View):
    template_name = 'sevac/crear_carpeta.html'

    def get_context_data(self, **kwargs):
        context = kwargs
        padre_id = self.request.GET.get('padre')
        context['carpetas'] = Carpeta.objects.filter(estatus='A', padre=None)
        context["breadcrumb"] = {
            'parent': {'name': 'SEVAC', 'url': '/admin/lista-sevac'},
            'child': {'name': 'Registrar Carpeta', 'url': ''}
        }
        context['sidebar'] = 'sevac'

        if padre_id:
            padre = get_object_or_404(Carpeta, id=padre_id)
            context['form'] = CarpetaForm(initial={'padre': padre}, es_subcarpeta=True, padre_id=padre_id)
            context['carpeta_padre'] = padre
            context['carpeta_padre_id'] = padre.pk  # Guardar el ID de la carpeta padre en el contexto
        else:
            context['form'] = CarpetaForm(es_subcarpeta=False)
            context['carpeta_padre'] = None

        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        padre_id = request.GET.get('padre')
        if padre_id:
            form = CarpetaForm(request.POST, es_subcarpeta=True, padre_id=padre_id)
        else:
            form = CarpetaForm(request.POST, es_subcarpeta=False)

        if form.is_valid():
            carpeta = form.save(commit=False)
            if not padre_id:
                carpeta.padre = None  # Establecer como carpeta principal
            carpeta.save()

            # Redirección según el tipo de carpeta creada
            if padre_id:
                return redirect('gestionar_carpetas', carpeta_id=padre_id)  # Subcarpeta
            else:
                return redirect('listar_carpetas')  # Carpeta principal

        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

    
# Vista para editar carpeta
class EditarCarpetaView(View):
    template_name = 'sevac/editar_carpeta.html'

    def get_context_data(self, carpeta_id, **kwargs):
        context = kwargs
        carpeta = get_object_or_404(Carpeta, id=carpeta_id)

        # Añadir carpeta y formulario al contexto
        context['carpeta'] = carpeta
        context['form'] = CarpetaForm(instance=carpeta)

        # Breadcrumb y sidebar para navegación
        context["breadcrumb"] = {
            'parent': {'name': 'SEVAC', 'url': '/admin/lista-sevac'},
            'child': {'name': f'Editar Carpeta', 'url': ''}
        }
        context['sidebar'] = 'sevac'  # Resalta la sección de Transparencia en el sidebar

        # Añadir la carpeta principal a los datos del contexto
        context['carpeta_principal'] = self.get_carpeta_principal(carpeta)

        return context

    def get(self, request, carpeta_id):
        context = self.get_context_data(carpeta_id)
        return render(request, self.template_name, context)

    def post(self, request, carpeta_id):
        carpeta = get_object_or_404(Carpeta, id=carpeta_id)
        form = CarpetaForm(request.POST, instance=carpeta)
        if form.is_valid():
            form.save()
            if carpeta.padre:  # Es una subcarpeta
                # Buscar la carpeta principal (padre de todos los niveles)
                while carpeta.padre:
                    carpeta = carpeta.padre
                # Redirigir a la carpeta principal
                return redirect('gestionar_carpetas', carpeta_id=carpeta.id)

            # Redirigir según si es carpeta principal o subcarpeta
           
            else:  # Es una carpeta principal
                return redirect('listar_carpetas')  # Redirige a la lista de carpetas principales

        # Si el formulario no es válido, regresar el contexto con los errores
        context = self.get_context_data(carpeta_id, form=form)
        return render(request, self.template_name, context)

    def get_carpeta_principal(self, carpeta):
        """
        Función que recursivamente busca la carpeta principal a partir de cualquier subcarpeta.
        """
        while carpeta.padre:
            carpeta = carpeta.padre
        return carpeta


    
# Vista para subir archivos
class SubirArchivoView(View):
    template_name = 'sevac/subir_archivo.html'

    def get_context_data(self, padre_id=None, **kwargs):
        context = kwargs

        if padre_id:
            carpeta = get_object_or_404(Carpeta, id=padre_id)
            context['form'] = ArchivoForm(padre_id=padre_id)
            context['carpeta'] = carpeta  # Pasar la carpeta padre al contexto
        else:
            context['form'] = ArchivoForm()
        carpeta_principal = carpeta
        while carpeta_principal.padre:
                carpeta_principal = carpeta_principal.padre
        context['carpeta_principal'] = carpeta_principal  # Pasar la carpeta principal al contexto


        # Breadcrumb y sidebar para navegación
        context["breadcrumb"] = {
            'parent': {'name': 'Carpeta', 'url': f'/admin/gestionar-carpetas/{carpeta_principal.id}/'},
            'child': {'name': 'Subir Archivo para Carpeta', 'url': ''}
        }
        context['sidebar'] = 'sevac'  # Resalta la sección de Transparencia en el sidebar

        return context

    def get(self, request):
        padre_id = request.GET.get('carpeta')
        context = self.get_context_data(padre_id=padre_id)
        return render(request, self.template_name, context)

    def post(self, request):
        padre_id = request.GET.get('carpeta')
        if padre_id:
            form = ArchivoForm(request.POST, request.FILES, padre_id=padre_id)
        else:
            form = ArchivoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('gestionar_carpetas', carpeta_id=padre_id)  # Subcarpeta

        # Si el formulario no es válido, regresar el contexto con los errores
        context = self.get_context_data(padre_id=padre_id, form=form)
        return render(request, self.template_name, context)

class EditarArchivoView(View):
    template_name = 'sevac/editar_archivo.html'

    def get_context_data(self, archivo_id, **kwargs):
        context = kwargs
        archivo = get_object_or_404(Archivo, id=archivo_id)

        # Añadir archivo y formulario al contexto
        context['archivo'] = archivo
        context['form'] = ArchivoForm(instance=archivo)

        # Breadcrumb y sidebar para navegación
        context["breadcrumb"] = {
            'parent': {'name': 'SEVAC', 'url': '/admin/lista-sevac'},
            'child': {'name': f'Editar Archivo', 'url': ''}
        }
        context['sidebar'] = 'sevac'

        return context

    def get(self, request, archivo_id):
        context = self.get_context_data(archivo_id)
        return render(request, self.template_name, context)

    def post(self, request, archivo_id):
        archivo = get_object_or_404(Archivo, id=archivo_id)
        form = ArchivoForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()

            # Redirigir según si el archivo está en una subcarpeta dentro de una subcarpeta o no
            if archivo.carpeta.padre:  # Es un archivo dentro de subcarpeta
                carpeta_principal = self.get_carpeta_principal(archivo.carpeta)
                return redirect('gestionar_carpetas', carpeta_id=carpeta_principal.id)
            else:  # Es un archivo dentro de carpeta principal
                return redirect('listar_carpetas')  # Redirige a la lista de carpetas principales

        # Si el formulario no es válido, regresar el contexto con los errores
        context = self.get_context_data(archivo_id, form=form)
        return render(request, self.template_name, context)

    def get_carpeta_principal(self, carpeta):
        """
        Función que recursivamente busca la carpeta principal a partir de cualquier subcarpeta.
        """
        while carpeta.padre:
            carpeta = carpeta.padre
        return carpeta


    
class ListarCarpetasView(LoginRequiredMixin,TemplateView):
    template_name = 'sevac/lista_archivos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carpetas'] = Carpeta.objects.filter(padre=None)
                # Total de carpetas activas (sin subcarpetas)
        context['total_carpetas'] = Carpeta.objects.filter(estatus='A', padre=None).count()

        # Total de archivos registrados
        context['total_archivos'] = Archivo.objects.filter(estatus='A').count()

        # Última carpeta creada
        context['ultima_carpeta'] = Carpeta.objects.filter(estatus='A').order_by('-id').first()

        # Total de subcarpetas
        context['total_subcarpetas'] = Carpeta.objects.filter(estatus='A').exclude(padre=None).count()

        # Total de archivos inactivos
        context['total_archivos_inactivos'] = Archivo.objects.filter(estatus='I').count()
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'SEVAC - Carpetas y Archivos', 'url': ''}
        }
        context['sidebar'] = 'sevac'  # Asegura que el sidebar resalte la sección de Transparencia
        url_configuracion = reverse("dashboard")
        context['regreso_url'] = url_configuracion

        return context
    
class EliminarCarpetaView(View):
    def post(self, request, carpeta_id):
        carpeta = get_object_or_404(Carpeta, id=carpeta_id)
        carpeta.delete()  # Elimina la carpeta y su contenido
        return redirect('listar_carpetas')
    
# Vista para gestionar subcarpetas y archivos de una carpeta principal
class GestionarCarpetaView(View):
    template_name = 'sevac/gestionar_carpetas.html'

    def get_context_data(self, carpeta_id, **kwargs):
        context = kwargs
        carpeta = get_object_or_404(Carpeta, id=carpeta_id)
        
        # Obtener todas las subcarpetas y archivos, activos e inactivos
        subcarpetas = carpeta.subcarpetas.all().prefetch_related('archivos', 'subcarpetas__archivos')
        archivos = carpeta.archivos.all()
        
        # Añadir datos al contexto
        context['carpeta'] = carpeta
        context['subcarpetas'] = subcarpetas
        context['archivos'] = archivos
        
        # Breadcrumb y sidebar para navegación
        context["breadcrumb"] = {
            'parent': {'name': 'SEVAC', 'url': '/admin/lista-sevac'},
            'child': {'name': f'Gestionar Carpeta - {carpeta.nombre}', 'url': ''}
        }
        context['sidebar'] = 'sevac'  # Resalta la sección de Transparencia en el sidebar

        return context

    def get(self, request, carpeta_id):
        context = self.get_context_data(carpeta_id)
        return render(request, self.template_name, context)

def eliminar_archivo(request, id):
    archivo = get_object_or_404(Archivo, id=id)
    try:
        archivo.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
class ListaObligacionesView(ListView):
    model = ListaObligaciones
    template_name = 'transparencia2/inicioTrasnparencia.html'
    context_object_name = 'lista_obligaciones'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total de listas de obligaciones
        context['total_lista_obligaciones'] = ListaObligaciones.objects.count()

        # Total de artículos (registros) relacionados con las listas de obligaciones
        context['total_articulos'] = ArticuloLiga.objects.count()


        # Agregar breadcrumbs y sidebar al contexto
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Transparencia', 'url': ''}
        }
        context['sidebar'] = 'transparencia'
        context['regreso_url'] = url_configuracion

        return context

    
# Vista para crear un nuevo registro de ListaObligaciones
class ListaObligacionesCreateView(CreateView):
    model = ListaObligaciones
    form_class = ListaObligacionesForm
    template_name = 'transparencia2/crearLista.html'  # Template a usar para la vista
    success_url = reverse_lazy('lista_obligaciones')  # URL a la que redirigir después de guardar el formulario

    def form_valid(self, form):
        # Aquí puedes añadir lógica adicional antes de guardar, si lo necesitas
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('lista_obligaciones')
        context["breadcrumb"] = {
            'parent': {'name': 'Trasnparencia', 'url': url_configuracion},
            'child': {'name': 'Regitro de nueva lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia
        return context

# Vista para editar un registro de ListaObligaciones
class ListaObligacionesUpdateView(UpdateView):
    model = ListaObligaciones
    form_class = ListaObligacionesForm
    template_name = 'transparencia2/editarLista.html'  # Template a usar para la vista
    context_object_name = 'lista_obligaciones'  # Nombre del objeto que se pasará al contexto
    success_url = reverse_lazy('lista_obligaciones')  # URL a la que redirigir después de guardar el formulario

    def form_valid(self, form):
        # Aquí puedes añadir lógica adicional antes de guardar, si lo necesitas
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('lista_obligaciones')
        context["breadcrumb"] = {
            'parent': {'name': 'Trasnparencia', 'url': url_configuracion},
            'child': {'name': 'Edición de lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia
        return context

class ListaObligacionesDeleteView(View):
    def post(self, request, pk):
        # Obtener el objeto que se quiere eliminar
        lista_obligaciones = get_object_or_404(ListaObligaciones, pk=pk)

        # Eliminar el objeto
        lista_obligaciones.delete()

        # Retornar una respuesta JSON indicando que la eliminación fue exitosa
        return JsonResponse({'success': True, 'message': 'Lista de Obligación eliminada exitosamente.'})
    

class GestionarArticulosView(View):
    def get(self, request, lista_id):
        # Obtener la lista de obligaciones
        lista_obligaciones = get_object_or_404(ListaObligaciones, pk=lista_id)

        # Obtener los artículos relacionados con la lista
        articulos = lista_obligaciones.articulos_liga.all()

        # Crear el contexto con la información necesaria
        context = {
            'lista_obligaciones': lista_obligaciones,
            'articulos': articulos,
            'breadcrumb': {
                'parent': {'name': 'Transparencia', 'url': reverse('lista_obligaciones')},
                'child': {'name': 'Gestión de artículos', 'url': ''}
            },
            'sidebar': 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia
        }

        # Renderizar la plantilla con el contexto
        return render(request, 'transparencia2/gestionarLista.html', context)
            


class CrearArticuloView(CreateView):
    model = ArticuloLiga
    form_class = ArticuloLigaForm
    template_name = 'transparencia2/crearArticulo.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        lista_obligacion_id = self.kwargs.get('lista_obligacion_id')
        kwargs['lista_obligacion_id'] = lista_obligacion_id
        return kwargs
    
    def form_valid(self, form):
        # Obtener la instancia de ListaObligaciones usando el id proporcionado
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        lista_obligacion = get_object_or_404(ListaObligaciones, pk=lista_obligacion_id)

        # Asignamos la instancia de ListaObligaciones al artículo
        form.instance.lista_obligaciones = lista_obligacion

        # Guardamos el artículo y mostramos el mensaje de éxito
        response = super().form_valid(form)
        messages.success(self.request, 'Artículo creado con éxito!')
        return response

    def get_success_url(self):
        # Redirigimos al usuario a la vista de gestión de artículos después de la creación
        return reverse_lazy('gestionar_articulos', kwargs={'lista_id': self.kwargs['lista_obligacion_id']})

    def get_context_data(self, **kwargs):
        # Obtener la lista de obligaciones para pasarla al contexto
        context = super().get_context_data(**kwargs)
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        lista_obligacion = get_object_or_404(ListaObligaciones, pk=lista_obligacion_id)
        context['lista_obligaciones'] = lista_obligacion  # Pasamos el objeto lista_obligaciones
        url_configuracion = reverse('gestionar_articulos', kwargs={'lista_id': self.kwargs['lista_obligacion_id']})
        context["breadcrumb"] = {
            'parent': {'name': 'Gestión de artículos', 'url': url_configuracion},
            'child': {'name': 'Registro de articulos en lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia
        
        return context


class EditarArticuloView(UpdateView):
    model = ArticuloLiga
    form_class = ArticuloLigaForm
    template_name = 'transparencia2/editarArticulo.html'

    def get_object(self):
        # Recuperar el artículo por su ID
        articulo_id = self.kwargs['articulo_id']
        articulo = get_object_or_404(ArticuloLiga, pk=articulo_id)
        return articulo
    
    def form_valid(self, form):
        # Al enviar el formulario correctamente, mostramos un mensaje de éxito
        messages.success(self.request, 'Artículo actualizado con éxito!')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigimos al usuario a la vista de gestión de artículos después de la edición
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        return reverse_lazy('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})
    
    def get_context_data(self, **kwargs):
        # Obtener la lista de obligaciones para pasarla al contexto
        context = super().get_context_data(**kwargs)
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        lista_obligacion = get_object_or_404(ListaObligaciones, pk=lista_obligacion_id)
        context['lista_obligaciones'] = lista_obligacion  # Pasamos el objeto lista_obligaciones
        url_configuracion = reverse('gestionar_articulos', kwargs={'lista_id': self.kwargs['lista_obligacion_id']})
        context["breadcrumb"] = {
            'parent': {'name': 'Gestión de artículos', 'url': url_configuracion},
            'child': {'name': 'Editar de articulos en lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'  # Asegura que el sidebar resalte la sección de Transparencia
        return context
    

class EliminarArticuloView(View):
    def post(self, request, articulo_id):
        # Obtener el artículo que se va a eliminar
        articulo = get_object_or_404(ArticuloLiga, id=articulo_id)
        
        # Eliminar el artículo
        articulo.delete()

        # Responder con éxito
        return JsonResponse({'success': True, 'message': 'Artículo eliminado con éxito'})
    


def get_active_municipality():
    """
    Retorna el primer municipio con status='activo',
    o None si no existe.
    """
    return Municipio.objects.filter(status='activo').first()

def list_social_networks(request):
    """
    Retorna todas las redes sociales (en formato JSON) del primer municipio activo.
    Se separan en 'favoritas' y 'normales'.
    """
    municipality = get_active_municipality()
    if not municipality:
        return JsonResponse({
            'error': 'No hay municipios con estado activo.'
        }, status=400)

    # Tomamos todas las redes de ese municipio
    all_networks = SocialNetwork.objects.filter(municipio=municipality)
    
    # Separamos favoritas y normales
    favorite_networks = []
    normal_networks = []
    for net in all_networks:
        data = {
            'id': net.id,
            'type': net.social_type,
            'username': net.social_username,
            'url': net.social_url,
            'is_favorite': net.is_favorite,
        }
        if net.is_favorite:
            favorite_networks.append(data)
        else:
            normal_networks.append(data)
    
    response_data = {
        'favorites': favorite_networks,
        'normals': normal_networks
    }
    return JsonResponse(response_data, safe=False)


@require_POST
def create_social_network(request):
    """
    Crea una nueva red social para el primer municipio activo.
    Espera los campos: social_type, social_username, social_url, is_favorite (opcional).
    """
    municipality = get_active_municipality()
    if not municipality:
        return JsonResponse({
            'error': 'No hay municipios con estado activo.'
        }, status=400)

    social_type = request.POST.get('social_type')
    social_username = request.POST.get('social_username')
    social_url = request.POST.get('social_url')
    is_favorite = request.POST.get('is_favorite') == 'true'

    # Validaciones mínimas
    if not social_type:
        return JsonResponse({'error': 'El campo "social_type" es requerido.'}, status=400)
    if not social_url:
        return JsonResponse({'error': 'El campo "social_url" es requerido.'}, status=400)
    if not social_username:
        return JsonResponse({'error': 'El campo "social_username" es requerido.'}, status=400)

    # Si se va a crear como favorita, primero desmarcamos la anterior de la misma red (si existe)
    if is_favorite:
        SocialNetwork.objects.filter(
            municipio=municipality,
            social_type=social_type,
            is_favorite=True
        ).update(is_favorite=False)

    new_network = SocialNetwork.objects.create(
        municipio=municipality,
        social_type=social_type,
        social_username=social_username,
        social_url=social_url,
        is_favorite=is_favorite
    )

    # Retornar la información del objeto creado
    data = {
        'id': new_network.id,
        'type': new_network.social_type,
        'username': new_network.social_username,
        'url': new_network.social_url,
        'is_favorite': new_network.is_favorite,
    }
    return JsonResponse(data, status=201)


@require_POST
def toggle_favorite(request, pk):
    """
    Alterna si una red social es favorita o no.
    Si se marca como favorita, desmarca la anterior (de la misma red social).
    """
    # Obtener la red social
    network = get_object_or_404(SocialNetwork, pk=pk)
    municipality = network.municipio

    # Si ya es favorita, la quitamos
    if network.is_favorite:
        network.is_favorite = False
        network.save()
        return JsonResponse({
            'id': network.id,
            'type': network.social_type,
            'is_favorite': network.is_favorite
        })
    else:
        # Si no es favorita, primero desmarcamos la anterior de la misma red
        SocialNetwork.objects.filter(
            municipio=municipality,
            social_type=network.social_type,
            is_favorite=True
        ).update(is_favorite=False)

        network.is_favorite = True
        network.save()
        return JsonResponse({
            'id': network.id,
            'type': network.social_type,
            'is_favorite': network.is_favorite
        })


@require_POST
def delete_social_network(request, pk):
    """
    Elimina la red social con id=pk.
    """
    network = get_object_or_404(SocialNetwork, pk=pk)
    network.delete()
    return JsonResponse({'deleted': True})



@require_POST
def actualizar_video(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

    municipio_id = data.get('municipio_id')
    titulo = data.get('titulo', '')
    descripcion = data.get('descripcion', '')
    url_video = data.get('url_video', '')
    canal_youtube = data.get('canal_youtube', '')

    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return JsonResponse({'error': 'Municipio no encontrado.'}, status=404)

    # Actualizar o crear el objeto Video relacionado
    try:
        video = municipio.video
    except Video.DoesNotExist:
        video = Video(municipio=municipio)

    video.titulo = titulo
    video.descripcion = descripcion
    video.url_video = url_video
    video.canal_youtube = canal_youtube
    video.save()

    return JsonResponse({'success': True})