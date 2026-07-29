from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, UsuarioCrearForm, UsuarioEditarForm
from .models import Usuario
from .decorators import admin_required
from auditoria.utils import registrar_auditoria


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            usuario = authenticate(
                request,
                username=username,
                password=password
            )

            if usuario:

                login(
                    request,
                    usuario
                )

                registrar_auditoria(
                    request=request,
                    accion="Inicio de sesión",
                    modulo="Autenticación",
                    descripcion=f"El usuario '{usuario.username}' inició sesión exitosamente.",
                    objeto_id=usuario.id
                )

                return redirect(
                    "dashboard"
                )

    else:
        form = LoginForm()

    return render(
        request,
        "usuarios/login.html",
        {
            "form": form
        }
    )


def logout_view(request):

    if request.user.is_authenticated:
        registrar_auditoria(
            request=request,
            accion="Cierre de sesión",
            modulo="Autenticación",
            descripcion=f"El usuario '{request.user.username}' cerró su sesión.",
            objeto_id=request.user.id
        )

    logout(request)

    return redirect(
        "login"
    )


@login_required
def dashboard(request):
    return render(
        request,
        "usuarios/dashboard.html"
    )


@admin_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by("username")
    context = {
        "usuarios": usuarios
    }
    return render(
        request,
        "usuarios/lista_usuarios.html",
        context
    )


@admin_required
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            registrar_auditoria(
                request=request,
                accion="Creó un usuario",
                modulo="Usuarios",
                descripcion=f"El usuario '{request.user.username}' creó al usuario '{usuario.username}' con rol '{usuario.rol}'.",
                objeto_id=usuario.id
            )

            messages.success(
                request,
                f"Usuario '{usuario.username}' creado exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al crear usuario: {errors}"
            )

    return redirect("lista_usuarios")


@admin_required
def editar_usuario(request, pk):
    usuario_obj = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioEditarForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            form.save()

            registrar_auditoria(
                request=request,
                accion="Editó un usuario",
                modulo="Usuarios",
                descripcion=f"El usuario '{request.user.username}' editó los datos del usuario '{usuario_obj.username}'.",
                objeto_id=usuario_obj.id
            )

            messages.success(
                request,
                f"Usuario '{usuario_obj.username}' actualizado correctamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al actualizar usuario: {errors}"
            )

    return redirect("lista_usuarios")


@admin_required
def eliminar_usuario(request, pk):
    usuario_obj = get_object_or_404(Usuario, pk=pk)

    if usuario_obj == request.user:
        messages.error(
            request,
            "No puedes eliminar tu propio usuario mientras estás autenticado."
        )
        return redirect("lista_usuarios")

    if request.method == "POST":
        nombre_usuario = usuario_obj.username
        user_id = usuario_obj.id

        registrar_auditoria(
            request=request,
            accion="Desactivó un usuario",
            modulo="Usuarios",
            descripcion=f"El usuario '{request.user.username}' desactivo/eliminó al usuario '{nombre_usuario}'.",
            objeto_id=user_id
        )

        usuario_obj.delete()

        messages.success(
            request,
            f"Usuario '{nombre_usuario}' eliminado exitosamente."
        )

    return redirect("lista_usuarios")