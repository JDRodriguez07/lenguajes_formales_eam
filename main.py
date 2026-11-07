"""Lee un archivo y recorre sus tokens mediante el Parser."""

import sys

from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.parser import Parser
from tuquiquilulu.tokens import ErrorLexico


def main():
    # Recibir el nombre del programa y la ruta del archivo.
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.txt")
        return 1

    ruta = sys.argv[1]

    try:
        # Leer el archivo y cerrarlo al salir del bloque.
        with open(ruta, encoding="utf-8") as archivo:
            texto = archivo.read()

        # El lexer transforma los caracteres en objetos Token.
        tokens = tokenizar(texto)

        # El parser guarda los tokens y comienza en la posición cero.
        parser = Parser(tokens)

        # Mostrar cada token y avanzar hasta llegar a EOF.
        while parser.actual().tipo != "EOF":
            print(parser.actual())
            parser.avanzar()

        # EOF también debe aparecer en la salida.
        print(parser.actual())

    except ErrorLexico as error:
        print(error)
        print(
            f"linea = {error.linea}, "
            f"columna = {error.columna}"
        )
        return 1

    except UnicodeDecodeError:
        print(
            "No se pudo leer el archivo: "
            "guárdalo con codificación UTF-8."
        )
        return 1

    except OSError as error:
        print(
            f"No se pudo abrir o leer el archivo "
            f"'{ruta}': {error}"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())