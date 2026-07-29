from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError, Count

from .models import Especialidad, Medico
from .forms import EspecialidadForm, MedicoForm




@login_required
def lista_especialidades(request):

    especialidades = Especialidad.objects.annotate(
        num_medicos=Count("medicos")
    ).order_by("nombre")

    context = {
        "especialidades": especialidades
    }

    return render(
        request,
        "especialidades/lista.html",
        context
    )


@login_required
def crear_especialidad(request):

    if request.method == "POST":
        form = EspecialidadForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Especialidad creada exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al crear especialidad: {errors}"
            )

    return redirect("lista_especialidades")


@login_required
def editar_especialidad(request, pk):

    especialidad = get_object_or_404(Especialidad, pk=pk)

    if request.method == "POST":
        form = EspecialidadForm(request.POST, instance=especialidad)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Especialidad actualizada exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al actualizar especialidad: {errors}"
            )

    return redirect("lista_especialidades")


@login_required
def eliminar_especialidad(request, pk):

    especialidad = get_object_or_404(Especialidad, pk=pk)

    if request.method == "POST":
        try:
            especialidad.delete()
            messages.success(
                request,
                "Especialidad eliminada exitosamente."
            )
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar la especialidad porque tiene médicos asociados."
            )

    return redirect("lista_especialidades")




@login_required
def lista_medicos(request):
    medicos = Medico.objects.select_related("usuario", "especialidad").all().order_by("usuario__first_name")
    form_medico = MedicoForm()
    context = {
        "medicos": medicos,
        "form_medico": form_medico
    }
    return render(
        request,
        "medicos/lista_medicos.html",
        context
    )


@login_required
def crear_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            medico = form.save()
            messages.success(
                request,
                f"Médico Dr. {medico.usuario.get_full_name() or medico.usuario.username} registrado exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al registrar médico: {errors}"
            )

    return redirect("lista_medicos")


@login_required
def editar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == "POST":
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Información del médico actualizada exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al actualizar médico: {errors}"
            )

    return redirect("lista_medicos")


@login_required
def eliminar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == "POST":
        nombre_medico = f"Dr. {medico.usuario.get_full_name() or medico.usuario.username}"
        try:
            medico.delete()
            messages.success(
                request,
                f"Registro del médico '{nombre_medico}' eliminado exitosamente."
            )
        except ProtectedError:
            messages.error(
                request,
                f"No se puede eliminar el registro del médico '{nombre_medico}' porque posee citas o historias clínicas vinculadas."
            )

    return redirect("lista_medicos")
