from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple

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
        widget=forms.EmailInput(attrs={
            "placeholder": "correo@ejemplo.com"
        })
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
            "username": forms.TextInput(attrs={
                "placeholder": "Nombre de usuario",
                # No se agrega autofocus aquí
            }),
            "password1": forms.PasswordInput(attrs={
                "placeholder": "Contraseña segura"
            }),
            "password2": forms.PasswordInput(attrs={
                "placeholder": "Repite la contraseña"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina cualquier atributo autofocus que pudiese haber en los widgets
        for field in self.fields.values():
            field.widget.attrs.pop('autofocus', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            grupo = self.cleaned_data.get("grupo")
            if grupo:
                user.groups.add(grupo)
        return user


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Grupo",
        help_text="Selecciona un grupo para el usuario (opcional)."
    )

    class Meta:
        model = User
        fields = ("username", "email", "grupo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el usuario tiene algún grupo asignado, se inicializa con el primero
        if self.instance:
            groups = self.instance.groups.all()
            if groups.exists():
                self.fields["grupo"].initial = groups.first()


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