from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse

from django.urls import reverse_lazy

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from informacion_municipal.models import Municipio
from servicios.forms import ServicioForm
from servicios.models import Servicio
from .forms import CustomAuthenticationForm
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
from transparencia.forms import SeccionTransparenciaForm, EjercicioFiscalForm, DocumentoTransparenciaForm
from transparencia.models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia
from sevac.models import Carpeta, Archivo
from sevac.forms import CarpetaForm, ArchivoForm
# Create your views here.
from django.db.models import Count

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


    
class ListarCarpetasView(TemplateView):
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