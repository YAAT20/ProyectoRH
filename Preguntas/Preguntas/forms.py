from django import forms
from .models import Universidad, Curso, Tema, Pregunta

class UniversidadForm(forms.ModelForm):
    class Meta:
        model = Universidad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'universidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'universidad': forms.Select(attrs={'class': 'form-control'})
        }

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nombre', 'curso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'})
        }

class PreguntaForm(forms.ModelForm):
    add_nombre = forms.BooleanField(required=False, label="¿Deseas añadir un nombre?")

    class Meta:
        model = Pregunta
        fields = ['universidad', 'curso', 'tema', 'nivel', 'nombre', 'contenido']
        widgets = {
            'universidad': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'tema': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),  # Deshabilitar por defecto
            'contenido': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = False  # Hace el campo nombre opcional
        
        if 'universidad' in self.data:
            try:
                universidad_id = int(self.data.get('universidad'))
                self.fields['curso'].queryset = Curso.objects.filter(universidad_id=universidad_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Si no hay universidad seleccionada, no filtrar
        else:
            self.fields['curso'].queryset = Curso.objects.none()  # Sin cursos si no hay universidad seleccionada

        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['tema'].queryset = Tema.objects.filter(curso_id=curso_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Si no hay curso seleccionado, no filtrar
        else:
            self.fields['tema'].queryset = Tema.objects.none()  # Sin temas si no hay curso seleccionado

    def clean_contenido(self):
        contenido = self.cleaned_data.get('contenido')
        if contenido.size > 5 * 1024 * 1024:  # Limitar a 5 MB
            raise forms.ValidationError("El archivo es demasiado grande. El tamaño máximo permitido es de 5 MB.")
        return contenido

#filtrar 
class FiltroPreguntaForm(forms.Form):
    universidad = forms.ModelChoiceField(queryset=Universidad.objects.all(), required=False)
    curso = forms.ModelChoiceField(queryset=Curso.objects.none(), required=False)
    tema = forms.ModelChoiceField(queryset=Tema.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'universidad' in self.data:
            try:
                universidad_id = int(self.data.get('universidad'))
                self.fields['curso'].queryset = Curso.objects.filter(universidad_id=universidad_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Si no hay universidad seleccionada, no filtrar
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['tema'].queryset = Tema.objects.filter(curso_id=curso_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Si no hay curso seleccionado, no filtrar