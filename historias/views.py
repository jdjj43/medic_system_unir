import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, ProtectedError

from .models import HistorialMedico, ArchivoMedico
from .forms import HistorialMedicoForm, ArchivoMedicoForm
from pacientes.models import Paciente
from citas.models import Cita
from auditoria.utils import registrar_auditoria


@login_required
def lista_historias(request):
    historias = HistorialMedico.objects.select_related(
        "paciente",
        "medico",
        "medico__usuario",
        "medico__especialidad",
        "cita"
    ).prefetch_related("archivos").all().order_by("-fecha")

    paciente_id = request.GET.get("paciente")
    search_query = request.GET.get("q", "").strip()
    paciente_filtrado = None

    if paciente_id:
        paciente_filtrado = get_object_or_404(Paciente, pk=paciente_id)
        historias = historias.filter(paciente=paciente_filtrado)

    if search_query:
        historias = historias.filter(
            Q(paciente__nombres__icontains=search_query) |
            Q(paciente__apellidos__icontains=search_query) |
            Q(paciente__cedula__icontains=search_query) |
            Q(diagnostico__icontains=search_query)
        )

    form_historial = HistorialMedicoForm()
    form_archivo = ArchivoMedicoForm()
    pacientes = Paciente.objects.all().order_by("apellidos", "nombres")
    citas_disponibles = Cita.objects.filter(historialmedico__isnull=True).select_related("paciente", "medico", "medico__usuario")

    context = {
        "historias": historias,
        "pacientes": pacientes,
        "paciente_filtrado": paciente_filtrado,
        "search_query": search_query,
        "form_historial": form_historial,
        "form_archivo": form_archivo,
        "citas_disponibles": citas_disponibles,
    }
    return render(
        request,
        "historias/lista_historias.html",
        context
    )


@login_required
def crear_historia(request):
    if request.method == "POST":
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            historial = form.save()

            if historial.cita and hasattr(historial.cita, "estado"):
                historial.cita.estado = "COMPLETADA"
                historial.cita.save()

            if "archivo" in request.FILES and request.POST.get("tipo"):
                archivo_form = ArchivoMedicoForm(request.POST, request.FILES)
                if archivo_form.is_valid():
                    archivo_obj = archivo_form.save(commit=False)
                    archivo_obj.historial = historial
                    archivo_obj.save()


            registrar_auditoria(
                request=request,
                accion="Creó una historia clínica",
                modulo="Historias clínicas",
                descripcion=f"Se registró la historia clínica para el paciente '{historial.paciente.nombres} {historial.paciente.apellidos}'.",
                objeto_id=historial.id
            )

            messages.success(
                request,
                f"Historia clínica para '{historial.paciente.nombres} {historial.paciente.apellidos}' registrada exitosamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al registrar historia clínica: {errors}"
            )

    paciente_id = request.POST.get("paciente") or request.GET.get("paciente")
    if paciente_id:
        return redirect(f"/historias/lista/?paciente={paciente_id}")
    return redirect("lista_historias")


@login_required
def editar_historia(request, pk):
    historial = get_object_or_404(HistorialMedico, pk=pk)

    if request.method == "POST":
        form = HistorialMedicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()

            registrar_auditoria(
                request=request,
                accion="Modificó una historia clínica",
                modulo="Historias clínicas",
                descripcion=f"Se actualizó la historia clínica #{historial.id} del paciente '{historial.paciente.nombres} {historial.paciente.apellidos}'.",
                objeto_id=historial.id
            )

            messages.success(
                request,
                f"Historia clínica del paciente '{historial.paciente.nombres} {historial.paciente.apellidos}' actualizada correctamente."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al actualizar la historia clínica: {errors}"
            )

    paciente_id = request.GET.get("paciente")
    if paciente_id:
        return redirect(f"/historias/lista/?paciente={paciente_id}")
    return redirect("lista_historias")


@login_required
def eliminar_historia(request, pk):
    historial = get_object_or_404(HistorialMedico, pk=pk)

    if request.method == "POST":
        paciente_nombre = f"{historial.paciente.nombres} {historial.paciente.apellidos}"
        historial_id = historial.id
        try:
            historial.delete()

            registrar_auditoria(
                request=request,
                accion="Eliminó una historia clínica",
                modulo="Historias clínicas",
                descripcion=f"Se eliminó la historia clínica #{historial_id} del paciente '{paciente_nombre}'.",
                objeto_id=historial_id
            )

            messages.success(
                request,
                f"Historia clínica de '{paciente_nombre}' eliminada exitosamente."
            )
        except ProtectedError:
            messages.error(
                request,
                f"No se puede eliminar la historia clínica de '{paciente_nombre}' porque contiene registros protegidos."
            )

    paciente_id = request.GET.get("paciente")
    if paciente_id:
        return redirect(f"/historias/lista/?paciente={paciente_id}")
    return redirect("lista_historias")


@login_required
def subir_archivo(request, pk):
    historial = get_object_or_404(HistorialMedico, pk=pk)

    if request.method == "POST":
        form = ArchivoMedicoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.historial = historial
            archivo.save()

            registrar_auditoria(
                request=request,
                accion="Adjuntó documento médico",
                modulo="Historias clínicas",
                descripcion=f"Se adjuntó el archivo '{archivo.tipo}' a la historia clínica del paciente '{historial.paciente.nombres} {historial.paciente.apellidos}'.",
                objeto_id=historial.id
            )

            messages.success(
                request,
                f"Documento '{archivo.tipo}' subido correctamente a la historia clínica de '{historial.paciente.nombres}'."
            )
        else:
            errors = " ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
            messages.error(
                request,
                f"Error al subir archivo: {errors}"
            )

    paciente_id = request.GET.get("paciente")
    if paciente_id:
        return redirect(f"/historias/lista/?paciente={paciente_id}")
    return redirect("lista_historias")


@login_required
def eliminar_archivo(request, pk):
    archivo = get_object_or_404(ArchivoMedico, pk=pk)
    historial = archivo.historial

    if request.method == "POST":
        nombre_archivo = archivo.tipo
        archivo_id = archivo.id
        if archivo.archivo and os.path.isfile(archivo.archivo.path):
            try:
                os.remove(archivo.archivo.path)
            except OSError:
                pass
        archivo.delete()

        registrar_auditoria(
            request=request,
            accion="Eliminó documento médico",
            modulo="Historias clínicas",
            descripcion=f"Se eliminó el documento '{nombre_archivo}' de la historia clínica del paciente '{historial.paciente.nombres} {historial.paciente.apellidos}'.",
            objeto_id=archivo_id
        )

        messages.success(
            request,
            f"Archivo '{nombre_archivo}' eliminado de la historia clínica."
        )

    paciente_id = request.GET.get("paciente")
    if paciente_id:
        return redirect(f"/historias/lista/?paciente={paciente_id}")
    return redirect("lista_historias")
