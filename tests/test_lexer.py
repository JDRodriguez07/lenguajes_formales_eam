"""Pruebas del analizador léxico de Tuquiquilulu."""

from tuquiquilulu.tokens import Token, ErrorLexico
from tuquiquilulu.lexer import tokenizar

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
        resultado = tokenizar(codigo)
        for token in resultado:
            print(token)
    except ErrorLexico as error:
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
            Token("RESERVADA", "PILLE", 1, 1),
            Token("IDENTIFICADOR", "x", 1, 7),
            Token("RESERVADA", "COMO", 1, 9),
            Token("TIPO", "ENTERO", 1, 14),
            Token("ASIGNACION", "=", 1, 21),
            Token("NUMERO", "5", 1, 23),
            Token("FIN_INSTRUCCION", "LISTO", 1, 25),
            Token("EOF", "", 1, 30),
        ],
    ))

    # Válido 2: los operadores no necesitan espacios a sus lados.
    resultados.append(probar_caso(
        "CASO VÁLIDO 2 · Operadores sin espacios",
        "PILLE total COMO ENTERO = puntos+5*2 LISTO",
        [
            Token("RESERVADA", "PILLE", 1, 1),
            Token("IDENTIFICADOR", "total", 1, 7),
            Token("RESERVADA", "COMO", 1, 13),
            Token("TIPO", "ENTERO", 1, 18),
            Token("ASIGNACION", "=", 1, 25),
            Token("IDENTIFICADOR", "puntos", 1, 27),
            Token("OPERADOR", "+", 1, 33),
            Token("NUMERO", "5", 1, 34),
            Token("OPERADOR", "*", 1, 35),
            Token("NUMERO", "2", 1, 36),
            Token("FIN_INSTRUCCION", "LISTO", 1, 38),
            Token("EOF", "", 1, 43),
        ],
    ))

    # Válido 3: cadena cerrada, comentario, salto de línea y decimal.
    resultados.append(probar_caso(
        "CASO VÁLIDO 3 · Texto, comentario y decimal en dos líneas",
        'PILLE nombre COMO TEXTO = "Ana" LISTO OJO: comentario\n'
        "PILLE tiempo COMO DECIMAL = 3.5 LISTO",
        [
            Token("RESERVADA", "PILLE", 1, 1),
            Token("IDENTIFICADOR", "nombre", 1, 7),
            Token("RESERVADA", "COMO", 1, 14),
            Token("TIPO", "TEXTO", 1, 19),
            Token("ASIGNACION", "=", 1, 25),
            Token("TEXTO", '"Ana"', 1, 27),
            Token("FIN_INSTRUCCION", "LISTO", 1, 33),
            Token("RESERVADA", "PILLE", 2, 1),
            Token("IDENTIFICADOR", "tiempo", 2, 7),
            Token("RESERVADA", "COMO", 2, 14),
            Token("TIPO", "DECIMAL", 2, 19),
            Token("ASIGNACION", "=", 2, 27),
            Token("NUMERO", "3.5", 2, 29),
            Token("FIN_INSTRUCCION", "LISTO", 2, 33),
            Token("EOF", "", 2, 38),
        ],
    ))

    resultados.append(probar_caso(
        "CASO INVÁLIDO 1 · Carácter desconocido",
        "PILLE puntos COMO ENTERO = 100 @ LISTO",
        "Error léxico en línea 1, columna 32: carácter '@' no reconocido",
    ))

    # Usamos un decimal mal formado: '=' sí es válido en nuestro lenguaje.
    # En 3.4.5, el segundo punto está en la columna 32 de esta instrucción.
    resultados.append(probar_caso(
        "CASO INVÁLIDO 2 · Decimal mal formado",
        "PILLE tiempo COMO DECIMAL = 3.4.5 LISTO",
        "Error léxico en línea 1, columna 32: decimal mal formado",
    ))

    # Aquí la posición señala la comilla de apertura del texto sin cerrar.
    resultados.append(probar_caso(
        "CASO INVÁLIDO 3 · Texto sin cerrar en la segunda línea",
        'PILLE puntos COMO ENTERO = 0 LISTO\n'
        'PILLE categoria COMO TEXTO = "Historia LISTO',
        "Error léxico en línea 2, columna 30: cadena de texto sin cerrar",
    ))

    # Tarea 8: paréntesis, operadores y punto y coma.
    resultados.append(probar_caso(
        "TAREA 8 · Expresión con delimitadores",
        "(a+b)*2;",
        [
            Token("SIMBOLO", "(", 1, 1),
            Token("IDENTIFICADOR", "a", 1, 2),
            Token("OPERADOR", "+", 1, 3),
            Token("IDENTIFICADOR", "b", 1, 4),
            Token("SIMBOLO", ")", 1, 5),
            Token("OPERADOR", "*", 1, 6),
            Token("NUMERO", "2", 1, 7),
            Token("SIMBOLO", ";", 1, 8),
            Token("EOF", "", 1, 9),
        ],
    ))

    # El punto separado es símbolo; dentro de 3.14 es parte del número.
    resultados.append(probar_caso(
        "TAREA 8 · Punto y decimal",
        "System.out 3.14",
        [
            Token("IDENTIFICADOR", "System", 1, 1),
            Token("SIMBOLO", ".", 1, 7),
            Token("IDENTIFICADOR", "out", 1, 8),
            Token("NUMERO", "3.14", 1, 12),
            Token("EOF", "", 1, 16),
        ],
    ))

    # Tarea 8: llaves y coma.
    resultados.append(probar_caso(
        "TAREA 8 · Llaves y coma",
        "{a,b}",
        [
            Token("SIMBOLO", "{", 1, 1),
            Token("IDENTIFICADOR", "a", 1, 2),
            Token("SIMBOLO", ",", 1, 3),
            Token("IDENTIFICADOR", "b", 1, 4),
            Token("SIMBOLO", "}", 1, 5),
            Token("EOF", "", 1, 6),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Operadores dobles",
        "a==b a!=b a<=b a>=b",
        [
            Token("IDENTIFICADOR", "a", 1, 1),
            Token("OPERADOR", "==", 1, 2),
            Token("IDENTIFICADOR", "b", 1, 4),

            Token("IDENTIFICADOR", "a", 1, 6),
            Token("OPERADOR", "!=", 1, 7),
            Token("IDENTIFICADOR", "b", 1, 9),

            Token("IDENTIFICADOR", "a", 1, 11),
            Token("OPERADOR", "<=", 1, 12),
            Token("IDENTIFICADOR", "b", 1, 14),

            Token("IDENTIFICADOR", "a", 1, 16),
            Token("OPERADOR", ">=", 1, 17),
            Token("IDENTIFICADOR", "b", 1, 19),

            Token("EOF", "", 1, 20),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Operadores relacionales simples",
        "a<b a>b",
        [
            Token("IDENTIFICADOR", "a", 1, 1),
            Token("OPERADOR", "<", 1, 2),
            Token("IDENTIFICADOR", "b", 1, 3),
            Token("IDENTIFICADOR", "a", 1, 5),
            Token("OPERADOR", ">", 1, 6),
            Token("IDENTIFICADOR", "b", 1, 7),
            Token("EOF", "", 1, 8),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Comparación de igualdad",
        "x == 5",
        [
            Token("IDENTIFICADOR", "x", 1, 1),
            Token("OPERADOR", "==", 1, 3),
            Token("NUMERO", "5", 1, 6),
            Token("EOF", "", 1, 7),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Asignaciones separadas por un espacio",
        "x = = 5",
        [
            Token("IDENTIFICADOR", "x", 1, 1),
            Token("ASIGNACION", "=", 1, 3),
            Token("ASIGNACION", "=", 1, 5),
            Token("NUMERO", "5", 1, 7),
            Token("EOF", "", 1, 8),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 9 · Exclamación sin igual",
        "x ! 5",
        "Error léxico en línea 1, columna 3: carácter '!' no reconocido",
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Reservadas de control",
        "if else while",
        [
            Token("RESERVADA", "if", 1, 1),
            Token("RESERVADA", "else", 1, 4),
            Token("RESERVADA", "while", 1, 9),
            Token("EOF", "", 1, 14),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Palabras completas",
        "if iffy while_x PILAS PILAS_extra",
        [
            Token("RESERVADA", "if", 1, 1),
            Token("IDENTIFICADOR", "iffy", 1, 4),
            Token("IDENTIFICADOR", "while_x", 1, 9),
            Token("RESERVADA", "PILAS", 1, 17),
            Token("IDENTIFICADOR", "PILAS_extra", 1, 23),
            Token("EOF", "", 1, 34),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Valores booleanos",
        "SISAS NONAS MELO PAILA true false",
        [
            Token("BOOLEANO", "SISAS", 1, 1),
            Token("BOOLEANO", "NONAS", 1, 7),
            Token("BOOLEANO", "MELO", 1, 13),
            Token("BOOLEANO", "PAILA", 1, 18),
            Token("BOOLEANO", "true", 1, 24),
            Token("BOOLEANO", "false", 1, 29),
            Token("EOF", "", 1, 34),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 10 · Tipo, valor e identificadores",
        "BOOLEANO SISAS SISAS_extra true_x",
        [
            Token("TIPO", "BOOLEANO", 1, 1),
            Token("BOOLEANO", "SISAS", 1, 10),
            Token("IDENTIFICADOR", "SISAS_extra", 1, 16),
            Token("IDENTIFICADOR", "true_x", 1, 28),
            Token("EOF", "", 1, 34),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Comentario en una línea",
        "a/* hola */+b",
        [
            Token("IDENTIFICADOR", "a", 1, 1),
            Token("OPERADOR", "+", 1, 12),
            Token("IDENTIFICADOR", "b", 1, 13),
            Token("EOF", "", 1, 14),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Comentario de varias líneas",
        "PILLE a COMO ENTERO = 1 LISTO /* uno\n"
        "dos\n"
        "tres */\n"
        "PILLE b COMO ENTERO = 2 LISTO",
        [
            Token("RESERVADA", "PILLE", 1, 1),
            Token("IDENTIFICADOR", "a", 1, 7),
            Token("RESERVADA", "COMO", 1, 9),
            Token("TIPO", "ENTERO", 1, 14),
            Token("ASIGNACION", "=", 1, 21),
            Token("NUMERO", "1", 1, 23),
            Token("FIN_INSTRUCCION", "LISTO", 1, 25),

            Token("RESERVADA", "PILLE", 4, 1),
            Token("IDENTIFICADOR", "b", 4, 7),
            Token("RESERVADA", "COMO", 4, 9),
            Token("TIPO", "ENTERO", 4, 14),
            Token("ASIGNACION", "=", 4, 21),
            Token("NUMERO", "2", 4, 23),
            Token("FIN_INSTRUCCION", "LISTO", 4, 25),

            Token("EOF", "", 4, 30),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Marcadores dentro de una cadena",
        '"/* hola */"',
        [
            Token("TEXTO", '"/* hola */"', 1, 1),
            Token("EOF", "", 1, 13),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 11 · Comentario sin cerrar",
        "a\n  /* sin cerrar\ncontinua",
        "Error léxico en línea 2, columna 3: comentario de bloque sin cerrar",
    ))

    resultados.append(probar_caso(
        "TAREA 12 · Entrada vacía",
        "",
        [
            Token("EOF", "", 1, 1),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 12 · Salto de línea al final",
        "x\n",
        [
            Token("IDENTIFICADOR", "x", 1, 1),
            Token("EOF", "", 2, 1),
        ],
    ))

    resultados.append(probar_caso(
        "TAREA 12 · Solo un comentario",
        "/* hola */",
        [
            Token("EOF", "", 1, 11),
        ],
    ))

    print("\n" + "=" * 60)
    print("TAREA 14 · Datos del error por separado")

    codigo = "x\n  @"

    esperado = (
        "carácter '@' no reconocido",
        2,
        3,
    )

    print("\nEntrada:")
    print(codigo)

    print("\nSalida esperada (mensaje, línea, columna):")
    print(esperado)

    try:
        tokenizar(codigo)

    except ErrorLexico as error:
        resultado = (
            error.mensaje,
            error.linea,
            error.columna,
        )

        print("\nSalida real:")
        print(resultado)

        coincide = resultado == esperado

    else:
        print("\nSalida real: no se produjo el error esperado.")
        coincide = False


    resultados.append(probar_caso(
        "TAREA 16 · Primeras tres lineas del programa",
        "OJO: Programa de demostracion\n"
        "PILLE puntos COMO ENTERO = 2 LISTO\n"
        "PILLE precio COMO DECIMAL = 3.14 LISTO\n",
        [
            Token("RESERVADA", "PILLE", 2, 1),
            Token("IDENTIFICADOR", "puntos", 2, 7),
            Token("RESERVADA", "COMO", 2, 14),
            Token("TIPO", "ENTERO", 2, 19),
            Token("ASIGNACION", "=", 2, 26),
            Token("NUMERO", "2", 2, 28),
            Token("FIN_INSTRUCCION", "LISTO", 2, 30),

            Token("RESERVADA", "PILLE", 3, 1),
            Token("IDENTIFICADOR", "precio", 3, 7),
            Token("RESERVADA", "COMO", 3, 14),
            Token("TIPO", "DECIMAL", 3, 19),
            Token("ASIGNACION", "=", 3, 27),
            Token("NUMERO", "3.14", 3, 29),
            Token("FIN_INSTRUCCION", "LISTO", 3, 34),

            Token("EOF", "", 4, 1),
        ],
    ))

    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")
    resultados.append(coincide)

    print(f"\nResultado: {sum(resultados)}/{len(resultados)} pruebas correctas.")
    if not all(resultados):
        raise SystemExit(1)
