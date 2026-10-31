"""Tuquiquilulu: analizador léxico y seis pruebas del parcial.
"""

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

def tokenizar_fin_archivo(texto):
    """Devuelve tokens o lanza SyntaxError ante el primer error léxico.
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
                raise SyntaxError(
                    "Comentario de bloque sin cerrar "
                    f"en línea {linea_inicio}, "
                    f"columna {columna_inicio}"
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
                    raise SyntaxError(
                        f"Decimal mal formado en línea {linea}, columna {columna}"
                    )

                i += 1
                columna += 1

                while i < len(texto) and texto[i].isdigit():
                    i += 1
                    columna += 1

                # Un segundo punto tampoco pertenece a un decimal válido.
                if i < len(texto) and texto[i] == ".":
                    raise SyntaxError(
                        f"Decimal mal formado en línea {linea}, columna {columna}"
                    )

            tokens.append(("NUMERO", texto[inicio:i], linea_inicio, columna_inicio))

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
                raise SyntaxError(
                    "Cadena de texto sin cerrar "
                    f"en línea {linea_inicio}, columna {columna_inicio}"
                )

            i += 1
            columna += 1
            tokens.append(("TEXTO", texto[inicio:i], linea_inicio, columna_inicio))

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

            tokens.append((tipo, palabra, linea, columna_inicio))

        # 7. Reconocer operadores de dos caracteres.
        elif texto[i:i + 2] in OPERADORES_DOBLES:
            operador = texto[i:i + 2]

            tokens.append(("OPERADOR", operador, linea, columna))

            i += 2
            columna += 2

        # 8. Reconocer la asignación.
        elif c == "=":
            tokens.append(("ASIGNACION", c, linea, columna))
            i += 1
            columna += 1

        # 9. Reconocer operadores de un carácter.
        elif c in OPERADORES:
            tokens.append(("OPERADOR", c, linea, columna))
            i += 1
            columna += 1

        # 10. Reconocer delimitadores
        elif c in SIMBOLOS:
            tokens.append(("SIMBOLO", c, linea, columna))
            i += 1
            columna += 1

        # 11. Detenerse ante un carácter no reconocido.
        else:
            raise SyntaxError(
                f"Error léxico: carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    # El recorrido terminó: señalar el final de la entrada.
    tokens.append(("EOF", "", linea, columna))

    return tokens


# Las funciones siguientes solo muestran y comparan las pruebas.
# Las salidas esperadas se escriben manualmente, antes de ejecutar el lexer.
def probar_caso(nombre, codigo, esperado):
    print("\n" + "=" * 60)
    print(nombre)
    print("\nEntrada:")
    print(codigo)
    print("\nSalida esperada:")
    if isinstance(esperado, list):
        for token in esperado:
            print(token)
    else:
        print(esperado)

    print("\nSalida real:")
    try:
        resultado = tokenizar_fin_archivo(codigo)
        for token in resultado:
            print(token)
    except SyntaxError as error:
        resultado = str(error)
        print(resultado)

    coincide = resultado == esperado
    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")
    if not coincide:
        print("Revisar el cálculo manual y el lexer; anotar la causa y corrección.")
    return coincide


if __name__ == "__main__":
    resultados = []

    # Válido 1: también se usa para el recorrido manual del video.
    resultados.append(probar_caso(
        "CASO VÁLIDO 1 · Declaración sencilla",
        "PILLE x COMO ENTERO = 5 LISTO",
        [
            ("RESERVADA", "PILLE", 1, 1),
            ("IDENTIFICADOR", "x", 1, 7),
            ("RESERVADA", "COMO", 1, 9),
            ("TIPO", "ENTERO", 1, 14),
            ("ASIGNACION", "=", 1, 21),
            ("NUMERO", "5", 1, 23),
            ("FIN_INSTRUCCION", "LISTO", 1, 25),
            ("EOF", "", 1, 30),
        ],
    ))

    # Válido 2: los operadores no necesitan espacios a sus lados.
    resultados.append(probar_caso(
        "CASO VÁLIDO 2 · Operadores sin espacios",
        "PILLE total COMO ENTERO = puntos+5*2 LISTO",
        [
            ("RESERVADA", "PILLE", 1, 1),
            ("IDENTIFICADOR", "total", 1, 7),
            ("RESERVADA", "COMO", 1, 13),
            ("TIPO", "ENTERO", 1, 18),
            ("ASIGNACION", "=", 1, 25),
            ("IDENTIFICADOR", "puntos", 1, 27),
            ("OPERADOR", "+", 1, 33),
            ("NUMERO", "5", 1, 34),
            ("OPERADOR", "*", 1, 35),
            ("NUMERO", "2", 1, 36),
            ("FIN_INSTRUCCION", "LISTO", 1, 38),
            ("EOF", "", 1, 43),
        ],
    ))

    # Válido 3: cadena cerrada, comentario, salto de línea y decimal.
    resultados.append(probar_caso(
        "CASO VÁLIDO 3 · Texto, comentario y decimal en dos líneas",
        'PILLE nombre COMO TEXTO = "Ana" LISTO OJO: comentario\n'
        "PILLE tiempo COMO DECIMAL = 3.5 LISTO",
        [
            ("RESERVADA", "PILLE", 1, 1),
            ("IDENTIFICADOR", "nombre", 1, 7),
            ("RESERVADA", "COMO", 1, 14),
            ("TIPO", "TEXTO", 1, 19),
            ("ASIGNACION", "=", 1, 25),
            ("TEXTO", '"Ana"', 1, 27),
            ("FIN_INSTRUCCION", "LISTO", 1, 33),
            ("RESERVADA", "PILLE", 2, 1),
            ("IDENTIFICADOR", "tiempo", 2, 7),
            ("RESERVADA", "COMO", 2, 14),
            ("TIPO", "DECIMAL", 2, 19),
            ("ASIGNACION", "=", 2, 27),
            ("NUMERO", "3.5", 2, 29),
            ("FIN_INSTRUCCION", "LISTO", 2, 33),
            ("EOF", "", 2, 38),
        ],
    ))

    resultados.append(probar_caso(
        "CASO INVÁLIDO 1 · Carácter desconocido",
        "PILLE puntos COMO ENTERO = 100 @ LISTO",
        "Error léxico: carácter inesperado '@' en línea 1, columna 32",
    ))

    # Usamos un decimal mal formado: '=' sí es válido en nuestro lenguaje.
    # En 3.4.5, el segundo punto está en la columna 32 de esta instrucción.
    resultados.append(probar_caso(
        "CASO INVÁLIDO 2 · Decimal mal formado",
        "PILLE tiempo COMO DECIMAL = 3.4.5 LISTO",
        "Decimal mal formado en línea 1, columna 32",
    ))

    # Aquí la posición señala la comilla de apertura del texto sin cerrar.
    resultados.append(probar_caso(
        "CASO INVÁLIDO 3 · Texto sin cerrar en la segunda línea",
        'PILLE puntos COMO ENTERO = 0 LISTO\n'
        'PILLE categoria COMO TEXTO = "Historia LISTO',
        "Cadena de texto sin cerrar en línea 2, columna 30",
    ))

    # Tarea 8: paréntesis, operadores y punto y coma.
    resultados.append(probar_caso(
        "TAREA 8 · Expresión con delimitadores",
        "(a+b)*2;",
        [
            ("SIMBOLO", "(", 1, 1),
            ("IDENTIFICADOR", "a", 1, 2),
            ("OPERADOR", "+", 1, 3),
            ("IDENTIFICADOR", "b", 1, 4),
            ("SIMBOLO", ")", 1, 5),
            ("OPERADOR", "*", 1, 6),
            ("NUMERO", "2", 1, 7),
            ("SIMBOLO", ";", 1, 8),
            ("EOF", "", 1, 9),
        ],
    ))

    # El punto separado es símbolo; dentro de 3.14 es parte del número.
    resultados.append(probar_caso(
        "TAREA 8 · Punto y decimal",
        "System.out 3.14",
        [
            ("IDENTIFICADOR", "System", 1, 1),
            ("SIMBOLO", ".", 1, 7),
            ("IDENTIFICADOR", "out", 1, 8),
            ("NUMERO", "3.14", 1, 12),
            ("EOF", "", 1, 16),
        ],
    ))

    # Tarea 8: llaves y coma.
    resultados.append(probar_caso(
        "TAREA 8 · Llaves y coma",
        "{a,b}",
        [
            ("SIMBOLO", "{", 1, 1),
            ("IDENTIFICADOR", "a", 1, 2),
            ("SIMBOLO", ",", 1, 3),
            ("IDENTIFICADOR", "b", 1, 4),
            ("SIMBOLO", "}", 1, 5),
            ("EOF", "", 1, 6),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Operadores dobles",
        "a==b a!=b a<=b a>=b",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "==", 1, 2),
            ("IDENTIFICADOR", "b", 1, 4),

            ("IDENTIFICADOR", "a", 1, 6),
            ("OPERADOR", "!=", 1, 7),
            ("IDENTIFICADOR", "b", 1, 9),

            ("IDENTIFICADOR", "a", 1, 11),
            ("OPERADOR", "<=", 1, 12),
            ("IDENTIFICADOR", "b", 1, 14),

            ("IDENTIFICADOR", "a", 1, 16),
            ("OPERADOR", ">=", 1, 17),
            ("IDENTIFICADOR", "b", 1, 19),

            ("EOF", "", 1, 20),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Operadores relacionales simples",
        "a<b a>b",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "<", 1, 2),
            ("IDENTIFICADOR", "b", 1, 3),
            ("IDENTIFICADOR", "a", 1, 5),
            ("OPERADOR", ">", 1, 6),
            ("IDENTIFICADOR", "b", 1, 7),
            ("EOF", "", 1, 8),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Comparación de igualdad",
        "x == 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("OPERADOR", "==", 1, 3),
            ("NUMERO", "5", 1, 6),
            ("EOF", "", 1, 7),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Asignaciones separadas por un espacio",
        "x = = 5",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("ASIGNACION", "=", 1, 3),
            ("ASIGNACION", "=", 1, 5),
            ("NUMERO", "5", 1, 7),
            ("EOF", "", 1, 8),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Exclamación sin igual",
        "x ! 5",
        "Error léxico: carácter inesperado '!' en línea 1, columna 3",
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Reservadas de control",
        "if else while",
        [
            ("RESERVADA", "if", 1, 1),
            ("RESERVADA", "else", 1, 4),
            ("RESERVADA", "while", 1, 9),
            ("EOF", "", 1, 14),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Palabras completas",
        "if iffy while_x PILAS PILAS_extra",
        [
            ("RESERVADA", "if", 1, 1),
            ("IDENTIFICADOR", "iffy", 1, 4),
            ("IDENTIFICADOR", "while_x", 1, 9),
            ("RESERVADA", "PILAS", 1, 17),
            ("IDENTIFICADOR", "PILAS_extra", 1, 23),
            ("EOF", "", 1, 34),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Valores booleanos",
        "SISAS NONAS MELO PAILA true false",
        [
            ("BOOLEANO", "SISAS", 1, 1),
            ("BOOLEANO", "NONAS", 1, 7),
            ("BOOLEANO", "MELO", 1, 13),
            ("BOOLEANO", "PAILA", 1, 18),
            ("BOOLEANO", "true", 1, 24),
            ("BOOLEANO", "false", 1, 29),
            ("EOF", "", 1, 34),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Tipo, valor e identificadores",
        "BOOLEANO SISAS SISAS_extra true_x",
        [
            ("TIPO", "BOOLEANO", 1, 1),
            ("BOOLEANO", "SISAS", 1, 10),
            ("IDENTIFICADOR", "SISAS_extra", 1, 16),
            ("IDENTIFICADOR", "true_x", 1, 28),
            ("EOF", "", 1, 34),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Comentario en una línea",
        "a/* hola */+b",
        [
            ("IDENTIFICADOR", "a", 1, 1),
            ("OPERADOR", "+", 1, 12),
            ("IDENTIFICADOR", "b", 1, 13),
            ("EOF", "", 1, 14),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Comentario de varias líneas",
        "PILLE a COMO ENTERO = 1 LISTO /* uno\n"
        "dos\n"
        "tres */\n"
        "PILLE b COMO ENTERO = 2 LISTO",
        [
            ("RESERVADA", "PILLE", 1, 1),
            ("IDENTIFICADOR", "a", 1, 7),
            ("RESERVADA", "COMO", 1, 9),
            ("TIPO", "ENTERO", 1, 14),
            ("ASIGNACION", "=", 1, 21),
            ("NUMERO", "1", 1, 23),
            ("FIN_INSTRUCCION", "LISTO", 1, 25),

            ("RESERVADA", "PILLE", 4, 1),
            ("IDENTIFICADOR", "b", 4, 7),
            ("RESERVADA", "COMO", 4, 9),
            ("TIPO", "ENTERO", 4, 14),
            ("ASIGNACION", "=", 4, 21),
            ("NUMERO", "2", 4, 23),
            ("FIN_INSTRUCCION", "LISTO", 4, 25),

            ("EOF", "", 4, 30),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Marcadores dentro de una cadena",
        '"/* hola */"',
        [
            ("TEXTO", '"/* hola */"', 1, 1),
            ("EOF", "", 1, 13),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Comentario sin cerrar",
        "a\n  /* sin cerrar\ncontinua",
        "Comentario de bloque sin cerrar en línea 2, columna 3",
    ))

    resultados.append(probar_caso(
        "TAREA 12 · Entrada vacía",
        "",
        [
            ("EOF", "", 1, 1),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 12 · Salto de línea al final",
        "x\n",
        [
            ("IDENTIFICADOR", "x", 1, 1),
            ("EOF", "", 2, 1),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 12 · Solo un comentario",
        "/* hola */",
        [
            ("EOF", "", 1, 11),
        ],
    ))



    print(f"\nResultado: {sum(resultados)}/{len(resultados)} pruebas correctas.")
    if not all(resultados):
        raise SystemExit(1)
