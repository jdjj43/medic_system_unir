from django.db import models

from pacientes.models import Paciente
from medicos.models import Medico


class Cita(models.Model):

    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("ATENDIDA", "Atendida"),
        ("CANCELADA", "Cancelada"),
    ]


    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="citas"
    )

    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="citas"
    )

    fecha = models.DateField()

    hora = models.TimeField()

    motivo = models.TextField()


    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="PENDIENTE"
    )


    observaciones = models.TextField(
        blank=True,
        null=True
    )


    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "medico",
                    "fecha",
                    "hora"
                ],
                name="medico_no_duplique_hora"
            ),

            models.UniqueConstraint(
                fields=[
                    "paciente",
                    "fecha",
                    "hora"
                ],
                name="paciente_no_duplique_hora"
            ),

        ]


    def __str__(self):
        return f"{self.paciente} - {self.fecha}"