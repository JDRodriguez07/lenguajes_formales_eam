"""Pruebas del prototipo de Parser de Tuquiquilulu."""

from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.parser import Parser
from tuquiquilulu.tokens import Token


if __name__ == "__main__":
    print("=" * 60)
    print("PARSER · Dos objetos con posiciones independientes")

    entrada_uno = "x = 5"
    entrada_dos = "y = 8"

    print("\nEntradas:")
    print("Parser uno:", entrada_uno)
    print("Parser dos:", entrada_dos)

    parser_uno = Parser(tokenizar(entrada_uno))
    parser_dos = Parser(tokenizar(entrada_dos))

    # Avanzamos únicamente el primer objeto.
    parser_uno.avanzar()

    # Esperamos que el primero esté en '=' y el segundo siga en 'y'.
    esperado = [
        (1, Token("ASIGNACION", "=", 1, 3)),
        (0, Token("IDENTIFICADOR", "y", 1, 1)),
    ]

    resultado = [
        (parser_uno.posicion, parser_uno.actual()),
        (parser_dos.posicion, parser_dos.actual()),
    ]

    print("\nSalida esperada:")
    for posicion, token in esperado:
        print(f"posición = {posicion}, token = {token}")

    print("\nSalida real:")
    for posicion, token in resultado:
        print(f"posición = {posicion}, token = {token}")

    coincide = resultado == esperado

    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")

    if not coincide:
        raise SystemExit(1)