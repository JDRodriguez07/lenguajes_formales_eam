"""Pruebas de ejecución de programas completos de Tuquiquilulu."""

from contextlib import redirect_stdout
from io import StringIO

from lexer import tokenizar
from parser import Parser
from interprete import Interprete
from tokens import ErrorSemantico


# Cada caso contiene:
# nombre, programa, salida esperada y error esperado.
# El error esperado es (mensaje, línea, columna), o None.
CASOS = [
    (
        "Declaración, asignación y salida",
        "PILLE puntos COMO ENTERO = 5 LISTO\n"
        "puntos = puntos + 2 LISTO\n"
        "QUIUBO(puntos) LISTO",
        "7\n",
        None,
    ),
    (
        "Decimal inicializado con entero",
        "PILLE nota COMO DECIMAL = 7 LISTO\n"
        "QUIUBO(nota / 2) LISTO",
        "3.5\n",
        None,
    ),
    (
        "Texto y booleanos",
        'PILLE mensaje COMO TEXTO = "Hola" LISTO\n'
        'QUIUBO(mensaje + " bro") LISTO\n'
        "QUIUBO(SISAS) LISTO\n"
        "QUIUBO(PAILA) LISTO",
        "Hola bro\nSISAS\nNONAS\n",
        None,
    ),
    (
        "Inicialización posterior",
        "PILLE puntos COMO ENTERO LISTO\n"
        "puntos = 10 LISTO\n"
        "QUIUBO(puntos) LISTO",
        "10\n",
        None,
    ),
    (
        "Variable no declarada",
        "QUIUBO(edad) LISTO",
        "",
        ("la variable 'edad' no ha sido declarada", 1, 8),
    ),
    (
        "Asignación a una variable no declarada",
        "edad = 5 LISTO",
        "",
        ("la variable 'edad' no ha sido declarada", 1, 1),
    ),
    (
        "Declaración duplicada",
        "PILLE x COMO ENTERO = 1 LISTO\n"
        "PILLE x COMO ENTERO = 2 LISTO",
        "",
        ("la variable 'x' ya fue declarada en la línea 1", 2, 7),
    ),
    (
        "Tipo incompatible al declarar",
        'PILLE n COMO ENTERO = "hola" LISTO',
        "",
        (
            "no se puede guardar ese valor en la variable "
            "'n' de tipo ENTERO",
            1,
            7,
        ),
    ),
    (
        "Tipo incompatible al asignar",
        "PILLE n COMO ENTERO = 1 LISTO\n"
        'n = "hola" LISTO',
        "",
        (
            "no se puede guardar ese valor en la variable "
            "'n' de tipo ENTERO",
            2,
            1,
        ),
    ),
    (
        "Un booleano no es un ENTERO",
        "PILLE n COMO ENTERO = SISAS LISTO",
        "",
        (
            "no se puede guardar ese valor en la variable "
            "'n' de tipo ENTERO",
            1,
            7,
        ),
    ),
    (
        "Lectura antes de inicializar",
        "PILLE x COMO ENTERO LISTO\n"
        "QUIUBO(x) LISTO",
        "",
        ("la variable 'x' no tiene un valor asignado", 2, 8),
    ),
    (
        "División por cero durante la ejecución",
        "PILLE d COMO ENTERO = 10 / 0 LISTO",
        "",
        ("división por cero", 1, 26),
    ),
    (
        "Conserva lo impreso antes del error y se detiene",
        "QUIUBO(5) LISTO\n"
        "QUIUBO(edad) LISTO\n"
        "QUIUBO(99) LISTO",
        "5\n",
        ("la variable 'edad' no ha sido declarada", 2, 8),
    ),
    (
        "Ejemplo de la entrega del 20",
        "PILLE precio COMO ENTERO = 12000 LISTO\n"
        "PILLE cantidad COMO ENTERO = 3 LISTO\n"
        "PILLE total COMO ENTERO = precio * cantidad LISTO\n"
        "QUIUBO(total) LISTO\n"
        "PILLE promedio COMO DECIMAL = total / 4.0 LISTO\n"
        "QUIUBO(promedio) LISTO\n"
        'PILLE mensaje COMO TEXTO = "Fin del calculo" LISTO\n'
        "QUIUBO(mensaje) LISTO",
        "36000\n9000.0\nFin del calculo\n",
        None,
    ),
]


def main():
    correctas = 0

    for nombre, entrada, salida_esperada, error_esperado in CASOS:
        programa = Parser(tokenizar(entrada)).programa()
        interprete = Interprete()

        captura = StringIO()
        error_real = None

        # Capturamos únicamente lo que imprime el programa.
        with redirect_stdout(captura):
            try:
                interprete.ejecutar_programa(programa)

            except ErrorSemantico as error:
                error_real = (
                    error.mensaje,
                    error.linea,
                    error.columna,
                )

        salida_real = captura.getvalue()

        coincide = (
            salida_real == salida_esperada
            and error_real == error_esperado
        )

        print("\n" + "=" * 60)
        print("EJECUCIÓN ·", nombre)

        print("\nEntrada:")
        print(entrada)

        print("\nSalida esperada:")
        print(repr(salida_esperada))
        print("Error esperado:", error_esperado)

        print("\nSalida real:")
        print(repr(salida_real))
        print("Error real:", error_real)

        print("\n¿Coinciden?:", "SÍ" if coincide else "NO")

        if coincide:
            correctas += 1

    total = len(CASOS)
    print(f"\nResultado: {correctas}/{total} pruebas correctas.")

    return 0 if correctas == total else 1


if __name__ == "__main__":
    raise SystemExit(main())