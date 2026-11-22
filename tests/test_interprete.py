"""Primeras pruebas del intérprete: evaluación de literales."""

from lexer import tokenizar
from parser import Parser
from interprete import Interprete
from tokens import ErrorSemantico


CASOS = [
    ("Número entero", "5", 5, int),
    ("Número decimal", "3.5", 3.5, float),
    ("Texto", '"Ana"', "Ana", str),
    ("Texto vacío", '""', "", str),
    ("Booleano SISAS", "SISAS", True, bool),
    ("Booleano NONAS", "NONAS", False, bool),
    ("Booleano MELO", "MELO", True, bool),
    ("Booleano PAILA", "PAILA", False, bool),
    ("Booleano true", "true", True, bool),
    ("Booleano false", "false", False, bool),
    ("Suma", "5 + 2", 7, int),
    ("Prioridad de multiplicación", "5 + 2 * 3", 11, int),
    ("Paréntesis", "(5 + 2) * 3", 21, int),
    ("Resta a la izquierda", "10 - 3 - 2", 5, int),
    ("División entera", "7 / 2", 3, int),
    ("División decimal", "7 / 2.0", 3.5, float),
    ("División a la izquierda", "8 / 4 / 2", 1, int),
    ("Suma con decimal", "2 + 0.5", 2.5, float),
    ("Unión de textos", '"ho" + "la"', "hola", str),
    ("División negativa hacia cero", "(0 - 7) / 2", -3, int),
]

CASOS_INVALIDOS = [
    (
        "División por cero",
        "5 / 0",
        "división por cero",
        1,
        3,
    ),
    (
        "División por una expresión que da cero",
        "8 / (3 - 3)",
        "división por cero",
        1,
        3,
    ),
    (
        "Texto por número",
        '"hola" * 2',
        "no se puede usar '*' con esos valores de texto",
        1,
        8,
    ),
    (
        "Texto más número",
        '"hola" + 2',
        "no se puede usar '+' con esos valores de texto",
        1,
        8,
    ),
    (
        "Booleano más número",
        "SISAS + 1",
        "el operador '+' requiere números",
        1,
        7,
    ),
]


def main():
    correctas = 0

    for nombre, entrada, esperado, tipo_esperado in CASOS:
        parser = Parser(tokenizar(entrada))

        # En esta prueba aislamos una expresión, no un programa completo.
        nodo = parser.expresion()
        parser.esperar("EOF")

        resultado = Interprete().evaluar(nodo)

        coincide = (
            resultado == esperado
            and type(resultado) is tipo_esperado
        )

        print("\n" + "=" * 60)
        print("INTÉRPRETE ·", nombre)
        print("\nEntrada:")
        print(entrada)

        print("\nSalida esperada:")
        print(f"{esperado!r} ({tipo_esperado.__name__})")

        print("\nSalida real:")
        print(f"{resultado!r} ({type(resultado).__name__})")

        print("\n¿Coinciden?:", "SÍ" if coincide else "NO")

        if coincide:
            correctas += 1

    for nombre, entrada, mensaje, linea, columna in CASOS_INVALIDOS:
        parser = Parser(tokenizar(entrada))
        nodo = parser.expresion()
        parser.esperar("EOF")

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

        print("\n" + "=" * 60)
        print("INTÉRPRETE ·", nombre)
        print("\nEntrada:")
        print(entrada)
        print("\nSalida esperada:")
        print(esperado)
        print("\nSalida real:")
        print(resultado)
        print("\n¿Coinciden?:", "SÍ" if coincide else "NO")

        if coincide:
            correctas += 1

        total = len(CASOS) + len(CASOS_INVALIDOS)
    print(f"\nResultado: {correctas}/{total} pruebas correctas.")

    return 0 if correctas == total else 1


if __name__ == "__main__":
    raise SystemExit(main())