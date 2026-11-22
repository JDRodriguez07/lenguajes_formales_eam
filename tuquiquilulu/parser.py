"""Parser por descenso recursivo. Construye el árbol; todavía no ejecuta.

Gramática EBNF del alcance del 14 de noviembre:
programa    ::= instruccion* EOF
instruccion ::= declaracion | asignacion | salida
salida      ::= "QUIUBO" "(" expresion ")" "LISTO"
declaracion ::= "PILLE" IDENTIFICADOR "COMO" TIPO ("=" expresion)? "LISTO"
asignacion  ::= IDENTIFICADOR "=" expresion "LISTO"
condicion ::= expresion COMPARADOR expresion
expresion   ::= termino (("+" | "-") termino)*
termino     ::= factor (("*" | "/") factor)*
factor      ::= NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | "(" expresion ")"

"=" es ASIGNACION; "LISTO" es FIN_INSTRUCCION; paréntesis son SIMBOLO.
PILLE y COMO son RESERVADA. Los signos aritméticos son OPERADOR.
"?" conserva la inicialización opcional del diseño original del lenguaje.
"""

from .tokens import ErrorSintactico
from .arbol import (
    Comparacion, Programa, Declaracion, Asignacion, OperacionBinaria,
    Numero, Cadena, Booleano, Variable, Mostrar,
)


class Parser:
    """Recibe la lista terminada en EOF que produce el lexer."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        """Consulta sin consumir el token."""
        return self.tokens[self.posicion]

    def avanzar(self):
        """Devuelve el token consumido y avanza sin sobrepasar EOF."""
        token = self.actual()
        if token.tipo != "EOF":
            self.posicion += 1
        return token

    def esperar(self, tipo, texto=None):
        """Comprueba, consume y devuelve; si no coincide, informa su posición."""
        token = self.actual()
        if token.tipo != tipo or (texto is not None and token.texto != texto):
            esperado = repr(texto) if texto is not None else f"un {tipo}"
            recibido = "el fin del archivo" if token.tipo == "EOF" else repr(token.texto)
            raise ErrorSintactico(
                f"se esperaba {esperado} y llegó {recibido}",
                token.linea, token.columna,
            )
        return self.avanzar()

    def programa(self):
        instrucciones = []
        while self.actual().tipo != "EOF":
            instrucciones.append(self.instruccion())
        self.esperar("EOF")
        return Programa(instrucciones)

    def instruccion(self):
        token = self.actual()

        if token.tipo == "RESERVADA" and token.texto == "PILLE":
            return self.declaracion()

        if token.tipo == "RESERVADA" and token.texto == "QUIUBO":
            return self.salida()

        if token.tipo == "IDENTIFICADOR":
            return self.asignacion()

        raise ErrorSintactico(
            "se esperaba una declaración, asignación o salida "
            f"y llegó {token.texto!r}",
            token.linea,
            token.columna,
        )

    def declaracion(self):
        self.esperar("RESERVADA", "PILLE")
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("RESERVADA", "COMO")
        tipo = self.esperar("TIPO")
        valor = None
        if self.actual().tipo == "ASIGNACION":
            self.esperar("ASIGNACION", "=")
            valor = self.expresion()
        self.esperar("FIN_INSTRUCCION", "LISTO")
        return Declaracion(tipo, nombre, valor)

    def asignacion(self):
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("ASIGNACION", "=")
        valor = self.expresion()
        self.esperar("FIN_INSTRUCCION", "LISTO")
        return Asignacion(nombre, valor)

    def salida(self):
        """Reconoce una instrucción de salida y construye su nodo."""
        palabra = self.esperar("RESERVADA", "QUIUBO")
        self.esperar("SIMBOLO", "(")
        valor = self.expresion()
        self.esperar("SIMBOLO", ")")
        self.esperar("FIN_INSTRUCCION", "LISTO")

        return Mostrar(palabra, valor)

    def expresion(self):
        izq = self.termino()
        while self.actual().tipo == "OPERADOR" and self.actual().texto in ("+", "-"):
            operador = self.avanzar()
            der = self.termino()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    def termino(self):
        izq = self.factor()
        while self.actual().tipo == "OPERADOR" and self.actual().texto in ("*", "/"):
            operador = self.avanzar()
            der = self.factor()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    def condicion(self):
        """Reconoce dos expresiones separadas por un comparador."""
        izquierdo = self.expresion()
        operador = self.esperar("COMPARADOR")
        derecho = self.expresion()

        return Comparacion(
            izquierdo,
            operador,
            derecho,
        )

    def factor(self):
        token = self.actual()
        if token.tipo == "NUMERO":
            return Numero(self.avanzar())
        if token.tipo == "TEXTO":
            return Cadena(self.avanzar())
        if token.tipo == "BOOLEANO":
            return Booleano(self.avanzar())
        if token.tipo == "IDENTIFICADOR":
            return Variable(self.avanzar())
        if token.tipo == "SIMBOLO" and token.texto == "(":
            self.avanzar()
            dentro = self.expresion()
            self.esperar("SIMBOLO", ")")
            return dentro
        recibido = "el fin del archivo" if token.tipo == "EOF" else repr(token.texto)
        raise ErrorSintactico(
            "se esperaba un número, un texto, un booleano, una variable o '(' "
            f"y llegó {recibido}", token.linea, token.columna,
        )
    
