"""Primeras pruebas del intérprete: evaluación de literales."""

from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.parser import Parser
from tuquiquilulu.interprete import Interprete


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

    total = len(CASOS)
    print(f"\nResultado: {correctas}/{total} pruebas correctas.")

    return 0 if correctas == total else 1


if __name__ == "__main__":
    raise SystemExit(main())