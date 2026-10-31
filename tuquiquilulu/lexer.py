"""Reconocimiento de tokens de Tuquiquilulu."""

from .tokens import Token, ErrorLexico


# Conjuntos: permiten comprobar si una palabra pertenece a una categoría.
TIPOS = {"ENTERO", "DECIMAL", "TEXTO", "BOOLEANO"}

RESERVADAS = {
    # Palabras de Tuquiquilulu.
    "PILLE", "COMO", "PILAS",

    # Palabras de control solicitadas en la guía.
    "if", "else", "while",
}

BOOLEANOS = {
    # Valores de Tuquiquilulu.
    "SISAS", "NONAS", "MELO", "PAILA",
    # Valores solicitados en la guía.
    "true", "false",
}

INICIO_COMENTARIO = "OJO:"

INICIO_COMENTARIO_BLOQUE = "/*"

FIN_COMENTARIO_BLOQUE = "*/"

# Operadores de un carácter.
OPERADORES = {"+", "-", "*", "<", ">"}

# Operadores de dos caracteres.
OPERADORES_DOBLES = {"==", "!=", "<=", ">="}

# Delimitadores y signos de puntuación de la tarea 8.
SIMBOLOS = {"(", ")", "{", "}", ",", ".", ";"}

def tokenizar(texto):
    """Devuelve objetos Token o lanza ErrorLexico ante el primer error léxico.
    """
    tokens = []
    i = 0
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        # 1. Ignorar espacios y tabulaciones.
        if c in " \t":
            i += 1
            columna += 1

        # 2. Avanzar de línea y reiniciar la columna.
        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        # 3. Ignorar el comentario, dejando el salto para el caso anterior.
        # Reconocer e ignorar comentarios de bloque.
        elif texto.startswith(INICIO_COMENTARIO_BLOQUE, i):
            linea_inicio = linea
            columna_inicio = columna

            # Consumir los dos caracteres de apertura: /*
            i += 2
            columna += 2

            # Recorrer el contenido hasta encontrar el cierre.
            while (
                i < len(texto)
                and not texto.startswith(FIN_COMENTARIO_BLOQUE, i)
            ):
                if texto[i] == "\n":
                    i += 1
                    linea += 1
                    columna = 1
                else:
                    i += 1
                    columna += 1

            # Si llegamos al final, faltó cerrar el comentario.
            if i >= len(texto):
                raise ErrorLexico(
                    "comentario de bloque sin cerrar",
                    linea_inicio,
                    columna_inicio,
                )

            # Consumir los dos caracteres de cierre: */
            i += 2
            columna += 2

        elif texto.startswith(INICIO_COMENTARIO, i):
            while i < len(texto) and texto[i] != "\n":
                i += 1
                columna += 1

        # 4. Leer un número entero o decimal.
        elif c.isdigit():
            inicio = i
            linea_inicio = linea
            columna_inicio = columna

            while i < len(texto) and texto[i].isdigit():
                i += 1
                columna += 1

            if i < len(texto) and texto[i] == ".":
                # Reportar el punto problemático, no el inicio del número.
                # Ejemplo: 25..55 falla en la columna 3.
                if i + 1 >= len(texto) or not texto[i + 1].isdigit():
                    raise ErrorLexico(
                        "decimal mal formado",
                        linea,
                        columna,
                    )

                i += 1
                columna += 1

                while i < len(texto) and texto[i].isdigit():
                    i += 1
                    columna += 1

                # Un segundo punto tampoco pertenece a un decimal válido.
                if i < len(texto) and texto[i] == ".":
                    raise ErrorLexico(
                        "decimal mal formado",
                        linea,
                        columna,
                    )

            tokens.append(Token("NUMERO", texto[inicio:i], linea_inicio, columna_inicio))

        # 5. Leer texto entre comillas dobles, en una sola línea.
        # Esta versión no implementa secuencias de escape.
        elif c == '"':
            inicio = i
            linea_inicio = linea
            columna_inicio = columna
            i += 1
            columna += 1

            while i < len(texto) and texto[i] != '"' and texto[i] != "\n":
                i += 1
                columna += 1

            if i >= len(texto) or texto[i] == "\n":
                raise ErrorLexico(
                    "cadena de texto sin cerrar",
                    linea_inicio,
                    columna_inicio,
                )

            i += 1
            columna += 1
            tokens.append(Token("TEXTO", texto[inicio:i], linea_inicio, columna_inicio))

        # 6. Leer la palabra completa antes de clasificarla.
        elif c.isalpha():
            inicio = i
            columna_inicio = columna

            while (i < len(texto) and (texto[i].isalnum() or texto[i] == "_")):
                i += 1
                columna += 1

            palabra = texto[inicio:i]

            if palabra in TIPOS:
                tipo = "TIPO"

            elif palabra in BOOLEANOS:
                tipo = "BOOLEANO"

            elif palabra in RESERVADAS:
                tipo = "RESERVADA"

            elif palabra == "LISTO":
                tipo = "FIN_INSTRUCCION"

            else:
                tipo = "IDENTIFICADOR"

            tokens.append(Token(tipo, palabra, linea, columna_inicio))

        # 7. Reconocer operadores de dos caracteres.
        elif texto[i:i + 2] in OPERADORES_DOBLES:
            operador = texto[i:i + 2]

            tokens.append(Token("OPERADOR", operador, linea, columna))

            i += 2
            columna += 2

        # 8. Reconocer la asignación.
        elif c == "=":
            tokens.append(Token("ASIGNACION", c, linea, columna))
            i += 1
            columna += 1

        # 9. Reconocer operadores de un carácter.
        elif c in OPERADORES:
            tokens.append(Token("OPERADOR", c, linea, columna))
            i += 1
            columna += 1

        # 10. Reconocer delimitadores
        elif c in SIMBOLOS:
            tokens.append(Token("SIMBOLO", c, linea, columna))
            i += 1
            columna += 1

        # 11. Detenerse ante un carácter no reconocido.
        else:
            raise ErrorLexico(
                f"carácter '{c}' no reconocido",
                linea,
                columna,
            )

    # El recorrido terminó: señalar el final de la entrada.
    tokens.append(Token("EOF", "", linea, columna))

    return tokens
