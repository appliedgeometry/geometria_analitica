import sympy
import ast
from sympy.parsing.latex import parse_latex


def inversa_matriz(pregunta, html=False):
    """"""
    inicio = pregunta.find("$")
    final = pregunta.rfind("$")
    sympy_str = ast.literal_eval(pregunta[inicio+1:final])
    sympy_obj = sympy.Matrix(sympy_str)
    try:
        return sympy_obj.inv() if not html else f"${sympy.latex(sympy_obj.inv())}$"
    except:
        zero = sympy.Matrix([
            [0, 0],
            [0, 0]
        ])
        # TODO "NO EXISTE INVERSA"
        return zero if not html else "Sin inversa"

def determinate(pregunta, html=False):
    """"""
    inicio = pregunta.find("$")
    final = pregunta.rfind("$")
    sympy_str = ast.literal_eval(pregunta[inicio+1:final])
    sympy_obj = sympy.Matrix(sympy_str)
    return sympy_obj.det() if not html else f"${sympy.latex(sympy_obj.det())}$"

def superficies_regladas(pregunta, html=False):
    """"""
    final = pregunta.rfind("$")
    inicio = pregunta[:final].rfind("$")
    eq_symbolic = sympy.sympify(pregunta[inicio+1:final])
    coeff_x = sympy.sqrt(eq_symbolic.coeff('x**2').as_numer_denom()[1])
    coeff_y = sympy.sqrt(eq_symbolic.coeff('y**2').as_numer_denom()[1])

    punto_final = pregunta[:inicio].rfind("$")
    punto_inicio = pregunta[:punto_final].rfind("$")

    # Respuestas
    punto = pregunta[punto_inicio+2:punto_final-1].split(",")
    x0 = sympy.sympify(punto[0])
    y0 = sympy.sympify(punto[1])
    z0 = sympy.sympify(punto[2])
    v1_direccion = (-coeff_x/(coeff_y*x0 - coeff_x*y0), -coeff_y/(coeff_y*x0 - coeff_x*y0), -2/(coeff_x*coeff_y))
    v2_direccion = (-coeff_x/(coeff_y*x0 + coeff_x*y0), coeff_y/(coeff_y*x0 + coeff_x*y0), -2/(coeff_x*coeff_y))
    if html:
        return f'$({x0},{y0},{z0}) + t{v1_direccion}$  y   $({x0},{y0},{z0}) + t{v2_direccion}$'
    else:
        return ((x0, y0, z0), v1_direccion, (x0, y0, z0), v2_direccion)

def plano_tangente(pregunta, html=False):
    """"""
    # Variables
    x, y, z = sympy.symbols('x y z')
    # Punto
    final_punto = pregunta.rfind("$")
    antefinal = pregunta[0:final_punto-1].rfind("$")
    punto = pregunta[antefinal+2:final_punto-1].strip().split(",")
    punto_sym = [sympy.sympify(elemento) for elemento in punto]

    P_min_P0 = tuple([punto_sym[0]-x, punto_sym[1]-y, punto_sym[2]-z])

    # Ecuacion
    inicio = pregunta.find("$")
    final = pregunta.find("$", inicio + 1)
    funcion = sympy.sympify(pregunta[inicio+1:final-2])

    grad_funcion = sympy.derive_by_array(funcion, (x, y, z))
    grad_funcion_subs = (e.subs([(x, punto_sym[0]), (y, punto_sym[1]), (z, punto_sym[2])]) for e in grad_funcion)
    plano = sympy.simplify(sum(map(lambda e1, e2: e1 * e2, P_min_P0, grad_funcion_subs)))
    plano_latex = sympy.latex(plano)
    if html:
        return f'${plano_latex}=0$'
    else:
        return plano

def familia_ortogonales(pregunta, html=False):
    """"""
    return "$\\{$ rectas por el origen $\\}$ y $\\{$ círculos con centro en el origen $\\}$"


respuesta_correcta = {
    "inversa_matriz": inversa_matriz,
    "determinate": determinate,
    "superficies_regladas": superficies_regladas,
    "plano_tangente": plano_tangente,
    "familia_ortogonales": familia_ortogonales,
}
