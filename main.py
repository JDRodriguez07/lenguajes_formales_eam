"""Lee y ejecuta un programa de Tuquiquilulu."""

import sys

from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.parser import Parser
from tuquiquilulu.tokens import ErrorDeLenguaje
from tuquiquilulu.interprete import Interprete


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

        # Texto -> tokens -> árbol -> ejecución.
        programa = Parser(tokenizar(texto)).programa()
        Interprete().ejecutar_programa(programa)

    except ErrorDeLenguaje as error:
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