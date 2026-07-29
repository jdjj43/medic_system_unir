from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError

from .models import Paciente
from .forms import PacienteForm
from auditoria.utils import registrar_auditoria


@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by("-id")
    context = {
        "pacientes": pacientes
    }
    return render(
        request,
        "pacientes/lista_pacientes.html",
        context
    )


@login_required
def crear_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()

            registrar_auditoria(
                request=request,
                accion="Registró un paciente",
                modulo="Pacientes",
                descripcion=f"Se registró al paciente '{paciente.nombres} {paciente.apellidos}' (C.I. {paciente.cedula}).",
                objeto_id=paciente.id
            )

            messages.success(
                request,
                f"Paciente '{paciente.nombres} {paciente.apellidos}' registrado exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al registrar paciente: {errors}"
            )

    return redirect("lista_pacientes")


@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()

            registrar_auditoria(
                request=request,
                accion="Editó un paciente",
                modulo="Pacientes",
                descripcion=f"Se actualizaron los datos del paciente '{paciente.nombres} {paciente.apellidos}'.",
                objeto_id=paciente.id
            )

            messages.success(
                request,
                f"Datos del paciente '{paciente.nombres} {paciente.apellidos}' actualizados correctamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al actualizar paciente: {errors}"
            )

    return redirect("lista_pacientes")


@login_required
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == "POST":
        nombre_completo = f"{paciente.nombres} {paciente.apellidos}"
        paciente_id = paciente.id
        try:
            paciente.delete()

            registrar_auditoria(
                request=request,
                accion="Eliminó un paciente",
                modulo="Pacientes",
                descripcion=f"Se eliminó al paciente '{nombre_completo}'.",
                objeto_id=paciente_id
            )

            messages.success(
                request,
                f"Paciente '{nombre_completo}' eliminado exitosamente."
            )
        except ProtectedError:
            messages.error(
                request,
                f"No se puede eliminar al paciente '{nombre_completo}' porque posee citas o historias clínicas registradas."
            )

    return redirect("lista_pacientes")
