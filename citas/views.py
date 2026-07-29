from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .models import Cita
from .forms import CitaForm
from medicos.models import Medico
from auditoria.utils import registrar_auditoria


@login_required
def lista_citas(request):
    citas = Cita.objects.select_related("paciente", "medico", "medico__usuario", "medico__especialidad").all().order_by("-fecha", "-hora")
    
    medico_id = request.GET.get("medico")
    medico_filtrado = None

    if medico_id:
        medico_filtrado = get_object_or_404(Medico, pk=medico_id)
        citas = citas.filter(medico=medico_filtrado)

    form_cita = CitaForm()
    if medico_filtrado:
        form_cita.initial["medico"] = medico_filtrado.id

    context = {
        "citas": citas,
        "medico_filtrado": medico_filtrado,
        "form_cita": form_cita,
    }
    return render(
        request,
        "citas/lista_citas.html",
        context
    )


@login_required
def crear_cita(request):
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            try:
                cita = form.save()

                registrar_auditoria(
                    request=request,
                    accion="Registró una cita",
                    modulo="Citas",
                    descripcion=f"Se agendó cita médica para '{cita.paciente.nombres} {cita.paciente.apellidos}' con Dr. '{cita.medico.usuario.get_full_name() or cita.medico.usuario.username}'.",
                    objeto_id=cita.id
                )

                messages.success(
                    request,
                    f"Cita médica para '{cita.paciente.nombres} {cita.paciente.apellidos}' agendada exitosamente."
                )
            except IntegrityError:
                messages.error(
                    request,
                    "Conflicto de horario: El médico o paciente ya posee una cita registrada a esa misma fecha y hora."
                )
        else:
            error_list = []
            for field, errs in form.errors.items():
                for err in errs:
                    err_str = str(err)
                    if "already exists" not in err_str:
                        error_list.append(err_str)
            
            msg = " ".join(error_list) if error_list else "Error al agendar la cita. Verifica los datos."
            messages.error(request, msg)

    medico_id = request.POST.get("medico") or request.GET.get("medico")
    if medico_id:
        return redirect(f"/citas/lista/?medico={medico_id}")
    return redirect("lista_citas")


@login_required
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)

    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                form.save()

                registrar_auditoria(
                    request=request,
                    accion="Modificó una cita",
                    modulo="Citas",
                    descripcion=f"Se modificaron los datos de la cita médica #{cita.id} del paciente '{cita.paciente.nombres} {cita.paciente.apellidos}'.",
                    objeto_id=cita.id
                )

                messages.success(
                    request,
                    "Cita médica actualizada correctamente."
                )
            except IntegrityError:
                messages.error(
                    request,
                    "Conflicto de horario: El médico o paciente ya posee una cita registrada a esa misma fecha y hora."
                )
        else:
            error_list = []
            for field, errs in form.errors.items():
                for err in errs:
                    err_str = str(err)
                    if "already exists" not in err_str:
                        error_list.append(err_str)
            
            msg = " ".join(error_list) if error_list else "Error al actualizar la cita. Verifica los datos."
            messages.error(request, msg)

    medico_id = request.GET.get("medico")
    if medico_id:
        return redirect(f"/citas/lista/?medico={medico_id}")
    return redirect("lista_citas")


@login_required
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)

    if request.method == "POST":
        paciente_nombre = f"{cita.paciente.nombres} {cita.paciente.apellidos}"
        cita_id = cita.id

        registrar_auditoria(
            request=request,
            accion="Canceló una cita",
            modulo="Citas",
            descripcion=f"Se canceló y eliminó la cita médica #{cita_id} del paciente '{paciente_nombre}'.",
            objeto_id=cita_id
        )

        cita.delete()

        messages.success(
            request,
            f"Cita del paciente '{paciente_nombre}' cancelada y eliminada exitosamente."
        )

    medico_id = request.GET.get("medico")
    if medico_id:
        return redirect(f"/citas/lista/?medico={medico_id}")
    return redirect("lista_citas")
