from django.db import models
from django.conf import settings


class Auditoria(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registros_auditoria"
    )

    accion = models.CharField(
        max_length=100
    )

    modulo = models.CharField(
        max_length=50
    )

    descripcion = models.TextField()

    fecha_hora = models.DateTimeField(
        auto_now_add=True
    )

    direccion_ip = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    objeto_id = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "-fecha_hora"
        ]
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"

    def __str__(self):
        usr = self.usuario.username if self.usuario else "Sistema/Anónimo"
        return f"[{self.fecha_hora.strftime('%d/%m/%Y %H:%M')}] {usr} - {self.accion} ({self.modulo})"