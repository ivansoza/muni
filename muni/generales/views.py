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
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from .mixins import SuperuserOrReportPermissionMixin

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from django.http import JsonResponse, HttpResponseNotAllowed

from informacion_municipal.models import ElementoLista, InformacionCiudad, Municipio, Video
from generales.models import ContadorVisitas, SeccionPlus, Secciones, SocialNetwork, VideoMunicipio
from reportes.models import ReporteStatus
from privacidad.forms import ArchivoRelacionadoForm, ArchivoRelacionadoFormSet, AvisoDePrivacidadForm
from privacidad.models import ArchivoRelacionado, AvisoDePrivacidad
from servicios.forms import ComoLoRealizoForm, CuantoCuestaForm, EnQueConsisteForm, QueSeRequiereForm, RequisitosImagenForm, ServicioForm
from servicios.models import ComoLoRealizo, ConfiguracionServicio, CuantoCuesta, Dependencia, EnQueConsiste, QueSeRequiere, RequisitosImagen, Servicio
from .forms import CustomAuthenticationForm, ElementoListaForm, GroupForm, InformacionCiudadForm, SeccionPlusForm, SeccionesForm, UserCreationWithGroupForm, UserEditForm, VideoMunicipioForm
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
from transparencia.forms import SeccionTransparenciaForm, EjercicioFiscalForm, DocumentoTransparenciaForm, ListaObligacionesForm, ArticuloLigaForm, ArticuloLigaArchivoForm
from transparencia.models import Encuesta, Opcion, Pregunta, Respuesta, SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia, ListaObligaciones, ArticuloLiga, LigaArchivo
from sevac.models import Carpeta, Archivo, CategoriaSevac
from sevac.forms import CarpetaForm, ArchivoForm, CategoriaSevacForm
# Create your views here.
from django.db.models import Count
from django.db import models
from convocatorias.models import Categoria as CategoriaConvocatoria, Convocatoria, ArchivoConvocatoria

from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from convocatorias.forms import ArchivoConvocatoriaForm, ConvocatoriaForm, ArchivoConvocatoriaFormSet
from django.contrib.auth.models import User  # Asegúrate de importar el modelo User
from django.views.generic import DetailView


from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission

from django.contrib.auth.mixins import  PermissionRequiredMixin
from noticias.forms import ImagenGaleriaForm

from eventos.models import Articulo, Categoria as CategoriaHabla, Autor
from eventos.forms import ArticuloForm

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
    






class ReportesView(LoginRequiredMixin,
                   SuperuserOrReportPermissionMixin,
                   TemplateView):
    template_name = "generales/reportes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            "parent": {"name": "Generales", "url": "/admin/generales/"},
            "child": {"name": "Reportes",  "url": ""},
        }
        context["sidebar"]    = "Generales"
        context["regreso_url"] = reverse("generalesDashboard")

        defaults = {
            "reporte_agua_status":         False,
            "reporte_bache_status":        False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status":    False,
        }
        reporte_status, _ = ReporteStatus.objects.get_or_create(
            pk=1, defaults=defaults
        )
        context["reporte_status"] = reporte_status
        return context
    


    
class DetailMunicipioView(LoginRequiredMixin,TemplateView):
    template_name = 'detalle/detalle.html'


    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.has_perm('auth.add_user')):
            raise PermissionDenied  
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Generales', 'url': '/admin'},
            'child': {'name': 'Detalles de Municipio', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse( 'generalesDashboard')
        context['regreso_url']= url_configuracion
        return context
    
@login_required
@require_http_methods(["GET", "POST"])
def informacion_ciudad_api(request):
    """
    Endpoint JSON-only para la ficha de InformaciónCiudad.
    - Selecciona el primer Municipio con status='activo'.
    - Si no hay municipios activos → 404.
    - GET  → devuelve datos.
    - POST → actualiza (lema, título, etc.).
    """
    municipio = (
        Municipio.objects
        .filter(status="activo")
        .order_by("id")
        .first()
    )

    if municipio is None:
        return JsonResponse(
            {"detail": "No hay ningún Municipio con estatus 'activo'."},
            status=404
        )

    # ficha vinculada a ese municipio
    info, _ = InformacionCiudad.objects.get_or_create(municipio=municipio)

    if request.method == "GET":
        data = {
            "id":               info.id,
            "municipio":        municipio.nombre,         # ← nombre del municipio activo
            "lema":             info.lema,
            "titulo":           info.titulo,
            "subtitulo":        info.subtitulo,
            "encabezado_lista": info.encabezado_lista,
            "elementos": list(info.elementos.values("id", "texto")),
        }
        return JsonResponse(data, status=200)

    # --- POST → actualizar ----------------------------------------------
    payload = json.loads(request.body or "{}")
    form = InformacionCiudadForm(payload, instance=info)
    if form.is_valid():
        form.save()
        return JsonResponse(
            {"detail": "Información actualizada con éxito."},
            status=200
        )
    return JsonResponse({"errors": form.errors}, status=400)
@login_required
@csrf_exempt
def elemento_api(request, pk=None):
    """
    Crear, actualizar o eliminar un ElementoLista:
      • POST    /elemento/          → crear
      • PATCH   /elemento/<pk>/     → actualizar
      • DELETE  /elemento/<pk>/     → eliminar
    Siempre trabaja con el primer Municipio activo.
    """
    # 1️⃣ Obtener el primer Municipio activo
    municipio = Municipio.objects.filter(status="activo").order_by("id").first()
    if not municipio:
        return JsonResponse(
            {"detail": "No hay ningún Municipio con estatus 'activo'."},
            status=404
        )

    # 2️⃣ Asegurar la existencia de la ficha de InfoCiudad
    info, _ = InformacionCiudad.objects.get_or_create(municipio=municipio)

    # 3️⃣ CREAR (POST sin pk)
    if request.method == "POST" and pk is None:
        payload = json.loads(request.body or "{}")
        form = ElementoListaForm(payload)
        if form.is_valid():
            elemento = form.save(commit=False)
            elemento.informacion = info
            elemento.save()
            return JsonResponse({"id": elemento.id, "texto": elemento.texto}, status=201)
        return JsonResponse({"errors": form.errors}, status=400)

    # 4️⃣ A partir de aquí, necesitamos un pk válido
    elemento = get_object_or_404(
        ElementoLista,
        pk=pk,
        informacion__municipio=municipio
    )

    # 5️⃣ ACTUALIZAR (PATCH)
    if request.method == "PATCH":
        payload = json.loads(request.body or "{}")
        # ❌ NO usar partial=True aquí
        form = ElementoListaForm(payload, instance=elemento)
        if form.is_valid():
            form.save()
            return JsonResponse({"detail": "Elemento actualizado."}, status=200)
        return JsonResponse({"errors": form.errors}, status=400)

    # 6️⃣ ELIMINAR (DELETE)
    if request.method == "DELETE":
        elemento.delete()
        return JsonResponse({"detail": "Elemento eliminado."}, status=204)

    # 7️⃣ Métodos no permitidos
    return HttpResponseNotAllowed(["POST", "PATCH", "DELETE"])
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





class PrivacidadView(LoginRequiredMixin, TemplateView):
    template_name = 'generales/privacidad.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Generales', 'url': '/admin/generales/'},
            'child': {'name': 'Avisos de Privacidad', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        context['regreso_url'] = reverse('generalesDashboard')
        return context
    

class AvisoDePrivacidadCreateView(LoginRequiredMixin, CreateView):
    model = AvisoDePrivacidad
    form_class = AvisoDePrivacidadForm
    template_name = 'generales/privacidadAdmin.html'
    success_url = reverse_lazy('PrivacidadView')   # cambia por tu url real

    # ---------- contexto ----------
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # formset: usa POST cuando volvemos con errores
        if self.request.method == 'POST':
            ctx['formset'] = ArchivoRelacionadoFormSet(
                self.request.POST, self.request.FILES)
        else:
            ctx['formset'] = ArchivoRelacionadoFormSet()

        # lo que ya tenías en tu TemplateView
        ctx["breadcrumb"] = {
            'parent': {'name': 'Avisos de Privacidad', 'url': reverse('PrivacidadView')},
            'child':  {'name': 'Crear Aviso de Privacidad', 'url': ''},
        }
        ctx['sidebar'] = 'Generales'
        ctx['regreso_url'] = reverse('PrivacidadView')
        return ctx

    # ---------- guardado ----------
    def form_valid(self, form):
        # 1) Buscar municipio activo
        municipio_activo = Municipio.objects.filter(status='activo').first()
        if not municipio_activo:
            form.add_error(
                None,
                'Aún no se ha creado un municipio con estado "activo".'
            )
            return self.form_invalid(form)

        # 2) Construir formset
        ctx = self.get_context_data()
        formset = ctx['formset']

        # 3) Validar todo junto
        if formset.is_valid():
            # guardar aviso
            form.instance.municipio = municipio_activo
            self.object = form.save()

            # ligar formset al aviso recién creado
            formset.instance = self.object
            formset.save()

            messages.success(self.request, 'Aviso de privacidad creado correctamente.')
            return redirect(self.get_success_url())

        # si el formset falla volvemos a la plantilla
        return self.render_to_response(self.get_context_data(form=form))
    


class AvisoDePrivacidadUpdateView(LoginRequiredMixin, UpdateView):
    model = AvisoDePrivacidad
    form_class = AvisoDePrivacidadForm
    template_name = 'generales/privacidadAdminEdit.html'
    success_url = reverse_lazy('PrivacidadView')  # Ajusta a tu URL correspondiente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si existen archivos, no mostramos formularios extra (extra=0), de lo contrario, mostramos 1 formulario extra
        extra_value = 0 if self.object.archivos_relacionados.exists() else 1

        # Configuramos el inline formset con can_delete=True para permitir la eliminación
        ArchivoRelacionadoFormSetDynamic = inlineformset_factory(
            AvisoDePrivacidad,
            ArchivoRelacionado,
            form=ArchivoRelacionadoForm,
            extra=extra_value,
            can_delete=True
        )

        if self.request.method == 'POST':
            formset = ArchivoRelacionadoFormSetDynamic(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            formset = ArchivoRelacionadoFormSetDynamic(instance=self.object)

        context['formset'] = formset

        # Contexto adicional (breadcrumbs, sidebar, url de regreso)
        context["breadcrumb"] = {
            'parent': {'name': 'Avisos de Privacidad', 'url': reverse('PrivacidadView')},
            'child':  {'name': 'Editar aviso de Privacidad', 'url': ''},
        }
        context['sidebar'] = 'Generales'
        context['regreso_url'] = reverse('PrivacidadView')
        return context

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Aviso de privacidad actualizado correctamente.')
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))

class SeccionesView(LoginRequiredMixin, TemplateView):
    template_name = 'generales/secciones.html'
    
    # --- control de permisos ---
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("generales.view_secciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    # --- breadcrumbs, sidebar, etc. ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Dashboard", "url": "/admin"},
            "child": {"name": "Secciones del Sistema", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("generalesDashboard")
        return context
    
class SeccionesNuevasView(LoginRequiredMixin, TemplateView):
    template_name = 'generales/seccionesNuevas.html'
    
    # --- control de permisos ---
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("generales.view_secciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    # --- breadcrumbs, sidebar, etc. ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Generales", "url": "/admin/generales/"},
            "child": {"name": "Secciones Extras del Sistema", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("generalesDashboard")

        # Consulta desde el modelo
        context["secciones"] = SeccionPlus.objects.filter(status=True)

        return context
    
class CrearSeccionPlusView(LoginRequiredMixin, CreateView):
    model = SeccionPlus
    form_class = SeccionPlusForm
    template_name = 'secciones/crear_seccion.html'
    success_url = reverse_lazy('SeccionesNuevasView')  # O el nombre de la vista principal

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("generales.add_seccionplus")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        municipio_activo = Municipio.objects.filter(status='activo').first()
        if municipio_activo:
            form.instance.municipio = municipio_activo
        else:
            form.add_error(None, "No hay un municipio activo disponible.")
            return self.form_invalid(form)
        return super().form_valid(form)
    
class EditarSeccionPlusView(LoginRequiredMixin, UpdateView):
    model = SeccionPlus
    form_class = SeccionPlusForm
    template_name = 'secciones/crear_seccion.html'  # usamos la misma
    success_url = reverse_lazy('SeccionesNuevasView')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("generales.change_seccionplus")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # El municipio ya está asignado en la instancia existente, no es necesario modificarlo
        return super().form_valid(form)
    
class EliminarSeccionPlusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not (request.user.is_superuser or request.user.has_perm("generales.delete_seccionplus")):
            raise PermissionDenied

        seccion = get_object_or_404(SeccionPlus, pk=pk)
        seccion.delete()
        messages.success(request, f"La sección '{seccion.nombre}' ha sido eliminada.")
        return redirect('SeccionesNuevasView')
    
class SeccionesUpdateView(LoginRequiredMixin, UpdateView):
    model = Secciones
    form_class = SeccionesForm
    template_name = 'generales/secciones_update.html'
    success_url = reverse_lazy('secciones_update')

    # --- control de permisos ---
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("generales.change_secciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    # --- obtenemos (o creamos) el objeto de secciones del municipio activo ---
    def get_object(self, queryset=None):
        try:
            municipio = Municipio.objects.get(status='activo')
        except Municipio.DoesNotExist:
            messages.warning(self.request, "No se ha agregado un municipio activo.")
            return None
        # Si no existe la instancia de Secciones para el municipio activo, se crea.
        obj, created = Secciones.objects.get_or_create(municipio=municipio)
        return obj

    # --- si no existe municipio activo se redirige ---
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect('generalesDashboard')
        return super().get(request, *args, **kwargs)

    # --- mensaje de éxito al guardar cambios ---
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Secciones actualizadas correctamente.")
        return response

    # --- breadcrumbs, sidebar, etc. ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Generales", "url": "/admin/generales/"},
            "child": {"name": "Habilitar/Inhabilitar Secciones", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse_lazy("generalesDashboard")
        return context
    

class UsuarioCreateView(LoginRequiredMixin, FormView):
    template_name = "generales/usuario_create.html"
    form_class = UserCreationWithGroupForm
    success_url = reverse_lazy("UsuariosView")

    # --- control de permisos ---
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("auth.add_user")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    # --- breadcrumbs, sidebar, etc. ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Lista de Usuarios", "url": "/admin/generales/usuarios"},
            "child": {"name": "Crear Usuario", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse_lazy("UsuariosView")
        return context

    # --- guardado y mensaje de éxito ---
    def form_valid(self, form):
        self.object = form.save()  # <‑‑ el usuario recién creado
        messages.success(
            self.request,
            f"Usuario {self.object.username} creado correctamente."
        )
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
        context["sidebar"] = "Generales"

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
    login_url = reverse_lazy('login') 


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
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("noticias.add_noticia")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        imagenes_formset = ImagenGaleriaFormSet(request.POST, request.FILES, queryset=ImagenGaleria.objects.none())

        if form.is_valid() and imagenes_formset.is_valid():
            noticia = form.save()
            for form_img in imagenes_formset:
                if form_img.cleaned_data:
                    imagen = form_img.save(commit=False)
                    imagen.noticia = noticia
                    imagen.save()
            return redirect('noticias_view')
    else:
        form = NoticiaForm()
        imagenes_formset = ImagenGaleriaFormSet(queryset=ImagenGaleria.objects.none())

    # Aquí se arma el contexto adicional
    url_configuracion = reverse('noticias_view')
    context = {
        'form': form,
        'imagenes_formset': imagenes_formset,
        'breadcrumb': {
            'parent': {'name': 'Noticias', 'url': url_configuracion},
            'child': {'name': 'Registro de noticia', 'url': ''}
        },
        'sidebar': 'noticias',
        'regreso_url': url_configuracion
    }

    return render(request, 'crear_noticia.html', context)


def editar_noticia_nueva(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    form = NoticiaForm(request.POST or None, request.FILES or None, instance=noticia)

    ImagenGaleriaFormSet = modelformset_factory(
        ImagenGaleria,
        form=ImagenGaleriaForm,
        extra=0,
        can_delete=True
    )

    formset = ImagenGaleriaFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=ImagenGaleria.objects.filter(noticia=noticia)
    )

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            noticia = form.save()

            for f in formset:
                if f.cleaned_data.get('DELETE'):
                    f.instance.delete()
                elif f.has_changed():
                    imagen = f.save(commit=False)
                    imagen.noticia = noticia
                    imagen.save()

            return redirect('noticias_view')
        else:
            print("Errores del form:", form.errors)
            print("Errores del formset:", formset.errors)

    # Agregamos el contexto extra para breadcrumb, sidebar y regreso
    url_configuracion = reverse('noticias_view')
    context = {
        'form': form,
        'formset': formset,
        'noticia': noticia,
        'breadcrumb': {
            'parent': {'name': 'Noticias', 'url': url_configuracion},
            'child': {'name': 'Editar noticia', 'url': ''}
        },
        'sidebar': 'noticias',
        'regreso_url': url_configuracion
    }

    return render(request, 'editar_noticia.html', context)


    
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
        context['regreso_url'] = url_configuracion

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
    
class GestionarServicioView(TemplateView):
    template_name = "servicios/gestionar_servicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = Servicio.objects.get(pk=kwargs['pk'])
        consiste = EnQueConsiste.objects.filter(servicio=servicio).first()
        requisitos = QueSeRequiere.objects.filter(servicio=servicio)
        instrucciones_queryset = ComoLoRealizo.objects.filter(servicio=servicio).order_by('canal_presentacion__nombre', 'paso')
        costos = CuantoCuesta.objects.filter(servicio=servicio)
        instrucciones = {
            'linea': instrucciones_queryset.filter(canal_presentacion__nombre='linea'),
            'presencial': instrucciones_queryset.filter(canal_presentacion__nombre='presencial')
        }

        breadcrumb = {
            'parent': {'name': 'Servicios', 'url': reverse('servicios_view')},
            'child': {'name': 'Gestión de servicio', 'url': ''},
        }

        context.update({
            'sidebar': 'servicios',
            'breadcrumb': breadcrumb,
            'servicio': servicio,
            'consiste': consiste,
            'requisitos': requisitos,
            'instrucciones': instrucciones,
            'costos': costos
        })

        # ✅ Agrega esta línea para activar el botón condicional
        config = ConfiguracionServicio.objects.first()
        context['usar_requisitos_v2'] = config.usar_requisitos_v2 if config else False
        
        return context
    
class EnQueConsisteView(View):
    def get(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        consiste = EnQueConsiste.objects.filter(servicio=servicio).first()
        form = EnQueConsisteForm(instance=consiste)

        breadcrumb = {
            'parent': {'name': 'Gestión De Servicio', 'url': reverse('gestionar_servicio', kwargs={'pk': servicio.id})},
            'child': {'name': 'Sección: ¿En qué consiste?', 'url': ''},
        }

        context = {
            'form': form,
            'servicio': servicio,
            'consiste': consiste,
            'breadcrumb': breadcrumb,
            'sidebar': 'servicios',
        }
        return render(request, 'servicios/consiste_form.html', context)

    def post(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        try:
            consiste = EnQueConsiste.objects.get(servicio=servicio)
            form = EnQueConsisteForm(request.POST, instance=consiste)
        except EnQueConsiste.DoesNotExist:
            form = EnQueConsisteForm(request.POST)

        if form.is_valid():
            consiste = form.save(commit=False)
            consiste.servicio = servicio
            consiste.save()
            return redirect('gestionar_servicio', pk=servicio.id )
        
        breadcrumb = {
            'parent': {'name': 'Servicios', 'url': reverse('gestionar_servicio', kwargs={'pk': servicio.id})},
            'child': {'name': 'Sección: ¿En qué consiste?', 'url': ''},
        }

        context = {
            'form': form,
            'servicio': servicio,
            'consiste': consiste,
            'breadcrumb': breadcrumb,
            'sidebar': 'servicios',
        }
        
        return render(request, 'servicios/consiste_form.html', context)
    
class RequisitosView(View):
    def get(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        requisitos = QueSeRequiere.objects.filter(servicio=servicio)
        form = QueSeRequiereForm()

        breadcrumb = {
            'parent': {'name': 'Gestión De Servicio', 'url': reverse('gestionar_servicio', kwargs={'pk': servicio.id})},
            'child': {'name': 'Sección: ¿Qué se requiere?', 'url': ''},
        }

        context = {
            'form': form,
            'servicio': servicio,
            'requisitos': requisitos,
            'breadcrumb': breadcrumb,
            'sidebar': 'servicios',
        }
        return render(request, 'servicios/requisitos_form.html', context)

    def post(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        form = QueSeRequiereForm(request.POST, request.FILES)
        if form.is_valid():
            requisito = form.save(commit=False)
            requisito.servicio = servicio
            requisito.save()
            return redirect('gestionar_requisitos', servicio_id=servicio.id)
        requisitos = QueSeRequiere.objects.filter(servicio=servicio)
        return render(request, 'servicios/requisitos_form.html', {
            'servicio': servicio,
            'requisitos': requisitos,
            'form': form
        })
    
class EditarRequisitoView(View):
    def get(self, request, servicio_id, requisito_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        requisito = get_object_or_404(QueSeRequiere, id=requisito_id, servicio=servicio)
        form = QueSeRequiereForm(instance=requisito)
        return render(request, 'servicios/requisitos_form.html', {
            'servicio': servicio,
            'form': form,
            'requisitos': QueSeRequiere.objects.filter(servicio=servicio),
            'modo_edicion': True,
            'requisito_id': requisito.id
        })

    def post(self, request, servicio_id, requisito_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        requisito = get_object_or_404(QueSeRequiere, id=requisito_id, servicio=servicio)
        form = QueSeRequiereForm(request.POST, request.FILES, instance=requisito)
        if form.is_valid():
            form.save()
            return redirect('gestionar_requisitos', servicio_id=servicio.id)
        return render(request, 'servicios/requisitos_form.html', {
            'servicio': servicio,
            'form': form,
            'requisitos': QueSeRequiere.objects.filter(servicio=servicio),
            'modo_edicion': True,
            'requisito_id': requisito.id
        })
    
class EliminarRequisitoView(View):
    def post(self, request, servicio_id, requisito_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        requisito = get_object_or_404(QueSeRequiere, id=requisito_id, servicio=servicio)
        requisito.delete()
        return redirect('gestionar_requisitos', servicio_id=servicio.id)
    
class RequisitosImagenView(View):
    def get(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        form, created = RequisitosImagen.objects.get_or_create(servicio=servicio)
        form = RequisitosImagenForm(instance=form)
        return render(request, 'servicios/requisitos_imagen_form.html', {
            'form': form,
            'servicio': servicio
        })

    def post(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        instancia, _ = RequisitosImagen.objects.get_or_create(servicio=servicio)
        form = RequisitosImagenForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('gestionar_servicio', pk=servicio.id)
        return render(request, 'servicios/requisitos_imagen_form.html', {
            'form': form,
            'servicio': servicio
        })

    
class RealizoView(View):
    def get(self, request, servicio_id, paso_id=None):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        if paso_id:
            paso = get_object_or_404(ComoLoRealizo, id=paso_id)
            form = ComoLoRealizoForm(instance=paso)
        else:
            form = ComoLoRealizoForm()
        pasos = ComoLoRealizo.objects.filter(servicio=servicio).order_by('canal_presentacion', 'paso')
        return render(request, 'servicios/realizo_form.html', {
            'servicio': servicio,
            'form': form,
            'pasos': pasos,
            'paso_id': paso_id,
        })

    def post(self, request, servicio_id, paso_id=None):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        if paso_id:
            paso = get_object_or_404(ComoLoRealizo, id=paso_id)
            form = ComoLoRealizoForm(request.POST, instance=paso)
        else:
            form = ComoLoRealizoForm(request.POST)
        
        if form.is_valid():
            paso = form.save(commit=False)
            paso.servicio = servicio
            paso.save()
            return redirect('gestionar_realizo', servicio_id=servicio.id)

        pasos = ComoLoRealizo.objects.filter(servicio=servicio).order_by('canal_presentacion', 'paso')
        return render(request, 'servicios/realizo_form.html', {
            'servicio': servicio,
            'form': form,
            'pasos': pasos,
            'paso_id': paso_id,
        })
    
class EliminarPasoView(View):
    def post(self, request, paso_id):
        paso = get_object_or_404(ComoLoRealizo, id=paso_id)
        servicio_id = paso.servicio.id  # Guardamos para redirigir después
        paso.delete()
        return redirect('gestionar_realizo', servicio_id=servicio_id)
    
class CostosView(View):
    def get(self, request, servicio_id, costo_id=None):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        if costo_id:
            costo = get_object_or_404(CuantoCuesta, id=costo_id, servicio=servicio)
            form = CuantoCuestaForm(instance=costo)
        else:
            form = CuantoCuestaForm()
        
        costos = CuantoCuesta.objects.filter(servicio=servicio)
        return render(request, 'servicios/costos_form.html', {
            'servicio': servicio,
            'form': form,
            'costos': costos,
            'costo_id': costo_id,
        })

    def post(self, request, servicio_id, costo_id=None):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        if costo_id:
            costo = get_object_or_404(CuantoCuesta, id=costo_id, servicio=servicio)
            form = CuantoCuestaForm(request.POST, instance=costo)
        else:
            form = CuantoCuestaForm(request.POST)

        if form.is_valid():
            nuevo_costo = form.save(commit=False)
            nuevo_costo.servicio = servicio
            nuevo_costo.save()
            return redirect('gestionar_costos', servicio_id=servicio.id)

        costos = CuantoCuesta.objects.filter(servicio=servicio)
        return render(request, 'servicios/costos_form.html', {
            'servicio': servicio,
            'form': form,
            'costos': costos,
            'costo_id': costo_id,
        })
    
class EliminarCostoView(View):
    def post(self, request, costo_id):
        costo = get_object_or_404(CuantoCuesta, id=costo_id)
        servicio_id = costo.servicio.id
        costo.delete()
        return redirect('gestionar_costos', servicio_id=servicio_id)
    
@csrf_exempt
def crear_dependencia_ajax(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            nueva = Dependencia.objects.create(nombre=nombre)
            return JsonResponse({'success': True, 'id': nueva.id, 'nombre': nueva.nombre})
    return JsonResponse({'success': False})
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
    
class CrearCategoriaView(CreateView):
    model = CategoriaSevac
    form_class = CategoriaSevacForm
    template_name = 'sevac/crear_categoria.html'
    success_url = reverse_lazy('crear_carpeta') 

class CrearCarpetaView(View, LoginRequiredMixin):
    template_name = 'sevac/crear_carpeta.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.add_carpeta")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

@csrf_exempt
def crear_categoria_ajax_sevac(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        if nombre:
            categoria, created = CategoriaSevac.objects.get_or_create(nombre=nombre)
            return JsonResponse({'id': categoria.id, 'nombre': categoria.nombre})
    return JsonResponse({'error': 'Error al procesar'}, status=400)

def editar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaSevac, pk=pk)
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        categoria.nombre = nuevo_nombre
        categoria.save()
        messages.success(request, 'Categoría actualizada correctamente.')
    return redirect('listar_carpetas')

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaSevac, pk=pk)
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')
    return redirect('listar_carpetas')  # reemplaza con tu vista

# Vista para editar carpeta
class EditarCarpetaView(View, LoginRequiredMixin):
    template_name = 'sevac/editar_carpeta.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.change_carpeta")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
class SubirArchivoView(View, LoginRequiredMixin):
    template_name = 'sevac/subir_archivo.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.add_archivo")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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

class EditarArchivoView(View, LoginRequiredMixin):
    template_name = 'sevac/editar_archivo.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.change_archivo")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.view_carpeta")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agrupar carpetas principales por categoría
        carpetas_agrupadas = {}
        categorias = CategoriaSevac.objects.all()
        for categoria in categorias:
            carpetas_categoria = Carpeta.objects.filter(categoria=categoria, padre=None)
            if carpetas_categoria.exists():
                carpetas_agrupadas[categoria] = carpetas_categoria

        context['carpetas_agrupadas'] = carpetas_agrupadas
        context['categorias'] = categorias  # si necesitas en otros lugares

        # Tus otros contextos los dejamos igual
        context['total_carpetas'] = Carpeta.objects.filter(estatus='A', padre=None).count()
        context['total_archivos'] = Archivo.objects.filter(estatus='A').count()
        context['ultima_carpeta'] = Carpeta.objects.filter(estatus='A').order_by('-id').first()
        context['total_subcarpetas'] = Carpeta.objects.filter(estatus='A').exclude(padre=None).count()
        context['total_archivos_inactivos'] = Archivo.objects.filter(estatus='I').count()
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'SEVAC - Carpetas y Archivos', 'url': ''}
        }
        context['sidebar'] = 'sevac'
        context['regreso_url'] = reverse("dashboard")

        return context

    
class EliminarCarpetaView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.delete_carpeta")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, carpeta_id):
        carpeta = get_object_or_404(Carpeta, id=carpeta_id)
        carpeta.delete()  # Elimina la carpeta y su contenido
        return redirect('listar_carpetas')
    
# Vista para gestionar subcarpetas y archivos de una carpeta principal
class GestionarCarpetaView(View):
    template_name = 'sevac/gestionar_carpetas.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("sevac.view_carpeta")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, carpeta_id, **kwargs):
        context = kwargs
        carpeta = get_object_or_404(Carpeta, id=carpeta_id)
        
        # Obtener todas las subcarpetas y archivos, activos e inactivos
        subcarpetas = carpeta.subcarpetas.all().prefetch_related(
            'archivos',
            'subcarpetas__archivos',
            'subcarpetas__subcarpetas__archivos',
            'subcarpetas__subcarpetas__subcarpetas__archivos',
            'subcarpetas__subcarpetas__subcarpetas__subcarpetas__archivos'
        )

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
    
class ListaObligacionesView(LoginRequiredMixin, ListView):
    model = ListaObligaciones
    template_name = 'transparencia2/inicioTrasnparencia.html'
    context_object_name = 'lista_obligaciones'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.view_listaobligaciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
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
class ListaObligacionesCreateView(LoginRequiredMixin, CreateView):
    model = ListaObligaciones
    form_class = ListaObligacionesForm
    template_name = 'transparencia2/crearLista.html'
    success_url = reverse_lazy('lista_obligaciones')
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.add_listaobligaciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "La lista de obligaciones se ha creado correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('lista_obligaciones')
        context["breadcrumb"] = {
            'parent': {'name': 'Transparencia', 'url': url_configuracion},
            'child': {'name': 'Registro de nueva lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'
        context['regreso_url'] = reverse('lista_obligaciones')
        return context

# Vista para editar un registro de ListaObligaciones
class ListaObligacionesUpdateView(LoginRequiredMixin, UpdateView):
    model = ListaObligaciones
    form_class = ListaObligacionesForm
    template_name = 'transparencia2/editarLista.html'  # Template a usar para la vista
    context_object_name = 'lista_obligaciones'  # Nombre del objeto que se pasará al contexto
    success_url = reverse_lazy('lista_obligaciones')  # URL a la que redirigir después de guardar el formulario
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.change_listaobligaciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

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
        context['sidebar'] = 'transparencia'
        context['regreso_url'] = reverse('lista_obligaciones')

        return context

class ListaObligacionesDeleteView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.delete_listaobligaciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, pk):
        # Obtener el objeto que se quiere eliminar
        lista_obligaciones = get_object_or_404(ListaObligaciones, pk=pk)

        # Eliminar el objeto
        lista_obligaciones.delete()

        # Retornar una respuesta JSON indicando que la eliminación fue exitosa
        return JsonResponse({'success': True, 'message': 'Lista de Obligación eliminada exitosamente.'})
    

class GestionarArticulosView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.view_listaobligaciones")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, lista_id):
        # Obtener la lista de obligaciones
        lista_obligaciones = get_object_or_404(ListaObligaciones, pk=lista_id)

        # Obtener los artículos relacionados con la lista
        articulos = lista_obligaciones.articulos_liga.all().order_by("orden")

        # Crear el contexto con la información necesaria
        context = {
            'lista_obligaciones': lista_obligaciones,
            'articulos': articulos,
            'breadcrumb': {
                'parent': {'name': 'Transparencia', 'url': reverse('lista_obligaciones')},
                'child': {'name': 'Gestión de artículos', 'url': ''}
            },
            'sidebar': 'transparencia',
            
        }
        context['regreso_url'] = reverse('lista_obligaciones')

        # Renderizar la plantilla con el contexto
        return render(request, 'transparencia2/gestionarLista.html', context)
            

@csrf_exempt
def actualizar_orden_articulos(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for item in data["orden"]:
                articulo = ArticuloLiga.objects.get(id=item["id"])
                articulo.orden = item["orden"]
                articulo.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})


class CrearArticuloView(CreateView, LoginRequiredMixin):
    model = ArticuloLiga
    form_class = ArticuloLigaForm
    template_name = 'transparencia2/crearArticulo.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.add_articuloliga")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        lista_obligacion_id = self.kwargs.get('lista_obligacion_id')
        kwargs['lista_obligacion_id'] = lista_obligacion_id
        return kwargs

    def form_valid(self, form):
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        lista_obligacion = get_object_or_404(ListaObligaciones, pk=lista_obligacion_id)

        form.instance.lista_obligaciones = lista_obligacion

        # Asignar número de orden automáticamente
        ultimo_orden = ArticuloLiga.objects.filter(lista_obligaciones=lista_obligacion).aggregate(
            max_orden=models.Max('orden'))['max_orden']
        form.instance.orden = (ultimo_orden + 1) if ultimo_orden is not None else 1

        response = super().form_valid(form)
        messages.success(self.request, 'Artículo creado con éxito!')
        return response

    def get_success_url(self):
        return reverse_lazy('gestionar_articulos', kwargs={'lista_id': self.kwargs['lista_obligacion_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        lista_obligacion = get_object_or_404(ListaObligaciones, pk=lista_obligacion_id)

        context['lista_obligaciones'] = lista_obligacion
        context['breadcrumb'] = {
            'parent': {
                'name': 'Gestión de artículos',
                'url': reverse('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})
            },
            'child': {'name': 'Registro de artículos en lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'
        context['regreso_url'] = reverse('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})
        return context

class EditarArticuloView(UpdateView, LoginRequiredMixin):
    model = ArticuloLiga
    form_class = ArticuloLigaForm
    template_name = 'transparencia2/editarArticulo.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.change_articuloliga")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        articulo_id = self.kwargs['articulo_id']
        return get_object_or_404(ArticuloLiga, pk=articulo_id)

    def form_valid(self, form):
        messages.success(self.request, 'Artículo actualizado con éxito!')
        return super().form_valid(form)

    def get_success_url(self):
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        return reverse_lazy('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_obligacion_id = self.kwargs['lista_obligacion_id']
        lista_obligacion = get_object_or_404(ListaObligaciones, pk=lista_obligacion_id)

        context['lista_obligaciones'] = lista_obligacion
        context['breadcrumb'] = {
            'parent': {
                'name': 'Gestión de artículos',
                'url': reverse('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})
            },
            'child': {'name': 'Editar artículos en lista', 'url': ''}
        }
        context['sidebar'] = 'transparencia'
        context['regreso_url'] = reverse('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})
        return context
    

class EliminarArticuloView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.delete_articuloliga")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, articulo_id):
        # Obtener el artículo que se va a eliminar
        articulo = get_object_or_404(ArticuloLiga, id=articulo_id)
        
        # Eliminar el artículo
        articulo.delete()

        # Responder con éxito
        return JsonResponse({'success': True, 'message': 'Artículo eliminado con éxito'})
    

class GestionarArticulosArView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.view_ligaarchivo")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id):
        # Obtener el artículo específico mediante su ID
        articulo = get_object_or_404(ArticuloLiga, pk=id)

        # Obtener los archivos relacionados al artículo
        archivos = LigaArchivo.objects.filter(articuloDe=articulo).order_by('-ano')

        # Agrupar los archivos por año
        articulos_por_ano = {}
        for archivo in archivos:
            ano = archivo.ano
            if ano not in articulos_por_ano:
                articulos_por_ano[ano] = []

            articulos_por_ano[ano].append({
                'articulo': articulo,
                'tipo': 'liga' if archivo.liga else 'archivo',
                'archivo': archivo
            })

        # Obtener el ID de la lista para el botón de regreso
        lista_obligacion_id = articulo.lista_obligaciones.id

        context = {
            'articulo': articulo,
            'articulos_por_ano': dict(sorted(articulos_por_ano.items(), reverse=True)),
            'breadcrumb': {
                'parent': {'name': 'Transparencia', 'url': reverse('lista_obligaciones')},
                'child': {'name': 'Gestión de artículos', 'url': ''}
            },
            'sidebar': 'transparencia',
            'regreso_url': reverse('gestionar_articulos', kwargs={'lista_id': lista_obligacion_id})
        }

        return render(request, 'transparencia2/gestionar_articulo.html', context)
class CrearArticuloLigaView(CreateView, LoginRequiredMixin):
    model = LigaArchivo
    form_class = ArticuloLigaArchivoForm
    template_name = 'transparencia2/crear_articuloLA.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.add_ligaarchivo")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        articulo_id = self.kwargs.get('id')
        kwargs['articuloDe_id'] = articulo_id  # Estás pasando el 'id' correcto al formulario
        return kwargs
    
    def form_valid(self, form):
        # Obtener el articuloDe (ArticuloLiga) usando el id de la URL
        articulo_id = self.kwargs['id']
        articulo = get_object_or_404(ArticuloLiga, pk=articulo_id)
        
        # Asignamos el artículo al campo 'articuloDe' del nuevo objeto LigaArchivo
        form.instance.articuloDe = articulo
        
        # Guardamos el objeto LigaArchivo con el artículo relacionado
        response = super().form_valid(form)
        
        messages.success(self.request, 'Artículo creado con éxito!')
        return response

    def get_success_url(self):
        # Redirigimos al usuario a la vista de gestión de artículos después de la creación
        return reverse_lazy('gestionarArchivoLa', kwargs={'id': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el artículo utilizando el 'id' desde la URL
        articulo_id = self.kwargs['id']
        articulo = get_object_or_404(ArticuloLiga, pk=articulo_id)
        context['articulo'] = articulo

        # Obtener la ListaObligaciones asociada al artículo
        lista_obligacion = articulo.lista_obligaciones
        
        # Pasamos la lista de obligaciones al contexto
        context['lista_obligaciones'] = lista_obligacion
        url_configuracion = reverse('gestionar_articulos', kwargs={'lista_id': lista_obligacion.id})
        
        # Crear el breadcrumb con los enlaces adecuados
        context["breadcrumb"] = {
            'parent': {'name': 'Gestión de artículos', 'url': url_configuracion},
            'child': {'name': 'Registro de artículos en lista', 'url': ''}
        }
        
        context['sidebar'] = 'transparencia'
        
        return context

class EditarArticuloLigaArchivoView(UpdateView, LoginRequiredMixin):
    model = LigaArchivo
    form_class = ArticuloLigaArchivoForm
    template_name = 'transparencia2/editar_articuloLA.html'
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("transparencia.change_ligaarchivo")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el objeto LigaArchivo según el ID proporcionado en la URL
        return get_object_or_404(LigaArchivo, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Recuperar el objeto LigaArchivo
        context = super().get_context_data(**kwargs)
        liga_archivo = self.get_object()
        
        # Pasar el id de ArticuloLiga (no el id de LigaArchivo) al contexto
        context['articulo_liga_id'] = liga_archivo.articuloDe.id
        
        # Crear el breadcrumb con los enlaces adecuados
        url_configuracion = reverse('gestionarArchivoLa', kwargs={'id': liga_archivo.articuloDe.id})

        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Archivos', 'url': url_configuracion},
            'child': {'name': 'Editar Registro', 'url': ''}
        }
        return context

    def form_valid(self, form):
        # Llamar a la función base para guardar el formulario
        response = super().form_valid(form)
        # Mostrar un mensaje de éxito
        messages.success(self.request, 'Registro actualizado con éxito!')
        return response

    def get_success_url(self):
        # Redirige al usuario a la vista de gestión después de la edición
        return reverse_lazy('gestionarArchivoLa', kwargs={'id': self.object.articuloDe.id})
    
def eliminar_articulo_liga(request, articulo_id):
    # Obtener el objeto LigaArchivo que se desea eliminar
    liga_archivo = get_object_or_404(LigaArchivo, pk=articulo_id)

    if request.method == "POST":
        # Eliminar el objeto
        liga_archivo.delete()

        # Responder con un mensaje de éxito
        return JsonResponse({"success": True, "message": "Artículo eliminado exitosamente!"})

    # Si no es un POST, no permitimos la eliminación
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)
    
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

class convocatoriaHome(TemplateView, LoginRequiredMixin):
    template_name = 'convocatorias/convocatoriasHome.html'
    # --- control de permisos ---
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("convocatorias.view_convocatoria")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['convocatorias'] = Convocatoria.objects.all().order_by('-id')  # Ordenar por ID de forma descendente
        context['categorias'] = CategoriaConvocatoria.objects.all()
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Convocatorias', 'url': ''}
        }
        context['regreso_url'] = reverse('dashboard')
        context['sidebar'] = 'convo'
        return context

@require_GET
def filtrar_convocatorias(request):
    search_query = request.GET.get('q', '')
    estado_filtro = request.GET.get('estado', '')
    categoria_filtro = request.GET.get('categoria', '')

    convocatorias = Convocatoria.objects.all().order_by('-id')

    if search_query:
        convocatorias = convocatorias.filter(
            Q(titulo__icontains=search_query) |
            Q(categoria__nombre__icontains=search_query) |
            Q(estado__icontains=search_query)
        )

    if estado_filtro:
        convocatorias = convocatorias.filter(estado=estado_filtro)

    if categoria_filtro:
        convocatorias = convocatorias.filter(categoria__nombre=categoria_filtro)

    datos = []
    for convocatoria in convocatorias:
        datos.append({
            'id': convocatoria.id,
            'titulo': convocatoria.titulo,
            'categoria': convocatoria.categoria.nombre,
            'estado': convocatoria.estado,
            'descripcion': convocatoria.descripcion,
            'fecha_inicio': convocatoria.fecha_apertura.strftime('%Y-%m-%d'),
            'fecha_fin': convocatoria.fecha_cierre.strftime('%Y-%m-%d'),
            'imagen': convocatoria.imagen.url if convocatoria.imagen else '',
            'departamento': convocatoria.departamento if convocatoria.departamento else '',
            'email': convocatoria.email if convocatoria.email else '',
            'telefono': convocatoria.telefono if convocatoria.telefono else '',
            'horarios_atencion': convocatoria.horarios_atencion if convocatoria.horarios_atencion else '',

        })

    return JsonResponse({'convocatorias': datos})

def crear_convocatoria(request):
    # Obtener la URL de configuración (Dashboard)
    url_configuracion = reverse('convocatorias')

    # Crear la estructura del breadcrumb
    context = {
        "breadcrumb": {
            'parent': {'name': 'Convocatorias', 'url': url_configuracion},
            'child': {'name': 'Registro de convocatoria', 'url': ''}
        },
        'sidebar': 'convo',
        'regreso_url':url_configuracion
    }

    # Lógica para el formulario y el formset
    if request.method == 'POST':
        form = ConvocatoriaForm(request.POST, request.FILES)
        formset = ArchivoConvocatoriaFormSet(request.POST, request.FILES, queryset=ArchivoConvocatoria.objects.none())

        if form.is_valid() and formset.is_valid():
            convocatoria = form.save()

            for archivo_form in formset:
                if archivo_form.cleaned_data and not archivo_form.cleaned_data.get('DELETE', False):
                    archivo = archivo_form.save(commit=False)
                    archivo.convocatoria = convocatoria
                    archivo.save()

            # Redirigir después de guardar la convocatoria
            return redirect('convocatorias')
    else:
        form = ConvocatoriaForm()
        formset = ArchivoConvocatoriaFormSet(queryset=ArchivoConvocatoria.objects.none())

    # Incluir el contexto adicional antes de renderizar la plantilla
    context.update({'form': form, 'formset': formset})

    return render(request, 'convocatorias/crear_convocatoria.html', context)



def editar_convocatoria(request, pk):
    convocatoria = get_object_or_404(Convocatoria, pk=pk)
    url_configuracion = reverse('convocatorias')

    # Construyendo el contexto base para el breadcrumb y la navegación
    context = {
        "breadcrumb": {
            'parent': {'name': 'Convocatorias', 'url': url_configuracion},
            'child': {'name': 'Edición de convocatoria', 'url': ''}
        },
        'sidebar': 'convo',
        'regreso_url': url_configuracion,
    }

    # Obtenemos el queryset de archivos adjuntos de la convocatoria
    qs_archivos = ArchivoConvocatoria.objects.filter(convocatoria=convocatoria)

    # Determinamos el parámetro extra:
    # Si hay al menos un archivo, no se muestra formulario extra, de lo contrario se muestra uno.
    extra = 0 if qs_archivos.exists() else 1

    # Creamos el formset utilizando el extra calculado
    ArchivoFormSet = modelformset_factory(
        ArchivoConvocatoria,
        form=ArchivoConvocatoriaForm,
        extra=extra,
        can_delete=True
    )

    if request.method == 'POST':
        form = ConvocatoriaForm(request.POST, request.FILES, instance=convocatoria)
        formset = ArchivoFormSet(
            request.POST,
            request.FILES,
            queryset=qs_archivos
        )

        if form.is_valid() and formset.is_valid():
            convocatoria = form.save()

            # Guarda nuevos archivos o actualiza los existentes
            archivos = formset.save(commit=False)
            for archivo in archivos:
                archivo.convocatoria = convocatoria
                archivo.save()

            # Elimina los archivos marcados para borrar
            for archivo in formset.deleted_objects:
                archivo.delete()

            messages.success(request, "Convocatoria actualizada correctamente")
            return redirect('convocatorias')
        else:
            context.update({
                'form_errors': form.errors,
                'formset_errors': formset.errors,
            })
    else:
        form = ConvocatoriaForm(instance=convocatoria)
        formset = ArchivoFormSet(queryset=qs_archivos)

    context.update({
        'form': form,
        'formset': formset,
        'convocatoria': convocatoria 
    })
    return render(request, 'convocatorias/editar_convocatoria.html', context)

@csrf_exempt
def crear_categoria_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")
            if not nombre:
                return JsonResponse({"error": "Nombre requerido"}, status=400)
            categoria, created = CategoriaConvocatoria.objects.get_or_create(nombre=nombre)
            return JsonResponse({"id": categoria.id, "nombre": categoria.nombre})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)
# Vista para eliminar convocatoria
def eliminar_convocatoria(request, id):
    # Asegurarse de que la solicitud sea DELETE
    if request.method == 'DELETE':
        convocatoria = get_object_or_404(Convocatoria, id=id)
        convocatoria.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
def obtener_detalle_convocatoria(request, id):
    # Obtener la convocatoria por id
    convocatoria = get_object_or_404(Convocatoria, id=id)
    
    # Crear un diccionario con la información que deseas mostrar
    data = {
        'convocatoria': {
            'titulo': convocatoria.titulo,
            'fecha_inicio': convocatoria.fecha_apertura.strftime('%d-%m-%Y'),
            'fecha_fin': convocatoria.fecha_cierre.strftime('%d-%m-%Y'),
            'imagen': convocatoria.imagen.url if convocatoria.imagen else '',

        }
    }
    
    # Devolver los detalles de la convocatoria como JSON
    return JsonResponse(data)


class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'group_form.html'
    success_url = reverse_lazy('GruposView')
    permission_required = 'auth.add_group'

    def has_permission(self):
        # Si el usuario es superuser, se le permite crear grupos
        if self.request.user.is_superuser:
            return True
        return super().has_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Grupos', 'url': '/admin/generales/grupos/'},
            'child': {'name': 'Crear Grupo', 'url': ''}
        }
        context['sidebar'] = 'Generales'
        context['regreso_url'] = reverse_lazy('GruposView')

        # Enviamos todos los permisos al template para mostrarlos en la columna "disponibles"
        context['all_permissions'] = Permission.objects.all().order_by('codename')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group_name = self.object.name
        messages.success(
            self.request,
            f'El grupo "{group_name}" se ha creado y se le han asignado los permisos correctamente.'
        )
        return response
    



class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Pantalla para editar un grupo existente y sus permisos.
    Reutiliza el mismo GroupForm que la vista de creación.
    """
    model = Group
    form_class = GroupForm
    template_name = "group_form_edit.html"      # Usa la plantilla que verás más abajo
    success_url = reverse_lazy("GruposView")
    permission_required = "auth.change_group"

    # ——— Permisos ——————————————————————————————————————————————
    def has_permission(self):
        if self.request.user.is_superuser:
            return True
        return super().has_permission()

    # ——— Datos iniciales para el formulario ————————————————
    def get_initial(self):
        """
        Rellenamos el campo oculto 'permission_ids' con los permisos
        actuales del grupo para que el JavaScript los marque como
        seleccionados al cargar la página.
        """
        initial = super().get_initial()
        ids = self.object.permissions.values_list("id", flat=True)
        initial["permission_ids"] = ",".join(str(pk) for pk in ids)
        return initial

    # ——— Contexto para la plantilla ————————————————————————
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Grupos", "url": "/admin/generales/grupos/"},
            "child": {"name": f'Editar "{self.object.name}"', "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse_lazy("GruposView")

        # Todos los permisos para la columna “Disponibles”
        context["all_permissions"] = Permission.objects.all().order_by("codename")

        # IDs de los permisos ya asignados (los usará el JS)
        context["group_permissions_ids"] = list(
            self.object.permissions.values_list("id", flat=True)
        )
        return context

    # ——— Mensaje de éxito ————————————————————————————————
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'El grupo "{self.object.name}" se ha actualizado correctamente.',
        )
        return response



class SeccionPlusDetailView(TemplateView):
    template_name = 'seccionplus_detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        seccion = get_object_or_404(SeccionPlus, pk=pk, status=True)
        # Redirige si el slug no coincide
        if seccion.slug != slug:
            return redirect('seccionplus_detail', pk=seccion.pk, slug=seccion.slug)
        return seccion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seccion = self.get_object()

        context['seccion'] = seccion
        context['sidebar'] = 'mas'

        categoria = seccion.categoria_convocatoria

        if categoria:
            # Si hay categoría, filtra por ella
            context['convocatorias_activas'] = Convocatoria.objects.filter(
                estado__in=['ABIERTA', 'PRÓXIMA'],
                categoria=categoria
            ).order_by('-id')
            context['convocatorias_pasadas'] = Convocatoria.objects.filter(
                estado='CERRADA',
                categoria=categoria
            ).order_by('-id')
            context['categorias'] = CategoriaConvocatoria.objects.filter(pk=categoria.pk)
        else:
            # Si no hay categoría, muestra solo por estado (o vacío si prefieres)
            context['convocatorias_activas'] = Convocatoria.objects.filter(
                estado__in=['ABIERTA', 'PRÓXIMA']
            ).order_by('-id')
            context['convocatorias_pasadas'] = Convocatoria.objects.filter(
                estado='CERRADA'
            ).order_by('-id')
            context['categorias'] = CategoriaConvocatoria.objects.none()

        return context
def eliminar_aviso_privacidad(request, pk):
    aviso = get_object_or_404(AvisoDePrivacidad, pk=pk)
    if request.method == 'POST':
        aviso.delete()
        messages.success(request, "El aviso de privacidad se ha eliminado correctamente.")
    return redirect(reverse_lazy('PrivacidadView'))

class EncuestasView(LoginRequiredMixin, TemplateView):
    template_name = 'generales/encuestas.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.has_perm('transparencia.view_encuesta')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Encuestas', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse('generalesDashboard')
        context['regreso_url'] = url_configuracion
        
        # -- Aquí buscamos el primer municipio activo
        municipio_activo = Municipio.objects.filter(status='activo').first()
        if municipio_activo:
            # Tomamos las encuestas de ese municipio
            encuestas = municipio_activo.encuestas.all()
            total_activas = encuestas.filter(estado='activo').count()
            total_inactivas = encuestas.filter(estado='inactivo').count()
        else:
            # No hay municipio activo -> no hay encuestas
            encuestas = None
            total_activas = 0
            total_inactivas = 0
        
        # Enviamos todo lo que necesitamos al contexto
        context['municipio_activo'] = municipio_activo
        context['encuestas'] = encuestas
        
        # Guardamos los totales dentro de 'data' para facilidad en la plantilla
        context['data'] = {
            'total_activas': total_activas,
            'total_inactivas': total_inactivas
        }

        return context


class EncuestaDetailView(LoginRequiredMixin, DetailView):
    model = Encuesta
    template_name = 'generales/encuesta_detalle.html'
    context_object_name = 'encuesta'

    def dispatch(self, request, *args, **kwargs):
        # Verificación de permiso
        if not (request.user.is_superuser or request.user.has_perm('transparencia.view_encuesta')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encuesta = self.object  # La encuesta actual

        # Estadísticas generales
        total_preguntas = encuesta.preguntas.count()      # Total de preguntas
        total_envios = encuesta.envios.count()            # Total de envíos (respuestas completas)
        
        # Para cada pregunta, contaremos las respuestas por opción
        preguntas_stats = []
        for pregunta in encuesta.preguntas.all():
            total_respuestas_pregunta = Respuesta.objects.filter(pregunta=pregunta).count()
            opciones_stats = []

            for opcion in pregunta.opciones.all():
                opcion_count = Respuesta.objects.filter(
                    pregunta=pregunta,
                    opcion=opcion
                ).count()

                # Calculamos el porcentaje
                porcentaje_opcion = 0
                if total_respuestas_pregunta > 0:
                    porcentaje_opcion = (opcion_count / total_respuestas_pregunta) * 100

                opciones_stats.append({
                    'opcion_texto': opcion.texto,
                    'opcion_count': opcion_count,
                    'porcentaje': porcentaje_opcion
                })

            preguntas_stats.append({
                'pregunta_texto': pregunta.texto,
                'total_respuestas_pregunta': total_respuestas_pregunta,
                'opciones_stats': opciones_stats
            })

        # Ejemplo de data que podrías usar en Chart.js (o la librería que desees)
        # Podrías separar las series por pregunta o unificarlas según tu necesidad
        # Este es solo un ejemplo conceptual
        chart_data = []
        for p_stat in preguntas_stats:
            chart_data.append({
                'pregunta': p_stat['pregunta_texto'],
                'labels': [op['opcion_texto'] for op in p_stat['opciones_stats']],
                'data': [op['opcion_count'] for op in p_stat['opciones_stats']],
            })

        # Incluimos todo en el contexto
        context['breadcrumb'] = {
            'parent': {'name': 'Encuestas', 'url': '/admin/generales/encuestas'},
            'child': {'name': 'Ver Encuesta', 'url': ''},
        }
        context['sidebar'] = 'Generales'
        context['regreso_url'] = reverse('EncuestasView')

        context['total_preguntas'] = total_preguntas
        context['total_envios'] = total_envios
        context['preguntas_stats'] = preguntas_stats
        context['chart_data'] = chart_data  # En caso de querer usarlo para gráficos

        return context


@login_required
def encuesta_create_ajax(request):
    """
    Vista que maneja la creación de Encuesta + Preguntas + Opciones vía AJAX.
    Solo para superusuarios o quienes tengan el permiso 'transparencia.add_encuesta'.
    """
    user = request.user
    # Validación manual de permisos
    if not (user.is_superuser or user.has_perm('transparencia.add_encuesta')):
        return JsonResponse({'success': False, 'error': 'No tienes permiso para crear encuestas.'}, status=403)

    if request.method == 'GET':
        breadcrumb = {
            'parent': {'name': 'Encuestas', 'url': '/admin/generales/encuestas'},
            'child': {'name': 'Crear Encuesta', 'url': ''}
        }
        sidebar = 'Generales'
        url_configuracion = reverse('EncuestasView')
        regreso_url = url_configuracion
        context = {
            'breadcrumb': breadcrumb,
            'sidebar': sidebar,
            'regreso_url': regreso_url,
        }
        return render(request, 'generales/encuesta_create_ajax.html', context)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Forzar el primer municipio activo
            municipio_activo = Municipio.objects.filter(status='activo').first()
            if not municipio_activo:
                return JsonResponse({
                    'success': False,
                    'error': 'No existe un municipio activo para asociar la encuesta.'
                }, status=400)

            titulo = data.get('titulo', '')
            descripcion = data.get('descripcion', '')

            # Crear la encuesta con estado por defecto 'activo'
            encuesta = Encuesta.objects.create(
                municipio=municipio_activo,
                titulo=titulo,
                descripcion=descripcion,
                estado='activo'  # Forzado a 'activo'
            )

            # Procesar preguntas
            preguntas_data = data.get('preguntas', [])
            for p_data in preguntas_data:
                texto_pregunta = p_data.get('texto', '')
                orden = p_data.get('orden', 0)

                pregunta = Pregunta.objects.create(
                    encuesta=encuesta,
                    texto=texto_pregunta,
                    orden=orden
                )

                # Procesar opciones
                opciones_data = p_data.get('opciones', [])
                for op_texto in opciones_data:
                    Opcion.objects.create(
                        pregunta=pregunta,
                        texto=op_texto
                    )

            # Aquí se establece el mensaje de éxito que se mostrará luego de redirigir
            messages.success(request, "La encuesta se ha guardado correctamente.")

            return JsonResponse({'success': True, 'encuesta_id': encuesta.id}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def encuesta_eliminar(request, pk):
    encuesta = get_object_or_404(Encuesta, pk=pk)
    titulo_encuesta = encuesta.titulo  # Guardamos el título para mostrar en el mensaje
    encuesta.delete()
    messages.success(request, f'La encuesta "{titulo_encuesta}" ha sido eliminada correctamente.')
    # Redirige a la vista donde listamos las encuestas, ajústalo según tu proyecto
    return redirect('EncuestasView')  # o la vista que muestre el listado de encuestas


@login_required
def encuesta_update_ajax(request, encuesta_id):
    """
    Vista que maneja la edición de Encuesta + Preguntas + Opciones vía AJAX.
    Solo para superusuarios o quienes tengan el permiso 'transparencia.change_encuesta'.
    """
    user = request.user
    # Validación manual de permisos
    if not (user.is_superuser or user.has_perm('transparencia.change_encuesta')):
        return JsonResponse({'success': False, 'error': 'No tienes permiso para editar encuestas.'}, status=403)

    # Intentamos obtener la encuesta a editar
    try:
        encuesta = Encuesta.objects.get(pk=encuesta_id)
    except Encuesta.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'La encuesta solicitada no existe.'}, status=404)

    if request.method == 'GET':
        # Construimos la data para inyectar en el template
        preguntas_data = []
        for pregunta in encuesta.preguntas.all().order_by('orden', 'id'):
            opciones = list(pregunta.opciones.values_list('texto', flat=True))
            preguntas_data.append({
                'id': pregunta.id,
                'texto': pregunta.texto,
                'orden': pregunta.orden,
                'opciones': opciones,
            })

        encuesta_data = {
            'id': encuesta.id,
            'titulo': encuesta.titulo,
            'descripcion': encuesta.descripcion or '',
            'preguntas': preguntas_data
        }

        breadcrumb = {
            'parent': {'name': 'Encuestas', 'url': '/admin/generales/encuestas'},
            'child': {'name': 'Editar Encuesta', 'url': ''}
        }
        sidebar = 'Generales'
        regreso_url = reverse('EncuestasView')
        context = {
            'breadcrumb': breadcrumb,
            'sidebar': sidebar,
            'regreso_url': regreso_url,
            'encuesta_data_json': json.dumps(encuesta_data),  # Inyectamos en el template
            'encuesta_id': encuesta.id,  # <-- Nuevo valor en el contexto

        }
        return render(request, 'generales/encuesta_edit_ajax.html', context)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            titulo = data.get('titulo', '').strip()
            descripcion = data.get('descripcion', '').strip()

            # Actualizamos los campos principales de la encuesta
            encuesta.titulo = titulo
            encuesta.descripcion = descripcion
            # (Opcional) podrías forzar a 'activo', o dejarlo a elección del usuario
            encuesta.estado = 'activo'
            encuesta.save()

            # Listado de preguntas que el frontend está mandando
            nuevas_preguntas = data.get('preguntas', [])

            # IDs de preguntas *nuevas* o *existentes* (para luego saber cuáles borrar)
            frontend_pregunta_ids = []

            for p_data in nuevas_preguntas:
                pregunta_id = p_data.get('id')  # si viene del frontend
                texto_pregunta = p_data.get('texto', '').strip()
                orden = p_data.get('orden', 0)
                opciones_data = p_data.get('opciones', [])

                if pregunta_id:
                    # Pregunta existente, actualizar
                    try:
                        pregunta_obj = Pregunta.objects.get(pk=pregunta_id, encuesta=encuesta)
                        pregunta_obj.texto = texto_pregunta
                        pregunta_obj.orden = orden
                        pregunta_obj.save()
                    except Pregunta.DoesNotExist:
                        # Si no existe, la creamos (o podrías ignorar)
                        pregunta_obj = Pregunta.objects.create(
                            encuesta=encuesta,
                            texto=texto_pregunta,
                            orden=orden
                        )
                else:
                    # Crear nueva pregunta
                    pregunta_obj = Pregunta.objects.create(
                        encuesta=encuesta,
                        texto=texto_pregunta,
                        orden=orden
                    )

                frontend_pregunta_ids.append(pregunta_obj.id)

                # Actualizar / Crear opciones
                # Primero, obtenemos todas las opciones actuales de la pregunta
                opciones_existentes = list(pregunta_obj.opciones.all())
                # Convertimos a dict {texto: Opcion}
                opciones_existentes_dict = {op.texto: op for op in opciones_existentes}

                # Las opciones se identifican sólo por su texto aquí; si quisieras IDs para las opciones,
                # deberías cambiarlos en el frontend y parsear igual.
                nuevas_opciones_textos = [op.strip() for op in opciones_data if op.strip()]

                # Eliminamos opciones que no están en la nueva lista
                for op in opciones_existentes:
                    if op.texto not in nuevas_opciones_textos:
                        op.delete()

                # Creamos las que no existan
                for texto_op in nuevas_opciones_textos:
                    if texto_op not in opciones_existentes_dict:
                        Opcion.objects.create(
                            pregunta=pregunta_obj,
                            texto=texto_op
                        )

            # Borrar preguntas que ya no vienen en el JSON
            Pregunta.objects.filter(encuesta=encuesta).exclude(id__in=frontend_pregunta_ids).delete()

            messages.success(request, "La encuesta se ha actualizado correctamente.")
            return JsonResponse({'success': True, 'encuesta_id': encuesta.id}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@login_required
@permission_required("transparencia.change_encuesta", raise_exception=True)
def encuesta_toggle_estado(request, encuesta_id):
    """
    Cambia 'activo' ↔ 'inactivo' en una Encuesta y redirige
    a la pantalla principal con un message.success.
    """
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)

    nueva_estado = "inactivo" if encuesta.estado == "activo" else "activo"
    encuesta.estado = nueva_estado
    encuesta.save(update_fields=["estado"])

    accion = "desactivada" if nueva_estado == "inactivo" else "activada"
    messages.success(
        request,
        f'La encuesta “{encuesta.titulo}” ha sido {accion} correctamente.'
    )

    # Si llegas con ?next=/algo, respeta esa redirección
    return redirect("EncuestasView")

class HablaHome(TemplateView, LoginRequiredMixin):
    template_name = 'HablaHijos/hablaHome.html'
    # --- control de permisos ---
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("eventos.view_articulo")):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = Articulo.objects.all().order_by('-id')  # Ordenar por ID de forma descendente
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Habla con tus hijos', 'url': ''}
        }
        context['regreso_url'] = reverse('dashboard')
        context['sidebar'] = 'habla'
        return context
    
class ArticuloCreateView(CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'hablaHijos/registrarArticulo.html'  # Puedes cambiar la ruta al template si es necesario
    success_url = reverse_lazy('habla_home')  # Redirige a la lista de artículos después de guardar el artículo

    def form_valid(self, form):
        # Aquí puedes añadir lógica adicional antes de guardar el artículo (por ejemplo, agregar el autor actual al artículo)
        articulo = form.save(commit=False)
        articulo.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Añadimos contexto adicional al renderizado de la plantilla, si es necesario
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('habla_home')
        context["breadcrumb"] = {
            'parent': {'name': 'Habla con tus hijos', 'url': url_configuracion},
            'child': {'name': 'Crear Articulo', 'url': ''}
        }
        context['regreso_url'] = reverse('habla_home')
        context['sidebar'] = 'habla'
        return context
    
class ArticuloUpdateView(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'HablaHijos/editarArticulo.html'  # crea esta plantilla
    success_url = reverse_lazy('habla_home')  # URL para redirigir tras éxito

    # Opcional: controlar permisos si es necesario
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm("eventos.change_articulo")):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Añadimos contexto adicional al renderizado de la plantilla, si es necesario
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('habla_home')
        context["breadcrumb"] = {
            'parent': {'name': 'Habla con tus hijos', 'url': url_configuracion},
            'child': {'name': 'Editar Articulo', 'url': ''}
        }
        context['regreso_url'] = reverse('habla_home')
        context['sidebar'] = 'habla'
        return context
    
@login_required
@permission_required('eventos.delete_articulo', raise_exception=True)
def eliminar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, f'El artículo "{articulo.titulo}" fue eliminado correctamente.')
        return redirect('habla_home')  # Ajusta la url a donde quieras redirigir
    else:
        # Si quieres mostrar un template de confirmación, puedes hacerlo aquí
        return redirect('habla_home')

@csrf_exempt  # Usamos csrf_exempt si es necesario, pero mejor sería usar CSRF token correctamente
def agregar_categoria_habla(request):
    if request.method == 'POST':
        categoria_nombre = request.POST.get('categoria_nombre', '').strip()

        if categoria_nombre:
            # Verificar si la categoría ya existe
            categoria, created = CategoriaHabla.objects.get_or_create(nombre=categoria_nombre)
            
            if created:
                # Retornamos un JsonResponse con la información de la categoría
                return JsonResponse({
                    'success': True,
                    'categoria': categoria.nombre,
                    'categoria_id': categoria.id
                })
            else:
                # Si la categoría ya existe, devolver un error
                return JsonResponse({'success': False, 'message': 'La categoría ya existe.'})

        return JsonResponse({'success': False, 'message': 'El nombre de la categoría no puede estar vacío.'})
    
    return JsonResponse({'success': False, 'message': 'Solicitud inválida.'})

def agregar_autor(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        perfil = request.POST.get('perfil', '').strip()
        trayectoria = request.POST.get('trayectoria', '').strip()
        fotografia = request.FILES.get('fotografia', None)

        if nombre_completo and perfil and trayectoria:
            # Crear un nuevo autor
            autor = Autor.objects.create(
                nombre_completo=nombre_completo,
                perfil=perfil,
                trayectoria=trayectoria,
                fotografia=fotografia
            )
            return JsonResponse({
                'success': True,
                'autor': autor.nombre_completo,
                'autor_id': autor.id
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Todos los campos son obligatorios.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Solicitud inválida.'
    })


class VideosView(LoginRequiredMixin, TemplateView):
    template_name = 'videos/videos.html'
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # ajusta 'transparencia' al app_label real de tu modelo VideoMunicipio
        if not (user.is_superuser or user.has_perm('generales.view_videomunicipio')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Generales', 'url': '/admin'},
            'child':  {'name': 'Videos',    'url': ''      }
        }
        context['sidebar']     = 'Generales'
        context['regreso_url'] = reverse('generalesDashboard')

        municipio_activo = Municipio.objects.filter(status='activo').first()
        if municipio_activo:
            videos = municipio_activo.videos.all()
            total_videos = videos.count()
        else:
            videos = None
            total_videos = 0

        context['municipio_activo'] = municipio_activo
        context['videos']           = videos
        context['data']             = {'total_videos': total_videos}

        return context
    

class VideoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = VideoMunicipio
    form_class = VideoMunicipioForm
    template_name = 'videos/video_form.html'
    permission_required = 'generales.add_videomunicipio'
    success_url = reverse_lazy('videos')

    def dispatch(self, request, *args, **kwargs):
        # permitir sólo superuser o con permiso explícito
        if not (request.user.is_superuser or request.user.has_perm(self.permission_required)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # asignar al municipio activo
        municipio_activo = Municipio.objects.filter(status='activo').first()
        if not municipio_activo:
            form.add_error(None, "No existe un municipio activo.")
            return self.form_invalid(form)
        form.instance.municipio = municipio_activo
        response = super().form_valid(form)
        messages.success(self.request, "Video agregado con éxito.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Generales', 'url': '/admin/videos/'},
            'child':  {'name': 'Crear Video',    'url': ''      }
        }
        context['sidebar']     = 'Generales'
        context['regreso_url'] = reverse('videos')

        municipio_activo = Municipio.objects.filter(status='activo').first()
        if municipio_activo:
            videos = municipio_activo.videos.all()
            total_videos = videos.count()
        else:
            videos = None
            total_videos = 0

        context['municipio_activo'] = municipio_activo
        context['videos']           = videos
        context['data']             = {'total_videos': total_videos}

        return context
    
class VideoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = VideoMunicipio
    form_class = VideoMunicipioForm
    template_name = 'videos/video_form.html'
    permission_required = 'generales.change_videomunicipio'
    success_url = reverse_lazy('videos')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.has_perm(self.permission_required)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Video actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # reutilizamos breadcrumb y regreso_url
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child':  {'name': 'Editar Video', 'url': ''      }
        }
        context['sidebar']     = 'Generales'
        context['regreso_url'] = reverse_lazy('videos')
        return context
    
@login_required
@permission_required('generales.delete_videomunicipio', raise_exception=True)
@require_POST
def video_delete(request, pk):
    video = get_object_or_404(VideoMunicipio, pk=pk)
    video.delete()
    messages.success(request, "Video eliminado con éxito.")
    return redirect('videos')