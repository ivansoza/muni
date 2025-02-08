from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML

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