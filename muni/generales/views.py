from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomAuthenticationForm
# Create your views here.
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

        return context
    

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


class NewsView(LoginRequiredMixin, TemplateView):
    template_name = "noticias.html"  
    login_url = reverse_lazy('login')  # Redirigir si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('dashboard')
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Noticias', 'url': ''}
        }
        context['sidebar'] = 'noticias'  # Asegura que el sidebar resalte la sección de Noticias

        return context


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

        return context
