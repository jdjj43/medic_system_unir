from django import forms
from .models import Especialidad, Medico
from usuarios.models import Usuario, Rol


class EspecialidadForm(forms.ModelForm):

    class Meta:
        model = Especialidad
        fields = ["nombre", "descripcion"]
        labels = {
            "nombre": "Nombre de la Especialidad",
            "descripcion": "Descripción",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Cardiología, Pediatría...",
                    "required": True,
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción detallada de la especialidad...",
                    "rows": 4,
                }
            ),
        }


class MedicoForm(forms.ModelForm):

    class Meta:
        model = Medico
        fields = ["usuario", "especialidad", "numero_licencia", "consultorio"]
        labels = {
            "usuario": "Usuario Asociado",
            "especialidad": "Especialidad Médica",
            "numero_licencia": "Número de Licencia / Colegiatura",
            "consultorio": "Consultorio / Ubicación",
        }
        widgets = {
            "usuario": forms.Select(
                attrs={"class": "form-control"}
            ),
            "especialidad": forms.Select(
                attrs={"class": "form-control"}
            ),
            "numero_licencia": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: MPPS-123456"
                }
            ),
            "consultorio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Consultorio 204, Piso 2"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = Usuario.objects.filter(rol=Rol.MEDICO)
        if self.instance and self.instance.pk:
            medicos_con_perfil = Medico.objects.exclude(pk=self.instance.pk).values_list("usuario_id", flat=True)
            qs = qs.exclude(id__in=medicos_con_perfil)
        else:
            medicos_con_perfil = Medico.objects.values_list("usuario_id", flat=True)
            qs = qs.exclude(id__in=medicos_con_perfil)

        self.fields["usuario"].queryset = qs
        self.fields["usuario"].label_from_instance = lambda obj: f"{obj.get_full_name() or obj.username} ({obj.username})"

