from django.shortcuts import render
from django.http import Http404

# Create your views here

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Tarea
from django.db.models.functions import ExtractYear, ExtractMonth

import pandas as pd
import numpy as np


def index(request):
    return render(request, "tareas/index.html")


# Vamos a crear una funcion externa para no repetir codigo
def obtener_datos_dashboard(año, mes):
    # Ahora vamos cogiendo los datos para el mes y año por defecto, primero todas las tareas de ese mes y año
    tareas_mes = Tarea.objects.filter(fecha__year=año, fecha__month=mes)
    df = pd.DataFrame.from_records(tareas_mes.values())

    if df.empty:
        return{
            "año": año,
            "mes": mes,
            "sin_datos": True,
        }
    # Sacamos los que hicieron mayor numero de tareas y el que hizo menos

    
    suma_tareas = df.groupby('persona').size().reset_index(name='num_tareas')
    top_3_tareas = suma_tareas.nlargest(3, 'num_tareas')

    print(top_3_tareas)
    
    ganador1_tareas = (top_3_tareas["persona"].iloc[0] if len(top_3_tareas) > 0 else None,
                          top_3_tareas["num_tareas"].iloc[0] if len(top_3_tareas) > 0 else None)
    
    ganador2_tareas = (top_3_tareas["persona"].iloc[1] if len(top_3_tareas) > 1 else None,
                          top_3_tareas["num_tareas"].iloc[1] if len(top_3_tareas) > 1 else None)
    
    ganador3_tareas = (top_3_tareas["persona"].iloc[2] if len(top_3_tareas) > 2 else None,
                          top_3_tareas["num_tareas"].iloc[2] if len(top_3_tareas) > 2 else None)
    
    perdedor_tareas = (suma_tareas.nsmallest(1, 'num_tareas')["persona"].iloc[0] if not suma_tareas.empty else None,
                       suma_tareas.nsmallest(1, 'num_tareas')["num_tareas"].iloc[0] if not suma_tareas.empty else None)

    # Sacamos los ganadores por puntos ponderando las tareas
    df['puntos'] = (
        df['pone_mesa'].astype(int) * 1 +
        df['quita_mesa'].astype(int) * 1 +
        df['mete_lava'].astype(int) * 1 +
        df['saca_lava'].astype(int) * 1 +
        (df['era_mi_turno'] == False).astype(int) * 2 +
        df['num_fregados'] * 0.5
    )

    suma_ptos = df.groupby('persona')['puntos'].sum().reset_index()
    top_3_ptos = suma_ptos.nlargest(3, 'puntos')

    ganador1_pts = (top_3_ptos["persona"].iloc[0] if len(top_3_ptos) > 0 else None,
                          top_3_ptos["puntos"].iloc[0] if len(top_3_ptos) > 0 else None)
    
    ganador2_pts = (top_3_ptos["persona"].iloc[1] if len(top_3_ptos) > 1 else None,
                          top_3_ptos["puntos"].iloc[1] if len(top_3_ptos) > 1 else None)
    
    ganador3_pts = (top_3_ptos["persona"].iloc[2] if len(top_3_ptos) > 2 else None,
                          top_3_ptos["puntos"].iloc[2] if len(top_3_ptos) > 2 else None)

    perdedor_pts = (suma_ptos.nsmallest(1, 'puntos')["persona"].iloc[0] if not suma_ptos.empty else None,
                       suma_ptos.nsmallest(1, 'puntos')["puntos"].iloc[0] if not suma_ptos.empty else None)


    # Sacamos ganadores por categorias ( cacharros, poner mesa, quitar mesa, etc)

    suma_cacharros = df.groupby('persona')['num_fregados'].sum().reset_index()
    ganador_cacharros = (suma_cacharros.nlargest(1, 'num_fregados')["persona"].iloc[0] if not suma_cacharros.empty else None,
                            suma_cacharros.nlargest(1, 'num_fregados')["num_fregados"].iloc[0] if not suma_cacharros.empty else None)
    
    perdedor_cacharros = (suma_cacharros.nsmallest(1, 'num_fregados')["persona"].iloc[0] if not suma_cacharros.empty else None,
                            suma_cacharros.nsmallest(1, 'num_fregados')["num_fregados"].iloc[0] if not suma_cacharros.empty else None)

    suma_poner_mesa = df.groupby('persona')['pone_mesa'].sum().reset_index()
    ganador_poner_mesa = (suma_poner_mesa.nlargest(1, 'pone_mesa')["persona"].iloc[0] if not suma_poner_mesa.empty else None,
                            suma_poner_mesa.nlargest(1, 'pone_mesa')["pone_mesa"].iloc[0] if not suma_poner_mesa.empty else None)
    perdedor_poner_mesa = (suma_poner_mesa.nsmallest(1, 'pone_mesa')["persona"].iloc[0] if not suma_poner_mesa.empty else None,
                            suma_poner_mesa.nsmallest(1, 'pone_mesa')["pone_mesa"].iloc[0] if not suma_poner_mesa.empty else None)

    suma_quitar_mesa = df.groupby('persona')['quita_mesa'].sum().reset_index()
    ganador_quitar_mesa = (suma_quitar_mesa.nlargest(1, 'quita_mesa')["persona"].iloc[0] if not suma_quitar_mesa.empty else None,
                            suma_quitar_mesa.nlargest(1, 'quita_mesa')["quita_mesa"].iloc[0] if not suma_quitar_mesa.empty else None)
    perdedor_quitar_mesa = (suma_quitar_mesa.nsmallest(1, 'quita_mesa')["persona"].iloc[0] if not suma_quitar_mesa.empty else None,
                            suma_quitar_mesa.nsmallest(1, 'quita_mesa')["quita_mesa"].iloc[0] if not suma_quitar_mesa.empty else None)

    suma_mete_lava = df.groupby('persona')['mete_lava'].sum().reset_index()
    ganador_mete_lava = (suma_mete_lava.nlargest(1, 'mete_lava')["persona"].iloc[0] if not suma_mete_lava.empty else None,
                            suma_mete_lava.nlargest(1, 'mete_lava')["mete_lava"].iloc[0] if not suma_mete_lava.empty else None)
    perdedor_mete_lava = (suma_mete_lava.nsmallest(1, 'mete_lava')["persona"].iloc[0] if not suma_mete_lava.empty else None,
                            suma_mete_lava.nsmallest(1, 'mete_lava')["mete_lava"].iloc[0] if not suma_mete_lava.empty else None)

    suma_saca_lava = df.groupby('persona')['saca_lava'].sum().reset_index()
    ganador_saca_lava = (suma_saca_lava.nlargest(1, 'saca_lava')["persona"].iloc[0] if not suma_saca_lava.empty else None,
                            suma_saca_lava.nlargest(1, 'saca_lava')["saca_lava"].iloc[0] if not suma_saca_lava.empty else None)
    perdedor_saca_lava = (suma_saca_lava.nsmallest(1, 'saca_lava')["persona"].iloc[0] if not suma_saca_lava.empty else None,
                            suma_saca_lava.nsmallest(1, 'saca_lava')["saca_lava"].iloc[0] if not suma_saca_lava.empty else None)

    context = {
        "año": año,
        "mes": mes,
        "ganador1_tareas": ganador1_tareas,
        "ganador2_tareas": ganador2_tareas,
        "ganador3_tareas": ganador3_tareas,
        "perdedor_tareas": perdedor_tareas,
        "ganador1_ptos": ganador1_pts,
        "ganador2_ptos": ganador2_pts,
        "ganador3_ptos": ganador3_pts,
        "perdedor_ptos": perdedor_pts,
        "ganador_cacharros": ganador_cacharros,
        "perdedor_cacharros": perdedor_cacharros,
        "ganador_poner_mesa": ganador_poner_mesa,
        "perdedor_poner_mesa": perdedor_poner_mesa,
        "ganador_quitar_mesa": ganador_quitar_mesa,
        "perdedor_quitar_mesa": perdedor_quitar_mesa,
        "ganador_mete_lava": ganador_mete_lava,
        "perdedor_mete_lava": perdedor_mete_lava,
        "ganador_saca_lava": ganador_saca_lava,
        "perdedor_saca_lava": perdedor_saca_lava,
        "sin_datos": False
    }

    return context

# NECESARIO HACER DATOS SINTETICOS PARA PROBAR
def dashboard(request):

    # Seleccionar mes y calcular lo siguientes datos:

        # Sacar quien 3 personas que hicieoron mas tareas
        # Sacar quien hizo menos tareas
        # Dar una puntuacion segun la ponderacion de las tareas (disintos campos de la tarea
        # Ver quien frego mas cacharros

    if request.method == 'POST':
        año = int(request.POST.get('year', '').strip())
        mes = int(request.POST.get('month', '').strip())

        años = (Tarea.objects
            .annotate(year=ExtractYear("fecha"))
            .values_list("year", flat=True)
            .distinct()
            .order_by("year"))
        meses = (Tarea.objects
            .filter(fecha__year=año)
            .annotate(month=ExtractMonth("fecha"))
            .values_list("month", flat=True)
            .distinct()
            .order_by("month"))
        
        if not mes or not año:
            return render(request, "tareas/dashboard.html", {"error": "El mes y el año son obligatorios."})
        
        if mes not in meses:
            return render(request, "tareas/dashboard.html", {"error": "El mes no es válido."})
        
        if año not in años:
            return render(request, "tareas/dashboard.html", {"error": "El año no es válido."})
    
        context = obtener_datos_dashboard(año, mes)
        context["años"] = años
        context["meses"] = meses
        context["selected_year"] = año
        context["selected_month"] = mes

        return render(request, "tareas/dashboard.html", context=context)
    
    # Renderizamos cuando el metodo es GET
    # Hacemos un map de los meses:
    meses_map = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
                 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

    # Primero sacamos los años y meses disponibles con el ORM de Django, para que las consultas no dependan de la bbdd
    años = (Tarea.objects
        .annotate(year=ExtractYear("fecha"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("year"))

    año_default = años.last() if años else None
    meses = (Tarea.objects
        .filter(fecha__year=año_default)
        .annotate(month=ExtractMonth("fecha"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("month"))

    mes_default = meses.last() if meses else None
    print("XDDDDDDDDDDDDDDDDDd")
    print(list(años))
    print(list(meses))

    context = obtener_datos_dashboard(año_default, mes_default)
    context["años"] = list(años)
    context["meses"] = list(meses)

    return render(request, "tareas/dashboard.html", context=context)


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
