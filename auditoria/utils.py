from .models import Auditoria


def obtener_ip(request):
    if not request:
        return None

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def registrar_auditoria(request, accion, modulo, descripcion, objeto_id=None):
    try:
        usuario = None
        if request and hasattr(request, "user") and request.user.is_authenticated:
            usuario = request.user

        direccion_ip = obtener_ip(request) if request else None

        return Auditoria.objects.create(
            usuario=usuario,
            accion=accion,
            modulo=modulo,
            descripcion=descripcion,
            direccion_ip=direccion_ip,
            objeto_id=objeto_id,
        )
    except Exception as e:
        print(f"Error al registrar auditoría: {e}")
        return None
