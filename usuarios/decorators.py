from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorador que restringe el acceso a una vista solo a usuarios con rol ADMIN.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.rol != "ADMIN":
            messages.error(
                request,
                "Acceso denegado: Solo los usuarios con rol de Administrador pueden acceder a este módulo."
            )
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
