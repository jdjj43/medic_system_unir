from django import forms
from .models import Paciente


class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = [
            "cedula",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "direccion",
            "correo",
        ]
        labels = {
            "cedula": "Cédula / Documento de Identidad",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "sexo": "Sexo",
            "telefono": "Teléfono",
            "direccion": "Dirección de Residencia",
            "correo": "Correo Electrónico",
        }
        widgets = {
            "cedula": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: V-12345678",
                    "required": True,
                }
            ),
            "nombres": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres del paciente",
                    "required": True,
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos del paciente",
                    "required": True,
                }
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "sexo": forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True,
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+58 412-1234567",
                    "required": True,
                }
            ),
            "direccion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dirección completa...",
                    "rows": 3,
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "correo@ejemplo.com",
                }
            ),
        }
