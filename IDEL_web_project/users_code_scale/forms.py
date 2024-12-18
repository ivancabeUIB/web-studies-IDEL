from django import forms
from .models import CodesForScales


class CodeForm(forms.Form):
    code = forms.CharField(
        label='Código',
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu código aquí'})
    )
