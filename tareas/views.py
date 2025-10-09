from django.shortcuts import render
from django.http import Http404

# Create your views here

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Tarea


def index(request):
    return render(request, "tareas/index.html")

""""
def tarea_info(request, tarea_id):
    try:
        tarea = Tarea.objects.get(pk=tarea_id)
    except Tarea.DoesNotExist:
        raise Http404("Question does not exist")
    campos = Tarea._meta.get_fields()
    return render(request, "tareas/tarea_info.html", {"tarea": tarea, "campos": campos})
"""

# Tus categorías deben coincidir con el modelo
CATEGORIAS_VALIDAS = {"CENA", "COMIDA"}
PERSONAS_VALIDAS = {"Miguel", "David", "Pablo", "Raquel", "Miriam", "Papa", "Mama", "Lolo"}


def guardar_tarea(request):
    print(request.method)
    if request.method == 'POST':
        persona = request.POST.get('persona', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha = request.POST.get('fecha', '').strip()
        tarea = request.POST.get('tarea', '').strip()
        pone_mesa = request.POST.get('pone_mesa', '').strip()
        quita_mesa = request.POST.get('quita_mesa', '').strip()
        mete_lava = request.POST.get('mete_lava', '').strip()
        saca_lava = request.POST.get('saca_lava', '').strip()
        era_mi_turno = request.POST.get('era_mi_turno', '').strip()
        num_fregados_str = request.POST.get('num_fregados', '').strip()  # ✅ corregido

        errors = {}

        if not persona:
            errors['persona'] = 'La persona es obligatoria.'
        elif persona not in PERSONAS_VALIDAS:
            errors['persona'] = 'Persona no válida.'

        if not descripcion:
            errors['descripcion'] = 'La descripción es obligatoria.'

        if tarea not in CATEGORIAS_VALIDAS:
            errors['tarea'] = 'Tarea no válida.'

        try:
            num_fregados = int(num_fregados_str)
            if not (1 <= num_fregados <= 5):
                errors['num_fregados'] = 'El número de cacharros debe estar entre 1 y 5.'
        except ValueError:
            errors['num_fregados'] = 'El número de cacharros fregados debe ser un entero.'

        if errors:
            context = {
                'errors': errors,
                'initial': {
                    'persona': persona,
                    'descripcion': descripcion,
                    'tarea': tarea,
                    'pone_mesa': pone_mesa,
                    'quita_mesa': quita_mesa,
                    'mete_lava': mete_lava,
                    'saca_lava': saca_lava,
                    "era_mi_turno": era_mi_turno,
                    'num_fregados': num_fregados_str,
                },
                'tareas': [
                    ('CENA', 'Cena'),
                    ('COMIDA', 'Comida'),
                ],
                "personas": [
                    'Miguel', 'David', 'Pablo', 'Raquel', 'Miriam', 'Papa', 'Mama', 'Lolo'
                ]
            }
            request.session["name"] = persona
            return render(request, 'tareas/guardar_tarea.html', context)

        print(request.POST)
        Tarea.objects.create(
            persona=persona,
            descripcion=descripcion,
            tarea=tarea,
            pone_mesa=(pone_mesa == 'on'),
            quita_mesa=(quita_mesa == 'on'),
            mete_lava=(mete_lava == 'on'),
            saca_lava=(saca_lava == 'on'),
            era_mi_turno=(era_mi_turno == 'on'),
            num_fregados=num_fregados,
        )

        request.session["name"] = persona
        return redirect("tareas:post_guardar")

    context = {
        'tareas': [
            ('CENA', 'Cena'),
            ('COMIDA', 'Comida'),
        ],
        "personas": [
            'Miguel', 'David', 'Pablo', 'Raquel', 'Miriam', 'Papa', 'Mama', 'Lolo'
        ],
    }
    return render(request, 'tareas/guardar_tarea.html', context)


def post_guardar(request):
    nombre = request.session.pop("name", None)
    return render(request, "tareas/post_guardar.html", {"name": nombre})  # ✅ corregido
