from django import forms
from .models import HistorialMedico, ArchivoMedico
from citas.models import Cita
from pacientes.models import Paciente
from medicos.models import Medico


class HistorialMedicoForm(forms.ModelForm):

    class Meta:
        model = HistorialMedico
        fields = [
            "paciente",
            "medico",
            "cita",
            "diagnostico",
            "sintomas",
            "tratamiento",
            "observaciones",
        ]
        labels = {
            "paciente": "Paciente",
            "medico": "Médico Tratante",
            "cita": "Cita Médica Asociada",
            "diagnostico": "Diagnóstico Clínico",
            "sintomas": "Síntomas Presentados",
            "tratamiento": "Tratamiento / Indicaciones",
            "observaciones": "Observaciones Médicas",
        }
        widgets = {
            "paciente": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
            "medico": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
            "cita": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
            "diagnostico": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Diagnóstico principal del paciente...",
                    "required": True,
                }
            ),
            "sintomas": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Síntomas expresados o evaluados...",
                }
            ),
            "tratamiento": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Tratamiento o medicamentos prescritos...",
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Notas adicionales del médico...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["paciente"].label_from_instance = lambda obj: f"{obj.nombres} {obj.apellidos} (C.I. {obj.cedula})"
        self.fields["medico"].label_from_instance = lambda obj: f"Dr. {obj.usuario.get_full_name() or obj.usuario.username} - {obj.especialidad.nombre}"
        self.fields["cita"].label_from_instance = lambda obj: f"Cita #{obj.id} ({obj.fecha.strftime('%d/%m/%Y')} {obj.hora.strftime('%H:%M')}) - {obj.paciente.nombres} {obj.paciente.apellidos}"

        citas_con_historial = HistorialMedico.objects.values_list('cita_id', flat=True)

        if self.instance and self.instance.pk and self.instance.cita_id:
            citas_con_historial = citas_con_historial.exclude(cita_id=self.instance.cita_id)
        
        self.fields["cita"].queryset = Cita.objects.filter(
            id__in=Cita.objects.exclude(id__in=citas_con_historial).values_list('id', flat=True)
        ).select_related('paciente', 'medico', 'medico__usuario').order_by('-fecha', '-hora')


class ArchivoMedicoForm(forms.ModelForm):

    class Meta:
        model = ArchivoMedico
        fields = [
            "archivo",
            "tipo",
        ]
        labels = {
            "archivo": "Archivo / Documento Adjunto",
            "tipo": "Tipo de Documento",
        }
        widgets = {
            "archivo": forms.FileInput(
                attrs={"class": "form-control", "required": True}
            ),
            "tipo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Examen de Sangre, Radiografía, Receta, Informe...",
                    "required": True,
                }
            ),
        }
