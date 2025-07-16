from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple

from generales.models import SeccionPlus, Secciones, VideoMunicipio
from informacion_municipal.models import ElementoLista, InformacionCiudad

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'form-control with-icon',
            'autocomplete': 'username',
            'spellcheck': 'false'
        }),
        label='Correo electrónico'
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control with-icon',
            'id': 'password-field', 
            'autocomplete': 'current-password',
            'spellcheck': 'false'
        })
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Ingresar', 
                   css_class='btn btn-primary w-100 mb-3',
                   css_id='submit-button'),
            HTML("""
            <div class="additional-links">
                <a href="#"><i class="fas fa-key mr-1"></i>¿Olvidaste tu contraseña?</a>
                <span class="text-muted">|</span>
                <a href="#"><i class="fas fa-user-plus mr-1"></i>Crear cuenta</a>
            </div>
            <div class="social-login mt-4">
                <p class="text-muted mb-3">O ingresa con</p>
                <div class="d-flex justify-content-center">
                    <a href="#" class="social-btn">
                        <i class="fab fa-google"></i>
                    </a>
                    <a href="#" class="social-btn">
                        <i class="fab fa-facebook-f"></i>
                    </a>
                    <a href="#" class="social-btn">
                        <i class="fab fa-apple"></i>
                    </a>
                </div>
            </div>
            """)
        )






class UserCreationWithGroupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"})
    )
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Grupo",
        help_text="Si no ves un grupo disponible, crea uno primero.",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "grupo")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nombre de usuario"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Contraseña segura"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Repite la contraseña"}),
        }

    # quitamos cualquier autofocus heredado
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.pop("autofocus", None)

    # ---- CORRECCIÓN AQUÍ ----
    def save(self, commit=True):
        # 1. Creamos el usuario con las contraseñas ya encriptadas
        user = super().save(commit=True)   # commit=True porque UserCreationForm
                                           # ya llama a set_password()

        # 2. Añadimos el grupo (si se seleccionó)
        grupo = self.cleaned_data.get("grupo")
        if grupo:
            grupo.user_set.add(user)       # equivalente a user.groups.add(grupo)

        return user   


class UserEditForm(forms.ModelForm):
    email  = forms.EmailField(required=True)
    grupo  = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        required = False,
        label    = "Grupo",
        help_text= "Selecciona un grupo para el usuario (opcional)."
    )

    class Meta:
        model  = User
        fields = ("username", "email", "grupo")

    # --------- inicializamos el grupo actual ---------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:              # usuario ya existe
            first_group = self.instance.groups.first()
            if first_group:
                self.fields["grupo"].initial = first_group

    # --------- guardamos los cambios ---------
    def save(self, commit=True):
        user = super().save(commit=False)                   # username y email

        if commit:
            user.save()

            grupo = self.cleaned_data.get("grupo")
            if grupo:
                # mantenemos SÓLO ese grupo
                user.groups.set([grupo])
            else:
                # si se deja vacío, quitamos todos los grupos
                user.groups.clear()

        return user
class GroupForm(forms.ModelForm):
    """
    Formulario para crear o editar un grupo, usando un campo oculto
    para gestionar los permisos seleccionados mediante JavaScript.
    """
    # Campo oculto que guardará los IDs de permisos seleccionados.
    permission_ids = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Group
        fields = ['name']  # Solo mostramos el nombre del grupo (los permisos se manejan manualmente)

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()

        # Asignamos los permisos que vienen en 'permission_ids'
        if self.cleaned_data.get('permission_ids'):
            # Dividimos los IDs por coma y buscamos los permisos en la BD
            permission_ids_list = self.cleaned_data['permission_ids'].split(',')
            perms = Permission.objects.filter(id__in=permission_ids_list)
            group.permissions.set(perms)
        else:
            # Si no hay nada seleccionado, se limpian los permisos
            group.permissions.clear()

        return group
    

# generales/forms.py
class SeccionesForm(forms.ModelForm):
    class Meta:
        model  = Secciones
        fields = [
            'noticias', 'convocatorias', 'transparencia', 'servicios',
            'habla_con_tus_hijos', 'aviso_de_privacidad', 'gabinete',
            'sevac', 'contacts', 'reportes', 'encuestas',
            'servicios_en_linea', 'videos',                      # ← agregado
        ]


class SeccionPlusForm(forms.ModelForm):
    class Meta:
        model = SeccionPlus
        fields = ['categoria_convocatoria', 'nombre', 'banner', 'status', 'detalles', 'es_general', 'archivo']
        widgets = {
            'categoria_convocatoria': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'es_general': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class InformacionCiudadForm(forms.ModelForm):
    class Meta:
        model = InformacionCiudad
        exclude = ("municipio",)

class ElementoListaForm(forms.ModelForm):
    class Meta:
        model = ElementoLista
        fields = ("texto",)


class VideoMunicipioForm(forms.ModelForm):
    class Meta:
        model = VideoMunicipio
        fields = ['nombre', 'frame', 'orden']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'frame': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/embed/…'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }