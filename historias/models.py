from django.db import models

from pacientes.models import Paciente
from medicos.models import Medico
from citas.models import Cita

class HistorialMedico(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="historial"
    )


    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT
    )


    cita = models.OneToOneField(
        Cita,
        on_delete=models.PROTECT
    )


    fecha = models.DateTimeField(
        auto_now_add=True
    )


    diagnostico = models.TextField()

    sintomas = models.TextField(
        blank=True
    )

    tratamiento = models.TextField(
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )


    def __str__(self):
        return f"Historial {self.paciente}"
    
class ArchivoMedico(models.Model):

    historial = models.ForeignKey(
        HistorialMedico,
        on_delete=models.CASCADE,
        related_name="archivos"
    )

    archivo = models.FileField(
        upload_to="archivos_medicos/"
    )

    tipo = models.CharField(
        max_length=50
    )

    fecha_subida = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.tipo