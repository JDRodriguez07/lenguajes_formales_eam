"""Tuquiquilulu: analizador léxico y seis pruebas del parcial.

Ejecutar: python parcial.py
Cada token contiene (tipo, lexema, línea, columna).
Las posiciones empiezan en 1. Una tabulación cuenta como una columna.
Este analizador reconoce tokens; no valida la gramática de las instrucciones.
"""

TIPOS = {"ENTERO", "DECIMAL", "TEXTO", "BOOLEANO"}
RESERVADAS = {"PILLE", "COMO"}
INICIO_COMENTARIO = "OJO:"
OPERADORES = {"+", "-", "*"}


def tokenizar_operadores(texto):
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

            while i < len(texto) and (texto[i].isalnum() or texto[i] == "_"):
                i += 1
                columna += 1

            palabra = texto[inicio:i]
            if palabra in TIPOS:
                tipo = "TIPO"
            elif palabra in RESERVADAS:
                tipo = "RESERVADA"
            elif palabra == "LISTO":
                tipo = "FIN_INSTRUCCION"
            else:
                tipo = "IDENTIFICADOR"

            tokens.append((tipo, palabra, linea, columna_inicio))

        # 7. Reconocer la asignación.
        elif c == "=":
            tokens.append(("ASIGNACION", c, linea, columna))
            i += 1
            columna += 1

        # 8. Reconocer operadores de un carácter.
        elif c in OPERADORES:
            tokens.append(("OPERADOR", c, linea, columna))
            i += 1
            columna += 1

        # 9. Detenerse ante un carácter no reconocido.
        else:
            raise SyntaxError(
                f"Error léxico: carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

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
        resultado = tokenizar_operadores(codigo)
        for token in resultado:
            print(token)
    except SyntaxError as error:
        resultado = str(error)
        print(resultado)

    coincide = resultado == esperado
    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")
    return coincide


if __name__ == "__main__":
    resultados = []

    # Válido 1: declaración con espacios.
    resultados.append(probar_caso(
        "CASO VÁLIDO 1 · Declaración sencilla",
        "PILLE puntos COMO ENTERO = 100 LISTO",
        [
            ("RESERVADA", "PILLE", 1, 1),
            ("IDENTIFICADOR", "puntos", 1, 7),
            ("RESERVADA", "COMO", 1, 14),
            ("TIPO", "ENTERO", 1, 19),
            ("ASIGNACION", "=", 1, 26),
            ("NUMERO", "100", 1, 28),
            ("FIN_INSTRUCCION", "LISTO", 1, 32),
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
        ],
    ))

    # Válido 3: comentario, salto de línea y literal decimal.
    resultados.append(probar_caso(
        "CASO VÁLIDO 3 · Dos líneas y comentario",
        "PILLE puntos COMO ENTERO = 100 LISTO OJO: puntaje inicial\n"
        "PILLE tiempo COMO DECIMAL = 3.5 LISTO",
        [
            ("RESERVADA", "PILLE", 1, 1),
            ("IDENTIFICADOR", "puntos", 1, 7),
            ("RESERVADA", "COMO", 1, 14),
            ("TIPO", "ENTERO", 1, 19),
            ("ASIGNACION", "=", 1, 26),
            ("NUMERO", "100", 1, 28),
            ("FIN_INSTRUCCION", "LISTO", 1, 32),
            ("RESERVADA", "PILLE", 2, 1),
            ("IDENTIFICADOR", "tiempo", 2, 7),
            ("RESERVADA", "COMO", 2, 14),
            ("TIPO", "DECIMAL", 2, 19),
            ("ASIGNACION", "=", 2, 27),
            ("NUMERO", "3.5", 2, 29),
            ("FIN_INSTRUCCION", "LISTO", 2, 33),
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

    print(f"\nResultado: {sum(resultados)}/{len(resultados)} pruebas correctas.")
    if not all(resultados):
        raise SystemExit(1)
