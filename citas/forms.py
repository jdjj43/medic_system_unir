from django import forms
from .models import Cita
from pacientes.models import Paciente
from medicos.models import Medico


class CitaForm(forms.ModelForm):

    class Meta:
        model = Cita
        fields = [
            "paciente",
            "medico",
            "fecha",
            "hora",
            "motivo",
            "estado",
            "observaciones",
        ]
        labels = {
            "paciente": "Paciente",
            "medico": "Médico Asignado",
            "fecha": "Fecha de la Cita",
            "hora": "Hora de la Cita",
            "motivo": "Motivo de Consulta",
            "estado": "Estado de la Cita",
            "observaciones": "Observaciones Adicionales",
        }
        widgets = {
            "paciente": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
            "medico": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
            "fecha": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "required": True}
            ),
            "hora": forms.TimeInput(
                attrs={"class": "form-control", "type": "time", "required": True}
            ),
            "motivo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Motivo de la consulta médica...",
                    "required": True,
                }
            ),
            "estado": forms.Select(
                attrs={"class": "form-control"}
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Notas u observaciones adicionales...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["paciente"].label_from_instance = lambda obj: f"{obj.nombres} {obj.apellidos} (C.I. {obj.cedula})"
        self.fields["medico"].label_from_instance = lambda obj: f"Dr. {obj.usuario.get_full_name() or obj.usuario.username} - {obj.especialidad.nombre}"

    def clean(self):
        cleaned_data = super().clean()

        if hasattr(self, '_errors') and forms.ALL_FIELDS in self._errors:

            filtered = [
                err for err in self._errors[forms.ALL_FIELDS]
                if "already exists" not in str(err)
            ]
            if filtered:
                self._errors[forms.ALL_FIELDS] = self.error_class(filtered)
            else:
                del self._errors[forms.ALL_FIELDS]

        medico = cleaned_data.get("medico")
        paciente = cleaned_data.get("paciente")
        fecha = cleaned_data.get("fecha")
        hora = cleaned_data.get("hora")

        if medico and fecha and hora:
            query = Cita.objects.filter(medico=medico, fecha=fecha, hora=hora)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                fecha_str = fecha.strftime('%d/%m/%Y')
                hora_str = hora.strftime('%H:%M')
                nombre_medico = f"Dr. {medico.usuario.get_full_name() or medico.usuario.username}"
                self.add_error(
                    None,
                    f"El {nombre_medico} ya tiene una cita ocupada el día {fecha_str} a las {hora_str}."
                )

        if paciente and fecha and hora:
            query = Cita.objects.filter(paciente=paciente, fecha=fecha, hora=hora)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                fecha_str = fecha.strftime('%d/%m/%Y')
                hora_str = hora.strftime('%H:%M')
                nombre_paciente = f"{paciente.nombres} {paciente.apellidos}"
                self.add_error(
                    None,
                    f"El paciente {nombre_paciente} ya tiene otra cita agendada el día {fecha_str} a las {hora_str}."
                )

        return cleaned_data
