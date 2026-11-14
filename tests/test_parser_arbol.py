"""Salidas esperadas calculadas a mano para la entrega del 14."""
from tuquiquilulu.lexer import tokenizar
from tuquiquilulu.parser import Parser
from tuquiquilulu.arbol import representar_arbol
from tuquiquilulu.tokens import ErrorDeLenguaje, ErrorSintactico, Token

CASOS = [
('Resta a la izquierda', 'PILLE r COMO ENTERO = 10 - 3 - 2 LISTO',
 'Programa\n  Declaracion ENTERO r\n    OperacionBinaria -\n      OperacionBinaria -\n        Numero 10\n        Numero 3\n      Numero 2', None),
('Falta LISTO', 'PILLE x COMO ENTERO = 5',
 "Error sintáctico en línea 1, columna 24: se esperaba 'LISTO' y llegó el fin del archivo", ErrorSintactico),
('Operadores consecutivos', 'PILLE y COMO ENTERO = 4 + * 2 LISTO',
 "Error sintáctico en línea 1, columna 27: se esperaba un número, un texto, un booleano, una variable o '(' y llegó '*'", ErrorSintactico),
('Falta paréntesis', 'PILLE z COMO ENTERO = (1 + 2 LISTO',
 "Error sintáctico en línea 1, columna 30: se esperaba ')' y llegó 'LISTO'", ErrorSintactico),
('Multiplicación antes de suma', 'PILLE total COMO ENTERO = a + 5 * 2 LISTO',
 'Programa\n  Declaracion ENTERO total\n    OperacionBinaria +\n      Variable a\n      OperacionBinaria *\n        Numero 5\n        Numero 2', None),
('Paréntesis y asignación', 'x = (1 + 2) * 3 LISTO',
 'Programa\n  Asignacion x\n    OperacionBinaria *\n      OperacionBinaria +\n        Numero 1\n        Numero 2\n      Numero 3', None),
('Dos declaraciones y división', 'PILLE edad COMO ENTERO = 20 LISTO\nPILLE nota COMO DECIMAL = edad / 4.0 LISTO',
 'Programa\n  Declaracion ENTERO edad\n    Numero 20\n  Declaracion DECIMAL nota\n    OperacionBinaria /\n      Variable edad\n      Numero 4.0', None),
('División a la izquierda', 'x = 8 / 4 / 2 LISTO',
 'Programa\n  Asignacion x\n    OperacionBinaria /\n      OperacionBinaria /\n        Numero 8\n        Numero 4\n      Numero 2', None),
('Comentario y división', 'x = 8/* comentario */ / 2 LISTO',
 'Programa\n  Asignacion x\n    OperacionBinaria /\n      Numero 8\n      Numero 2', None),
('Texto y booleano', 'PILLE nombre COMO TEXTO = "Ana" LISTO\nPILLE activo COMO BOOLEANO = SISAS LISTO',
 'Programa\n  Declaracion TEXTO nombre\n    Cadena "Ana"\n  Declaracion BOOLEANO activo\n    Booleano SISAS', None),
('Inicialización opcional', 'PILLE puntos COMO ENTERO LISTO',
 'Programa\n  Declaracion ENTERO puntos (sin inicializacion)', None),
('Archivo vacío', '', 'Programa', None),
('Falta nombre', 'PILLE = 5 LISTO',
 "Error sintáctico en línea 1, columna 7: se esperaba un IDENTIFICADOR y llegó '='", ErrorSintactico),
('Error en segunda línea', 'PILLE x COMO ENTERO = 1 LISTO\nx = * 2 LISTO',
 "Error sintáctico en línea 2, columna 5: se esperaba un número, un texto, un booleano, una variable o '(' y llegó '*'", ErrorSintactico),
('Tokens sobrantes', 'x = 1 LISTO )',
 "Error sintáctico en línea 1, columna 13: se esperaba una declaración o asignación y llegó ')'", ErrorSintactico),
('Todavía no valida tipos', 'PILLE x COMO ENTERO = "hola" LISTO',
 'Programa\n  Declaracion ENTERO x\n    Cadena "hola"', None),
]

def comprobar(nombre, entrada, esperado, resultado, coincide):
    print('\n' + '=' * 60)
    print('PARSER ·', nombre)
    print('\nEntrada:\n' + entrada)
    print('\nSalida esperada:\n' + str(esperado))
    print('\nSalida real:\n' + str(resultado))
    print('\n¿Coinciden?:', 'SÍ' if coincide else 'NO')
    return coincide

def main():
    correctas = 0
    for nombre, entrada, esperado, error_esperado in CASOS:
        clase_error = None
        try:
            resultado = representar_arbol(Parser(tokenizar(entrada)).programa())
        except ErrorDeLenguaje as error:
            resultado, clase_error = str(error), type(error)
        correctas += comprobar(nombre, entrada, esperado, resultado,
                               resultado == esperado and clase_error is error_esperado)
    entrada = 'x = 8 / 2 LISTO'
    nodo = Parser(tokenizar(entrada)).programa().instrucciones[0]
    esperado = [Token('IDENTIFICADOR', 'x', 1, 1), Token('OPERADOR', '/', 1, 7), Token('NUMERO', '2', 1, 9)]
    resultado = [nodo.nombre, nodo.valor.operador, nodo.valor.der.token]
    correctas += comprobar('Posiciones en el árbol', entrada, esperado, resultado, resultado == esperado)
    parser = Parser(tokenizar('x'))
    resultado = [parser.avanzar(), parser.posicion, parser.actual()]
    esperado = [Token('IDENTIFICADOR', 'x', 1, 1), 1, Token('EOF', '', 1, 2)]
    correctas += comprobar('avanzar devuelve el token', 'x', esperado, resultado, resultado == esperado)
    parser = Parser(tokenizar('x = 1 LISTO'))
    try:
        parser.esperar('NUMERO')
        resultado = None
    except ErrorSintactico as error:
        resultado = (error.linea, error.columna, parser.posicion)
    esperado = (1, 1, 0)
    correctas += comprobar('esperar no avanza si falla', 'x = 1 LISTO', esperado, resultado, resultado == esperado)
    total = len(CASOS) + 3
    print(f'\nResultado: {correctas}/{total} pruebas correctas.')
    return 0 if correctas == total else 1

if __name__ == '__main__':
    raise SystemExit(main())
