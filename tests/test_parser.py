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

    print("\n" + "=" * 60)
    print("PARSER · Consultar el token actual no avanza")

    entrada = "puntos = 10"

    print("\nEntrada:")
    print(entrada)

    parser = Parser(tokenizar(entrada))

    # Consultamos dos veces sin llamar a avanzar().
    primera_consulta = parser.actual()
    segunda_consulta = parser.actual()

    esperado = [
        Token("IDENTIFICADOR", "puntos", 1, 1),
        Token("IDENTIFICADOR", "puntos", 1, 1),
        0,
    ]

    resultado = [
        primera_consulta,
        segunda_consulta,
        parser.posicion,
    ]

    print("\nSalida esperada:")
    print("Primera consulta:", esperado[0])
    print("Segunda consulta:", esperado[1])
    print("Posición final:", esperado[2])

    print("\nSalida real:")
    print("Primera consulta:", resultado[0])
    print("Segunda consulta:", resultado[1])
    print("Posición final:", resultado[2])

    coincide = resultado == esperado

    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")

    if not coincide:
        raise SystemExit(1)