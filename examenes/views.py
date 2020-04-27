from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Examen
from .utils import pregunta_html, crear_pregunta, calificacion_final, respuesta_opcional, custom_alumno_respuesta
from .soluciones import respuesta_correcta
from .check import respuesta_correcta_check
from google_api.google_api import existe_cuenta, google_cuentas, google_cuentas_tema, agregar_calificacion, existe_calificacion


def examenes_list(request):
    """"""
    examenes = Examen.objects.all()
    return render(request, 'examenes/list.html', {'examenes': examenes})

def examen_detail(request, examen_id):
    """"""

    examen_query = Examen.objects.get(id=examen_id)
    preguntas = [pregunta.strip() for pregunta in examen_query.preguntas.split("--")][:-1]
    respuestas = [respuesta.strip() for respuesta in examen_query.respuestas.split("--")][:-1]
    opciones = [opcion.strip() for opcion in examen_query.opcional.split("--")][:-1]
    crear_preguntas = [opcion.strip() for opcion in examen_query.crear_pregunta.split("--")][:-1]

    examen = dict()
    examen.update({"tema": examen_query.tema, "id": examen_query.id })

    examen.update({"preguntas": [], })
    for index in range(0,len(preguntas)):
        # Crea la respuesta aleatoria
        if not crear_preguntas[index]:
            pregunta = crear_pregunta['default'](preguntas[index])
            html_pregunta = pregunta_html['default'](pregunta)
            default = True
        else:
            pregunta = crear_pregunta[crear_preguntas[index]](preguntas[index])
            html_pregunta = pregunta_html[crear_preguntas[index]](pregunta)
            default = False

        # Crea la respuesta opcionales, si es necesario
        respuesta = respuestas[index]
        opcional = opciones[index]
        custom_respuestas = []
        if opcional:
            if default:
                resp_correcta = respuesta_correcta[respuesta](pregunta)
                custom_respuestas, default = respuesta_opcional[opcional](resp_correcta)
            else:
                custom_respuestas, default = respuesta_opcional[opcional]()

        examen["preguntas"].append((html_pregunta, custom_respuestas, index + 1, pregunta, default))

    # Google API info
    cuentas = google_cuentas()
    cuentas_con_calificacion = google_cuentas_tema(examen_query.tema)

    return render(request, 'examenes/detail.html', {'examen': examen, 'ctas_tema': cuentas_con_calificacion, 'cuentas': cuentas})


def check_examen(request):
    """"""
    if request.method == "POST":
        numero_cuenta = request.POST['numero_cuenta']
        tema = request.POST['tema']
        existe_cta = existe_cuenta(numero_cuenta)

        if not existe_cta:
            return render(request, 'examenes/noexiste.html', {'numero_cuenta': numero_cuenta, 'existe_cuenta': existe_cta})

        if existe_calificacion(numero_cuenta, tema):
            return render(request, 'examenes/noexiste.html', {'numero_cuenta': numero_cuenta, 'existe_cuenta': existe_cta})

        solucion = dict()
        solucion.update({"tema": tema, "tiempo": request.POST['tiempo']})

        examen_query = Examen.objects.get(tema=request.POST['tema'])
        respuestas = [respuesta.strip() for respuesta in examen_query.respuestas.split("--")][:-1]

        solucion.update({"examen_result": [], })
        calificacion = []
        google_api_preguntas = []
        for index in range(0,len(respuestas)):
            respuesta = respuestas[index]
            pregunta_html = request.POST[f'pregunta{index+1}']
            pregunta_latex = request.POST[f'pregunta_latex{index+1}']
            alumno_respuesta = request.POST.get(f'{index+1}', False)
            if not alumno_respuesta:
                faltan_respuestas = True
                respuestas_parciales = []
                i = 1
                while faltan_respuestas:
                    respuesta_parcial = request.POST.get(f'{index+1}-{i}',False)
                    if respuesta_parcial == 'no_stop_here':
                        pass
                    elif respuesta_parcial:
                        respuestas_parciales.append(respuesta_parcial)
                    else:
                        faltan_respuestas = False
                    i = i + 1
                alumno_respuesta = respuestas_parciales

            resp_correcta_html = respuesta_correcta[respuesta](pregunta_html, html=True)
            resp_correcta = respuesta_correcta[respuesta](pregunta_html)
            check_resp = respuesta_correcta_check[respuesta](resp_correcta, alumno_respuesta)
            alumno_respuesta_aux = request.POST.get(f'{index+1}',False)
            if not alumno_respuesta_aux:
                alumno_respuesta = custom_alumno_respuesta[respuesta](alumno_respuesta)
            solucion["examen_result"].append((pregunta_latex, resp_correcta_html, alumno_respuesta, check_resp))
            google_api_preguntas.append(pregunta_latex)
            google_api_preguntas.append(resp_correcta_html)
            google_api_preguntas.append(alumno_respuesta)
            google_api_preguntas.append(check_resp)
            calificacion.append(check_resp)


        agregar_calificacion(request.POST['tema'], numero_cuenta, calificacion_final(calificacion), request.POST['tiempo'], google_api_preguntas)
        return render(request, 'examenes/solucion.html', {'solucion': solucion, "calificacion_final": calificacion_final(calificacion), 'numero_cuenta': numero_cuenta, 'existe_cuenta': existe_cta})

def credits_page(request):
    """"""
    return render(request, 'misc/credits.html')
