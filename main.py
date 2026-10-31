"""Lee un archivo de código y muestra sus tokens."""

import sys

from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.tokens import ErrorLexico


def main():
    # Debemos recibir el nombre del programa y una ruta.
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.txt")
        return 1

    ruta = sys.argv[1]

    try:
        # Leer el archivo como texto y cerrarlo al salir del bloque.
        with open(ruta, encoding="utf-8") as archivo:
            texto = archivo.read()

        # Obtener todos los tokens antes de imprimir la tabla.
        tokens = tokenizar(texto)

    except ErrorLexico as error:
        print(error)
        return 1

    except UnicodeDecodeError:
        print("No se pudo leer el archivo: guárdalo con codificación UTF-8.")
        return 1

    except OSError as error:
        print(f"No se pudo abrir o leer el archivo '{ruta}': {error}")
        return 1

    # Elegir un ancho suficiente para cada columna.
    ancho_linea = max(len("LINEA"), max(len(str(t.linea)) for t in tokens))
    ancho_columna = max(len("COL"), max(len(str(t.columna)) for t in tokens))
    ancho_tipo = max(len("TIPO"), max(len(t.tipo) for t in tokens))

    print(
        f"{'LINEA':<{ancho_linea}}  "
        f"{'COL':<{ancho_columna}}  "
        f"{'TIPO':<{ancho_tipo}}  "
        "TEXTO"
    )

    for token in tokens:
        print(
            f"{token.linea:<{ancho_linea}}  "
            f"{token.columna:<{ancho_columna}}  "
            f"{token.tipo:<{ancho_tipo}}  "
            f"{token.texto}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())