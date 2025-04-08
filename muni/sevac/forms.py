from django import forms
from .models import Carpeta, Archivo, CategoriaSevac
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class CategoriaSevacForm(forms.ModelForm):
    class Meta:
        model = CategoriaSevac
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre de la categoría',
        }

# Función recursiva para obtener todas las subcarpetas de forma anidada
def obtener_subcarpetas(carpeta_id):
    subcarpetas = Carpeta.objects.filter(padre_id=carpeta_id, estatus='A')
    resultado = list(subcarpetas)
    for subcarpeta in subcarpetas:
        resultado.extend(obtener_subcarpetas(subcarpeta.id))
    return resultado

class CarpetaForm(forms.ModelForm):
    class Meta:
        model = Carpeta
        fields = ['categoria', 'nombre', 'padre', 'estatus']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'padre': forms.Select(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'categoria': 'Categoria',
            'nombre': 'Nombre de la Carpeta',
            'padre': 'Carpeta Padre',
            'estatus': 'Estatus',
        }

    def __init__(self, *args, **kwargs):
        padre_id = kwargs.pop('padre_id', None)  # Capturar el ID de la carpeta padre
        es_subcarpeta = kwargs.pop('es_subcarpeta', False)
        super().__init__(*args, **kwargs)

        if es_subcarpeta:
            self.fields.pop('categoria')  # Ocultar campo 'categoria' si es subcarpeta
            if padre_id:
                subcarpetas = obtener_subcarpetas(padre_id)
                self.fields['padre'].queryset = Carpeta.objects.filter(id=padre_id) | Carpeta.objects.filter(id__in=[c.id for c in subcarpetas])
            else:
                self.fields['padre'].queryset = Carpeta.objects.none()
        else:
            self.fields.pop('padre')  # Ocultar campo 'padre' si no es subcarpeta

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['carpeta', 'nombre', 'archivo', 'estatus']
        widgets = {
            'carpeta': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'carpeta': 'Carpeta',
            'nombre': 'Nombre del Archivo',
            'archivo': 'Archivo',
            'estatus': 'Estatus',
        }

    def __init__(self, *args, **kwargs):
        padre_id = kwargs.pop('padre_id', None)  # Capturar el ID de la carpeta padre
        archivo = kwargs.get('instance', None)  # Verificar si estamos editando una instancia existente de Archivo
        super().__init__(*args, **kwargs)

        if archivo:  # Si es un archivo existente, establecer su carpeta
            self.fields['carpeta'].initial = archivo.carpeta.id
        elif padre_id:  # Si estamos creando un archivo dentro de una subcarpeta
            # Filtrar el campo 'carpeta' para mostrar la carpeta padre y todas sus subcarpetas anidadas
            subcarpetas = obtener_subcarpetas(padre_id)
            self.fields['carpeta'].queryset = Carpeta.objects.filter(id=padre_id) | Carpeta.objects.filter(id__in=[c.id for c in subcarpetas])
        else:
            self.fields['carpeta'].queryset = Carpeta.objects.none()  # Si no hay ID, dejar vacío


