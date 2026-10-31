# Mi primer programa

nombre = "Juan Rodríguez"
edad = 28
edad_proximo_año = edad + 1

print("==========================================")
print("MINI EJERCICIO 1")
print("==========================================")

print("nombre: ", nombre)
print("edad: ", edad)
print("edad del próximo año: ", edad_proximo_año)
print(" ")


print("==========================================")
print("MINI EJERCICIO 2")
print("==========================================")

texto = "a3b22cdflan49jsn2"
lista = []

for caracter in texto:
    if caracter.isdigit():
        print(caracter, end=" ")

print("\n")

print("==========================================")
print("MINI EJERCICIO 3")
print("==========================================")

lista_tuplas = []

for caracter in texto:
    if caracter.isdigit():
        lista_tuplas.append(("DIGITO",(caracter)))

print(lista_tuplas)

print("\n")

print("==========================================")
print("MINI EJERCICIO 4")
print("==========================================")

def funcion_digitos(texto):
    lista_tuplas = []
    for caracter in texto:
        if caracter.isdigit():
            lista_tuplas.append(("DIGITO",(caracter)))
    return lista_tuplas

texto_uno = "kj45k32bqhre8h288weqeio"
texto_dos = "po43ncsb3485cdsjkjnw8"
texto_tres = "23h4fdahowih9q4sd123dsakj3"

print("Resultados para el texto 1:")
print(funcion_digitos(texto_uno))
print(" ")
print("Resultados para el texto 2:")
print(funcion_digitos(texto_dos))
print(" ")
print("Resultados para el texto 3:")
print(funcion_digitos(texto_tres))
print(" ")


print("==========================================")
print("MINI EJERCICIO 4")
print("==========================================")

#Modificar digitos(texto) para que lance un error si encuentra un 
#carácter que no es dígito ni letra. Probar con "a1b" y "a1@" 
# usando try / except

def funcion_digitos_modificado():
    texto = input(str("Ingrese un texto: "))
    lista = []
    for caracter in texto:
        try:
            if caracter.isalnum():
                lista.append(caracter)
            else:
                raise ValueError(f"El carácter '{caracter}' no es alfanumérico.")
        except ValueError as e:
            print(f"Error: {e}")            
    print(" ")
    return lista

funcion_digitos_modificado()

print("==========================================")
print("Presentado por: ")
print("Juan David Rodríguez")
print("Diego Andrés Osorio")
print("Anggy Dahiana Ruiz")
print("Valentina Marín Flórez")