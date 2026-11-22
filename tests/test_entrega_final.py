"""Pruebas conjuntas de los requisitos de la entrega final."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.parser import Parser
from tuquiquilulu.interprete import Interprete
from tuquiquilulu.tokens import ErrorDeLenguaje


# Cada caso contiene:
# nombre, programa, respuestas a LEA, salida esperada, error esperado.
CASOS = [
    (
        "Variable local y global con el mismo nombre",
        "PILLE x COMO ENTERO = 10 LISTO\n"
        "PILAS (SISAS) DE UNA {\n"
        "PILLE x COMO ENTERO = 99 LISTO\n"
        "QUIUBO(x) LISTO\n"
        "} LISTO\n"
        "QUIUBO(x) LISTO",
        [],
        "99\n10\n",
        None,
    ),
    (
        "Asignación desde dos bloques interiores",
        "PILLE x COMO ENTERO = 1 LISTO\n"
        "PILAS (SISAS) DE UNA {\n"
        "PILAS (SISAS) DE UNA {\n"
        "x = x + 5 LISTO\n"
        "} LISTO\n"
        "} LISTO\n"
        "QUIUBO(x) LISTO",
        [],
        "6\n",
        None,
    ),
    (
        "Una variable local no existe afuera",
        "PILAS (SISAS) DE UNA {\n"
        "PILLE x COMO ENTERO = 5 LISTO\n"
        "} LISTO\n"
        "QUIUBO(x) LISTO",
        [],
        "",
        ("la variable 'x' no ha sido declarada", 4, 8),
    ),
    (
        "Cada vuelta tiene sus propias variables",
        "PILLE n COMO ENTERO = 1 LISTO\n"
        "MIENTRAS (n <= 2) DE UNA {\n"
        "PILLE temporal COMO ENTERO = n * 10 LISTO\n"
        "QUIUBO(temporal) LISTO\n"
        "n = n + 1 LISTO\n"
        "} LISTO",
        [],
        "10\n20\n",
        None,
    ),
    (
        "Precedencia lógica y paréntesis",
        "QUIUBO(SISAS O DE PRONTO NONAS Y ADEMÁS NONAS) LISTO\n"
        "QUIUBO((SISAS O DE PRONTO NONAS) Y ADEMÁS NONAS) LISTO\n"
        "QUIUBO(NADA DE 2 > 3) LISTO",
        [],
        "SISAS\nNONAS\nSISAS\n",
        None,
    ),
    (
        "Cortocircuito evita evaluar la división por cero",
        "QUIUBO(NONAS Y ADEMÁS (5 / 0 > 1)) LISTO\n"
        "QUIUBO(SISAS O DE PRONTO (5 / 0 > 1)) LISTO",
        [],
        "NONAS\nSISAS\n",
        None,
    ),
    (
        "Negativos y división hacia cero",
        "QUIUBO(-(2 + 3)) LISTO\n"
        "QUIUBO(8 - -2) LISTO\n"
        "QUIUBO(-7 / 2) LISTO",
        [],
        "-5\n10\n-3\n",
        None,
    ),
    (
        "Booleano calculado y alternativa",
        "PILLE listo COMO BOOLEANO = 2 > 3 LISTO\n"
        "PILAS (listo) DE UNA {\n"
        'QUIUBO("si") LISTO\n'
        "} O SI NO {\n"
        'QUIUBO("no") LISTO\n'
        "} LISTO",
        [],
        "no\n",
        None,
    ),
    (
        "Lectura de los cuatro tipos",
        "PILLE nombre COMO TEXTO LISTO\n"
        "PILLE edad COMO ENTERO LISTO\n"
        "PILLE nota COMO DECIMAL LISTO\n"
        "PILLE activo COMO BOOLEANO LISTO\n"
        "LEA(nombre) LISTO\n"
        "LEA(edad) LISTO\n"
        "LEA(nota) LISTO\n"
        "LEA(activo) LISTO\n"
        "QUIUBO(nombre) LISTO\n"
        "QUIUBO(edad + 1) LISTO\n"
        "QUIUBO(nota / 2) LISTO\n"
        "QUIUBO(activo) LISTO",
        ["Juan", "20", "7", "PAILA"],
        "Juan\n21\n3.5\nNONAS\n",
        None,
    ),
    (
        "Lectura inválida de un entero",
        "PILLE edad COMO ENTERO LISTO\n"
        "LEA(edad) LISTO",
        ["hola"],
        "",
        (
            "entrada inválida para 'edad': "
            "se esperaba un valor de tipo ENTERO",
            2,
            5,
        ),
    ),
    (
        "Lectura inválida de un booleano",
        "PILLE activo COMO BOOLEANO LISTO\n"
        "LEA(activo) LISTO",
        ["quizas"],
        "",
        (
            "entrada inválida para 'activo': "
            "se esperaba un valor de tipo BOOLEANO",
            2,
            5,
        ),
    ),
    (
        "Lectura sin datos disponibles",
        "PILLE edad COMO ENTERO LISTO\n"
        "LEA(edad) LISTO",
        [],
        "",
        ("no se recibió una entrada para 'edad'", 2, 5),
    ),
]


def ejecutar_caso(entrada, respuestas):
    """Ejecuta un programa con respuestas de teclado preparadas."""
    captura = StringIO()
    error_real = None
    pendientes = iter(respuestas)
    consumidas = []

    def leer_simulado(mensaje=""):
        try:
            respuesta = next(pendientes)
        except StopIteration:
            raise EOFError from None

        consumidas.append(respuesta)
        return respuesta

    with redirect_stdout(captura):
        with patch("builtins.input", side_effect=leer_simulado):
            try:
                programa = Parser(tokenizar(entrada)).programa()
                Interprete().ejecutar_programa(programa)

            except ErrorDeLenguaje as error:
                error_real = (
                    error.mensaje,
                    error.linea,
                    error.columna,
                )

    return captura.getvalue(), error_real, consumidas


def main():
    casos = list(CASOS)

    # También verificamos los archivos obligatorios de la entrega.
    raiz = Path(__file__).resolve().parents[1]

    ejemplos = [
        ("Tabla del 3", "tabla_del_3.txt", "3\n6\n9\n12\n15\n"),
        ("Factorial de 5", "factorial_de_5.txt", "120\n"),
        ("Promedio", "promedio_notas.txt", "4.0\naprueba\n"),
    ]

    for nombre, archivo, esperado in ejemplos:
        entrada = (raiz / "examples" / archivo).read_text(
            encoding="utf-8"
        )
        casos.append((nombre, entrada, [], esperado, None))

    correctas = 0

    for nombre, entrada, respuestas, esperado, error_esperado in casos:
        real, error_real, consumidas = ejecutar_caso(
            entrada,
            respuestas,
        )

        coincide = (
            real == esperado
            and error_real == error_esperado
            and consumidas == respuestas
        )

        print("\n" + "=" * 60)
        print("ENTREGA FINAL ·", nombre)

        print("\nEntrada:")
        print(entrada)
        print("Respuestas de teclado:", respuestas)

        print("\nSalida esperada:")
        print(repr(esperado))
        print("Error esperado:", error_esperado)

        print("\nSalida real:")
        print(repr(real))
        print("Error real:", error_real)
        print("Respuestas consumidas:", consumidas)

        print("\n¿Coinciden?:", "SÍ" if coincide else "NO")

        if coincide:
            correctas += 1

    total = len(casos)
    print(f"\nResultado: {correctas}/{total} pruebas correctas.")

    return 0 if correctas == total else 1


if __name__ == "__main__":
    raise SystemExit(main())