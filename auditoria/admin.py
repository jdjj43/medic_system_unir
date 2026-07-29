from django.contrib import admin
from .models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):

    list_display = (
        "fecha_hora",
        "usuario",
        "accion",
        "modulo",
        "direccion_ip",
        "objeto_id",
        "activo",
    )

    list_filter = (
        "modulo",
        "fecha_hora",
        "activo",
    )

    search_fields = (
        "accion",
        "modulo",
        "descripcion",
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "direccion_ip",
    )

    readonly_fields = [f.name for f in Auditoria._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
