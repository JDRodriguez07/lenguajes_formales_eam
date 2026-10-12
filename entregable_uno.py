#Tarea 1: Saber en qué columna está cada pieza

def tokenizar_simple(texto): 
    tokens = [] 
    i = 0 
    columna = 1  # Inicializamos la columna en 1
    while i < len(texto): 
        c = texto[i] 
        if c == " ": 
            i += 1 
            columna += 1
        elif c.isdigit(): 
            inicio = i 
            columna_inicio = columna  # Guardamos la columna donde empieza el número
            while i < len(texto) and texto[i].isdigit(): 
                i += 1 
                columna += 1
            numero = texto[inicio:i]
            tokens.append(("NUMERO", numero, columna_inicio))  # Guardamos el número con la columna donde comenzó
        elif c == ";": 
            tokens.append(("SIMBOLO", c, columna))  # Usamos la columna actual
            i += 1
            columna += 1
        else: 
            raise SyntaxError(f"Carácter inesperado '{c}'") 
    return tokens 

# Tarea 2: Saltos de línea y número de línea 

def tokenizar_salto_linea(texto):
    tokens = []
    i = 0
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        if c == " ":
            i += 1
            columna += 1

        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        elif c.isdigit():
            inicio = i
            columna_inicio = columna

            while i < len(texto) and texto[i].isdigit():
                i += 1
                columna += 1

            numero = texto[inicio:i]
            tokens.append(("NUMERO", numero, linea, columna_inicio))

        elif c == ";":
            tokens.append(("SIMBOLO", c, linea, columna))
            i += 1
            columna += 1

        else:
            raise SyntaxError(
                f"Carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens

# Tarea 3: Palabras (nombres de variable) 

def tokenizar_palabra(texto):
    tokens = [] 
    i = 0 # i señala la posición interna dentro del texto.
    # Línea y columna son las posiciones visibles:
    linea = 1
    columna = 1

    while i < len(texto):
        c = texto[i]

        if c in " \t":
            i += 1
            columna += 1

        elif c == "\n":
            i += 1
            linea += 1
            columna = 1

        elif c.isdigit():
            inicio = i
            columna_inicio = columna

            while i < len(texto) and texto[i].isdigit():
                i += 1
                columna += 1

            numero = texto[inicio:i]

            tokens.append(
                ("NUMERO", numero, linea, columna_inicio)
            )

        elif c.isalpha():
            inicio = i
            columna_inicio = columna

            while (
                i < len(texto) and (texto[i].isalnum() or texto[i] == "_")
            ):
                i += 1
                columna += 1

            palabra = texto[inicio:i]
            tokens.append(("IDENTIFICADOR", palabra, linea, columna_inicio))
        
        elif c == ";":

            tokens.append(("SIMBOLO", c, linea, columna))
            i += 1
            columna += 1

        else:
            raise SyntaxError(
                f"Carácter inesperado '{c}' "
                f"en línea {linea}, columna {columna}"
            )

    return tokens

print(" ")
print("Tarea 1: Saber en qué columna está cada pieza:")
print(tokenizar_simple("20;"))
print(" ")

print("Tarea 2: Saltos de línea y número de línea:")
print(tokenizar_salto_linea("5;\n12;"))
print(" ")

print("Tarea 3: Palabras (nombres de variable):")
print(tokenizar_palabra("edad 20;\nnota_1 5;"))
