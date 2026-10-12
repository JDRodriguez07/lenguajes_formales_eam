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

# Operadores aritméticos de un carácter
OPERADORES = {
    "+",
    "-",
    "*"
}


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

# Tarea 6.2: Literales de texto y decimales (según su lenguaje) 

def tokenizar_literales(texto):
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

        # 4. Reconocer números enteros y decimales
        elif c.isdigit():
            inicio = i
            linea_inicio = linea
            columna_inicio = columna

            # Leer la parte entera
            while (
                i < len(texto)
                and texto[i].isdigit()
            ):
                i += 1
                columna += 1

            # Comprobar si el número tiene punto decimal
            if i < len(texto) and texto[i] == ".":

                # El punto debe tener un dígito después
                if (
                    i + 1 >= len(texto)
                    or not texto[i + 1].isdigit()
                ):
                    raise SyntaxError(
                        "Decimal mal formado "
                        f"en línea {linea_inicio}, "
                        f"columna {columna_inicio}"
                    )

                # Consumir el punto decimal
                i += 1
                columna += 1

                # Leer la parte decimal
                while (
                    i < len(texto)
                    and texto[i].isdigit()
                ):
                    i += 1
                    columna += 1

                # Evitar números como 3.4.5
                if i < len(texto) and texto[i] == ".":
                    raise SyntaxError(
                        "Decimal mal formado "
                        f"en línea {linea_inicio}, "
                        f"columna {columna_inicio}"
                    )

            numero = texto[inicio:i]

            tokens.append(("NUMERO", numero, linea_inicio, columna_inicio))

        # 5. Reconocer cadenas de texto
        elif c == '"':
            inicio = i
            linea_inicio = linea
            columna_inicio = columna

            # Consumir la comilla inicial
            i += 1
            columna += 1

            # Buscar la comilla de cierre
            while (
                i < len(texto)
                and texto[i] != '"'
                and texto[i] != "\n"
            ):
                i += 1
                columna += 1

            # Si no encontramos la comilla de cierre
            if i >= len(texto) or texto[i] == "\n":
                raise SyntaxError(
                    "Cadena de texto sin cerrar "
                    f"en línea {linea_inicio}, "
                    f"columna {columna_inicio}"
                )

            # Consumir la comilla de cierre
            i += 1
            columna += 1

            cadena = texto[inicio:i]

            tokens.append(("TEXTO", cadena, linea_inicio, columna_inicio))

        # 6. Reconocer palabras completas
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

            tokens.append(( tipo, palabra, linea, columna_inicio))

        # 7. Reconocer el signo de asignación
        elif c == "=":
            tokens.append(("ASIGNACION", c, linea, columna))

            i += 1
            columna += 1

        # 8. Error léxico
        else:
            raise SyntaxError(
                f"Error léxico: carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens

# Tarea 6.3: Operadores de un carácter (+, -, *)

def tokenizar_operadores(texto):
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

        # 4. Reconocer números enteros y decimales
        elif c.isdigit():
            inicio = i
            linea_inicio = linea
            columna_inicio = columna

            # Leer la parte entera
            while (
                i < len(texto)
                and texto[i].isdigit()
            ):
                i += 1
                columna += 1

            # Comprobar si tiene punto decimal
            if i < len(texto) and texto[i] == ".":

                # El punto debe estar seguido de un dígito
                if (
                    i + 1 >= len(texto)
                    or not texto[i + 1].isdigit()
                ):
                    raise SyntaxError(
                        "Decimal mal formado "
                        f"en línea {linea_inicio}, "
                        f"columna {columna_inicio}"
                    )

                # Consumir el punto
                i += 1
                columna += 1

                # Leer la parte decimal
                while (
                    i < len(texto)
                    and texto[i].isdigit()
                ):
                    i += 1
                    columna += 1

                # Evitar números como 3.4.5
                if i < len(texto) and texto[i] == ".":
                    raise SyntaxError(
                        "Decimal mal formado "
                        f"en línea {linea_inicio}, "
                        f"columna {columna_inicio}"
                    )

            numero = texto[inicio:i]

            tokens.append(("NUMERO", numero, linea_inicio, columna_inicio))

        # 5. Reconocer cadenas de texto
        elif c == '"':
            inicio = i
            linea_inicio = linea
            columna_inicio = columna

            # Consumir la comilla inicial
            i += 1
            columna += 1

            # Buscar la comilla de cierre
            while (
                i < len(texto)
                and texto[i] != '"'
                and texto[i] != "\n"
            ):
                i += 1
                columna += 1

            # La cadena llegó al final o a otra línea sin cerrar
            if i >= len(texto) or texto[i] == "\n":
                raise SyntaxError(
                    "Cadena de texto sin cerrar "
                    f"en línea {linea_inicio}, "
                    f"columna {columna_inicio}"
                )

            # Consumir la comilla de cierre
            i += 1
            columna += 1

            cadena = texto[inicio:i]

            tokens.append(("TEXTO", cadena, linea_inicio, columna_inicio))

        # 6. Reconocer palabras completas
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

        # 7. Reconocer el signo de asignación
        elif c == "=":
            tokens.append(("ASIGNACION", c, linea, columna))

            i += 1
            columna += 1

        # 8. Reconocer operadores aritméticos
        elif c in OPERADORES:
            tokens.append(("OPERADOR", c, linea, columna))

            i += 1
            columna += 1

        # 9. Error léxico
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

# ========================================================
# =================== Prueba tarea 6.2 ===================
# ========================================================
print("\n======= PRUEBA TOKENIZACION LITERALES =======")
codigo_literal = "PILLE puntos COMO ENTERO = 100 LISTO"
resultado_literal = tokenizar_literales(codigo_literal)
for token in resultado_literal:
    print(token)

print(" ")
codigo_literal_dos = "PILLE tiempo COMO DECIMAL = 3.14 LISTO"
resultado_literal_dos = tokenizar_literales(codigo_literal_dos)
for token in resultado_literal_dos:
    print(token)

print(" ")
codigo_literal_tres = 'PILLE categoria COMO TEXTO = "Historia" LISTO'
resultado_literal_tres = tokenizar_literales(codigo_literal_tres)
for token in resultado_literal_tres:
    print(token)

print(" ")
codigo_literal_cuatro = 'PILLE categoria COMO TEXTO = "Historia LISTO'
print(f"Se prueba con la línea:\n'{codigo_literal_cuatro}'")
try:
    resultado_literal_cuatro = tokenizar_literales(codigo_literal_cuatro)
    print(resultado_literal_cuatro)

except SyntaxError as error:
    print(f"Error: {error}")

print(" ")
codigo_literal_cinco = (
    "PILLE puntos COMO ENTERO = 0 LISTO\n"
    'PILLE categoria COMO TEXTO = "Historia LISTO'
)
print(f"Se prueba con las líneas:\n'{codigo_literal_cinco}'")
try:
    resultado_literal_cinco = tokenizar_literales(codigo_literal_cinco)
    print(resultado_literal_cinco)

except SyntaxError as error:
    print(f"Error: {error}")

print(" ")
codigo_literal_seis = "PILLE tiempo COMO DECIMAL = 3.4.5 LISTO"
print(f"Se prueba con las líneas:\n'{codigo_literal_seis}'")
try:
    resultado_literal_seis = tokenizar_literales(codigo_literal_seis)
    print(resultado_literal_seis)
except SyntaxError as error:
    print(f"Error: {error}")

print(" ")
codigo_literal_siete = "PILLE tiempo COMO DECIMAL = 3. LISTO"
print(f"Se prueba con las líneas:\n'{codigo_literal_siete}'")
try:
    resultado_literal_siete = tokenizar_literales(codigo_literal_siete)
    print(resultado_literal_siete)
except SyntaxError as error:
    print(f"Error: {error}")

# ========================================================
# =================== Prueba tarea 6.3 ===================
# ========================================================
print("\n======= PRUEBA TOKENIZACION OPERADORES =======")
codigo_literal_ocho = "PILLE total COMO ENTERO = puntos + 5 * 2 LISTO"
resultado_literal_ocho = tokenizar_operadores(codigo_literal_ocho)
for token in resultado_literal_ocho:
    print(token)

print(" ")
codigo_operador_sin_espacios = (
    "PILLE total COMO ENTERO = puntos+5*2 LISTO"
)
resultado_operador_sin_espacios = tokenizar_operadores(
    codigo_operador_sin_espacios
)
for token in resultado_operador_sin_espacios:
    print(token)

print(" ")
codigo_operador_decimal = (
    "PILLE puntaje COMO DECIMAL = 3.5*2+1 LISTO"
)
resultado_operador_decimal = tokenizar_operadores(
    codigo_operador_decimal
)
for token in resultado_operador_decimal:
    print(token)

print(" ")
codigo_operador_resta = (
    "PILLE vidas COMO ENTERO = vidas-1 LISTO"
)
resultado_operador_resta = tokenizar_operadores(
    codigo_operador_resta
)
for token in resultado_operador_resta:
    print(token)

print(" ")
codigo_operador_invalido = (
    "PILLE total COMO ENTERO = puntos/2 LISTO"
)
print(f"Se prueba con la línea:\n'{codigo_operador_invalido}'")

try:
    resultado_operador_invalido = tokenizar_operadores(
        codigo_operador_invalido
    )
    print(resultado_operador_invalido)

except SyntaxError as error:
    print(f"Error: {error}")

print(" ")
codigo_operador_en_texto = (
    'PILLE mensaje COMO TEXTO = "Suma: 5+2" LISTO'
)
resultado_operador_en_texto = tokenizar_operadores(
    codigo_operador_en_texto
)
for token in resultado_operador_en_texto:
    print(token)

print(" ")
codigo_operador_completo = (
    "PILLE puntos COMO ENTERO = 100+50 LISTO "
    "OJO: puntaje inicial\n"
    "PILLE tiempo COMO DECIMAL = 3.5*2 LISTO"
)
resultado_operador_completo = tokenizar_operadores(
    codigo_operador_completo
)
for token in resultado_operador_completo:
    print(token)