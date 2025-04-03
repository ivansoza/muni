from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.contrib import messages

from django.urls import reverse_lazy

from usuario.forms import NoAutofocusPasswordChangeForm

# Create your views here.



class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'mi_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Mi Perfil', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse( 'dashboard')
        context['regreso_url']= url_configuracion
        context['usuario'] = self.request.user

        return context
    

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = NoAutofocusPasswordChangeForm
    template_name = 'registration/cambiar_contraseña.html'
    success_url = reverse_lazy('password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Mi Perfil', 'url': '/admin'},
            'child': {'name': 'Cambiar Contraseña', 'url': ''}
        }
        url_configuracion = reverse( 'perfil_usuario')
        context['regreso_url']= url_configuracion

        return context
    

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/cambiar_contraseña_hecho.html'

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'editar_perfil.html'
    success_url = reverse_lazy('perfil_usuario')  

    def get_object(self):
        # Retorna el usuario autenticado
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Tu perfil ha sido actualizado correctamente.')
        return response