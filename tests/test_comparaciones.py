"""Pruebas de comparaciones y sus errores semánticos."""

from lexer import tokenizar
from parser import Parser
from interprete import Interprete
from tokens import ErrorSemantico


CASOS_VALIDOS = [
    ("Mayor que", "5 > 2", True),
    ("Menor que", "5 < 2", False),
    ("Mayor o igual", "5 + 2 >= 7", True),
    ("Menor o igual", "3 <= 3", True),
    ("Igualdad numérica", "3 == 3.0", True),
    ("Diferencia numérica", "3 != 3", False),
    ("Igualdad de textos", '"hola" == "hola"', True),
    ("Diferencia de textos", '"hola" != "adios"', True),
    ("Igualdad de booleanos", "SISAS == MELO", True),
    ("Diferencia de booleanos", "SISAS != NONAS", True),
    ("Paréntesis aritméticos", "(2 + 3) * 2 == 10", True),
]

CASOS_INVALIDOS = [
    (
        "Texto comparado con número",
        '"5" == 5',
        "no se pueden comparar valores de tipos incompatibles",
        1,
        5,
    ),
    (
        "Booleano comparado con número",
        "SISAS == 1",
        "no se pueden comparar valores de tipos incompatibles",
        1,
        7,
    ),
    (
        "Orden entre textos",
        '"a" < "b"',
        "el comparador '<' requiere números",
        1,
        5,
    ),
    (
        "Orden entre booleanos",
        "SISAS > NONAS",
        "el comparador '>' requiere números",
        1,
        7,
    ),
]


def construir_condicion(entrada):
    parser = Parser(tokenizar(entrada))
    nodo = parser.condicion()
    parser.esperar("EOF")
    return nodo


def mostrar_resultado(nombre, entrada, esperado, real, coincide):
    print("\n" + "=" * 60)
    print("COMPARACIÓN ·", nombre)
    print("\nEntrada:")
    print(entrada)
    print("\nSalida esperada:")
    print(esperado)
    print("\nSalida real:")
    print(real)
    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")


def main():
    correctas = 0

    for nombre, entrada, esperado in CASOS_VALIDOS:
        nodo = construir_condicion(entrada)
        resultado = Interprete().evaluar(nodo)

        coincide = (
            type(resultado) is bool
            and resultado == esperado
        )

        mostrar_resultado(
            nombre, entrada, esperado, resultado, coincide
        )

        if coincide:
            correctas += 1

    for nombre, entrada, mensaje, linea, columna in CASOS_INVALIDOS:
        nodo = construir_condicion(entrada)
        esperado = (mensaje, linea, columna)

        try:
            valor = Interprete().evaluar(nodo)
            resultado = ("No se produjo el error esperado", valor)
            coincide = False

        except ErrorSemantico as error:
            resultado = (
                error.mensaje,
                error.linea,
                error.columna,
            )
            coincide = resultado == esperado

        mostrar_resultado(
            nombre, entrada, esperado, resultado, coincide
        )

        if coincide:
            correctas += 1

    total = len(CASOS_VALIDOS) + len(CASOS_INVALIDOS)
    print(f"\nResultado: {correctas}/{total} pruebas correctas.")

    return 0 if correctas == total else 1


if __name__ == "__main__":
    raise SystemExit(main())