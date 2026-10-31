"""Tuquiquilulu: analizador léxico.
"""

from dataclasses import dataclass

@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):
        return (
            f"{self.tipo}({self.texto!r}) "
            f"en {self.linea}:{self.columna}"
        )

class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

        super().__init__(
            f"Error léxico en línea {linea}, "
            f"columna {columna}: {mensaje}"
        )


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

def tokenizar_error_propio(texto):
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
        resultado = tokenizar_error_propio(codigo)
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
        tokenizar_error_propio(codigo)

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

    print("\n¿Coinciden?:", "SÍ" if coincide else "NO")
    resultados.append(coincide)

    print(f"\nResultado: {sum(resultados)}/{len(resultados)} pruebas correctas.")
    if not all(resultados):
        raise SystemExit(1)
