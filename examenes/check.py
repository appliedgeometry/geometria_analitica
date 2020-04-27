import sympy


def check_inversa_matriz(resp_correcta, alumno_respuesta):
    """"""
    sympy_obj = resp_correcta
    try:
        resp_correcta = sympy_obj.inv()
    except:
        resp_correcta = sympy.Matrix([
            [0, 0],
            [0, 0]
        ])

    if sympy_obj.is_zero:
        if alumno_respuesta == 'Sin inversa':
            return 1
        else:
            return 0
    else:
        if alumno_respuesta == f'${sympy.latex(sympy_obj)}$':
            return 1
        else:
            return 0

def check_det_matriz(resp_correcta, alumno_respuesta):
    """"""
    if int(alumno_respuesta) == int(resp_correcta):
        return 1
    else:
        return 0

def check_superficies_regladas(resp_correcta, alumno_respuesta):
    """"""
    P0_0 = (sympy.sympify(alumno_respuesta[0]), sympy.sympify(alumno_respuesta[1]), sympy.sympify(alumno_respuesta[2]))
    v1_direccion = (sympy.sympify(alumno_respuesta[3]), sympy.sympify(alumno_respuesta[4]), sympy.sympify(alumno_respuesta[5]))
    P0_1 = (sympy.sympify(alumno_respuesta[6]), sympy.sympify(alumno_respuesta[7]), sympy.sympify(alumno_respuesta[8]))
    v2_direccion = (sympy.sympify(alumno_respuesta[9]), sympy.sympify(alumno_respuesta[10]), sympy.sympify(alumno_respuesta[11]))
    respuestas = (P0_0, v1_direccion, P0_1, v2_direccion)

    calificacion = 0
    len_resp_correcta = len(resp_correcta)
    for (resp_correcta, resp) in zip(resp_correcta, respuestas):
        result = 0
        for i in [0,1,2]:
            result = result + (resp_correcta[i] - resp[i])**2
        if result.is_zero:
            calificacion = calificacion + 1

    return sympy.Rational(calificacion, len_resp_correcta)

def check_plano_tangente(plano, alumno_respuesta):
    """"""
    # Variables
    x, y, z = sympy.symbols('x y z')

    alumno_x = sympy.sympify(alumno_respuesta[0])
    alumno_y = sympy.sympify(alumno_respuesta[1])
    alumno_z = sympy.sympify(alumno_respuesta[2])
    alumno_c = sympy.sympify(alumno_respuesta[3])

    grad_plano = sympy.derive_by_array(plano, (x, y, z))
    const = plano.subs([(x, 0), (y, 0), (z, 0)])

    respuestas = (alumno_x, alumno_y, alumno_z, alumno_c)
    respuestas_val = (grad_plano[0], grad_plano[1], grad_plano[2], const)

    contador = 0
    for (e1, e2) in zip(respuestas_val, respuestas):
        if e1 - e2 == 0:
            contador = contador + 1

    return sympy.Rational(contador, len(respuestas_val))

def check_familia_ortogonales(resp_correcta, alumno_respuesta):
    """"""
    if resp_correcta == alumno_respuesta:
        return 1
    else:
        return 0


respuesta_correcta_check = {
    "inversa_matriz": check_inversa_matriz,
    "determinate": check_det_matriz,
    "superficies_regladas": check_superficies_regladas,
    "plano_tangente": check_plano_tangente,
    "familia_ortogonales": check_familia_ortogonales,
}
