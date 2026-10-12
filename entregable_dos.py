# Tipos permitidos en Tuquiquilulu
TIPOS = {
    "ENTERO",
    "DECIMAL",
    "TEXTO",
    "BOOLEANO"
}

# Palabras reservadas utilizadas en una declaración
RESERVADAS = {
    "PILLE",
    "COMO"
}


# Símbolo que inicia un comentario
INICIO_COMENTARIO = "OJO:"



# Tarea 4: Palabras reservadas (los tipos) 

def tokenizar_reservadas(texto):
    tokens = []

    i = 0
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        # Ignorar espacios y tabulaciones
        if c in " \t":
            i += 1
            columna += 1

        # Procesar saltos de línea
        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        # Reconocer números completos
        elif c.isdigit():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and texto[i].isdigit()
            ):
                i += 1
                columna += 1

            numero = texto[inicio:i]

            tokens.append(
                (
                    "NUMERO",
                    numero,
                    linea,
                    columna_inicio
                )
            )

        # Reconocer palabras completas
        elif c.isalpha():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto) and (texto[i].isalnum() or texto[i] == "_")
            ):
                i += 1
                columna += 1

            palabra = texto[inicio:i]

            # La mejora de la tarea 4 está aquí
            if palabra in TIPOS:
                tipo = "TIPO"
            else:
                tipo = "IDENTIFICADOR"

            tokens.append((tipo, palabra, linea, columna_inicio))

        # Reconocer el punto y coma
        elif c == ";":
            tokens.append(("SIMBOLO", c, linea, columna))
            i += 1
            columna += 1

        # Carácter desconocido
        else:
            raise SyntaxError(
                f"Carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens

# Tarea 5: El signo de asignación y el fin de instrucción de su lenguaje 

def tokenizar_asignacion(texto):
    tokens = []

    i = 0
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        # Ignorar espacios y tabulaciones
        if c in " \t":
            i += 1
            columna += 1

        # Procesar saltos de línea
        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        # Reconocer números completos
        elif c.isdigit():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and texto[i].isdigit()
            ):
                i += 1
                columna += 1

            numero = texto[inicio:i]

            tokens.append(
                (
                    "NUMERO",
                    numero,
                    linea,
                    columna_inicio
                )
            )

        # Reconocer palabras completas
        elif c.isalpha():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and (
                    texto[i].isalnum()
                    or texto[i] == "_"
                )
            ):
                i += 1
                columna += 1

            palabra = texto[inicio:i]

            # Clasificar la palabra completa
            if palabra in TIPOS:
                tipo = "TIPO"

            elif palabra in RESERVADAS:
                tipo = "RESERVADA"

            elif palabra == "LISTO":
                tipo = "FIN_INSTRUCCION"

            else:
                tipo = "IDENTIFICADOR"

            tokens.append(
                (
                    tipo,
                    palabra,
                    linea,
                    columna_inicio
                )
            )

        # Reconocer el signo de asignación
        elif c == "=":
            tokens.append(
                (
                    "ASIGNACION",
                    c,
                    linea,
                    columna
                )
            )

            i += 1
            columna += 1

        # Cualquier otro carácter genera error
        else:
            raise SyntaxError(
                f"Carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens


# Tarea 6: Comentarios 

def tokenizar_comentarios(texto):
    tokens = []

    i = 0
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        # 1. Ignorar espacios y tabulaciones
        if c in " \t":
            i += 1
            columna += 1

        # 2. Procesar saltos de línea
        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        # 3. Reconocer e ignorar comentarios
        elif texto.startswith(INICIO_COMENTARIO, i):

            # Avanzar hasta encontrar un salto de línea
            while (
                i < len(texto)
                and texto[i] != "\n"
            ):
                i += 1
                columna += 1

            # No hacemos tokens.append(),
            # porque el comentario se descarta.

        # 4. Reconocer números enteros
        elif c.isdigit():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and texto[i].isdigit()
            ):
                i += 1
                columna += 1

            numero = texto[inicio:i]
            tokens.append(("NUMERO", numero, linea, columna_inicio))

        # 5. Reconocer palabras completas
        elif c.isalpha():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and (
                    texto[i].isalnum()
                    or texto[i] == "_"
                )
            ):
                i += 1
                columna += 1

            palabra = texto[inicio:i]

            # Clasificar la palabra
            if palabra in TIPOS:
                tipo = "TIPO"

            elif palabra in RESERVADAS:
                tipo = "RESERVADA"

            elif palabra == "LISTO":
                tipo = "FIN_INSTRUCCION"

            else:
                tipo = "IDENTIFICADOR"

            tokens.append((tipo, palabra, linea, columna_inicio))

        # 6. Reconocer el signo de asignación
        elif c == "=":
            tokens.append(("ASIGNACION", c, linea, columna))

            i += 1
            columna += 1

        # 7. Carácter desconocido
        else:
            raise SyntaxError(
                f"Carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens

# Tarea 6.1: Errores léxicos con posición 

def tokenizar_errores(texto):
    tokens = []

    i = 0
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        # 1. Ignorar espacios y tabulaciones
        if c in " \t":
            i += 1
            columna += 1

        # 2. Procesar saltos de línea
        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        # 3. Reconocer e ignorar comentarios
        elif texto.startswith(INICIO_COMENTARIO, i):

            while (
                i < len(texto)
                and texto[i] != "\n"
            ):
                i += 1
                columna += 1

        # 4. Reconocer números enteros
        elif c.isdigit():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and texto[i].isdigit()
            ):
                i += 1
                columna += 1

            numero = texto[inicio:i]

            tokens.append(("NUMERO", numero, linea, columna_inicio))

        # 5. Reconocer palabras completas
        elif c.isalpha():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto)
                and (
                    texto[i].isalnum()
                    or texto[i] == "_"
                )
            ):
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

        # 6. Reconocer el signo de asignación
        elif c == "=":
            tokens.append(("ASIGNACION", c, linea, columna))
            
            i += 1
            columna += 1

        # 7. Error léxico
        else:
            raise SyntaxError(
                f"Error léxico: carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens



# ======================================================
# =================== Prueba tarea 4 ===================
# ======================================================
print("\n======= PRUEBA TOKENIZACION RESERVADAS =======")
codigo_reservada = "ENTERO edad"
resultado_reservada = tokenizar_reservadas(codigo_reservada)
print(resultado_reservada)

# ======================================================
# =================== Prueba tarea 5 ===================
# ======================================================
print("\n======= PRUEBA TOKENIZACION ASIGNACIÓN =======")
codigo_asignacion = "PILLE puntos COMO ENTERO = 0 LISTO"
resultado_asignacion = tokenizar_asignacion(codigo_asignacion)
for token in resultado_asignacion:
    print(token)

# ======================================================
# =================== Prueba tarea 6 ===================
# ======================================================
print("\n======= PRUEBA TOKENIZACION COMENTARIO =======")
codigo_comentario = (
    "PILLE puntos COMO ENTERO = 0 LISTO "
    "OJO: puntos iniciales"
)
resultado_comentario = tokenizar_comentarios(codigo_comentario)
for token in resultado_comentario:
    print(token)

print(" ")
codigo_comentario_dos = (
    "PILLE puntos COMO ENTERO = 0 LISTO "
    "OJO: puntos iniciales\n"
    "PILLE vidas COMO ENTERO = 3 LISTO"
)
resultado_comentario_dos = tokenizar_comentarios(codigo_comentario_dos)
for token in resultado_comentario_dos:
    print(token)

# ========================================================
# =================== Prueba tarea 6.1 ===================
# ========================================================
print("\n======= PRUEBA TOKENIZACION ERROR =======")
codigo_error = "PILLE puntos COMO ENTERO = 0 @ LISTO"
print(f"Se prueba con la línea: '{codigo_error}'")
try:
    resultado_error = tokenizar_errores(codigo_error)
    print(resultado_error)
except SyntaxError as error:
    print(error)

print(" ")
codigo_error_dos = (
    "PILLE puntos COMO ENTERO = 0 LISTO\n"
    "PILLE vidas COMO ENTERO = @ LISTO"
)

print(f"Se prueba con las líneas:\n'{codigo_error_dos}'")
try:
    resultado_error_dos = tokenizar_errores(codigo_error_dos)
    print(resultado_error_dos)

except SyntaxError as error:
    print(error)
