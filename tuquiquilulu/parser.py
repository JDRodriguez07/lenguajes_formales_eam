"""Parser por descenso recursivo. Construye el árbol; todavía no ejecuta.

Gramática EBNF del alcance del 14 de noviembre:
bloque      ::= "{" instruccion* "}"
programa    ::= instruccion* EOF
instruccion ::= declaracion | asignacion | salida | condicional | mientras
salida      ::= "QUIUBO" "(" expresion ")" "LISTO"
declaracion ::= "PILLE" IDENTIFICADOR "COMO" TIPO ("=" expresion)? "LISTO"
condicional ::= "PILAS" "(" condicion ")" "DE" "UNA" bloque
                ("O" "SI" "NO" bloque)? "LISTO"
asignacion  ::= IDENTIFICADOR "=" expresion "LISTO"
condicion   ::= expresion
expresion   ::= logica_o
termino     ::= unario (("*" | "/") unario)*
unario      ::= "-" unario | factor
factor      ::= NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | "(" expresion ")"
mientras    ::= "MIENTRAS" "(" condicion ")" "DE" "UNA" bloque "LISTO"
logica_o    ::= logica_y ("O" "DE" "PRONTO" logica_y)*
logica_y    ::= logica_no ("Y" "ADEMÁS" logica_no)*
logica_no   ::= "NADA" "DE" logica_no | comparacion
comparacion ::= aritmetica (COMPARADOR aritmetica)?
aritmetica  ::= termino (("+" | "-") termino)*

"=" es ASIGNACION; "LISTO" es FIN_INSTRUCCION; paréntesis son SIMBOLO.
PILLE y COMO son RESERVADA. Los signos aritméticos son OPERADOR.
"?" conserva la inicialización opcional del diseño original del lenguaje.
"""

from .tokens import ErrorSintactico
from .arbol import (
    Comparacion, Programa, Declaracion, Asignacion, OperacionBinaria,
    Numero, Cadena, Booleano, Variable, Mostrar, Bloque, Condicional,
    Mientras, OperacionUnaria, OperacionLogica, Negacion,
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

    def bloque(self):
        """Reconoce instrucciones entre llaves y conserva su apertura."""
        apertura = self.esperar("SIMBOLO", "{")
        instrucciones = []

        while not (
            self.actual().tipo == "SIMBOLO"
            and self.actual().texto == "}"
        ):
            if self.actual().tipo == "EOF":
                raise ErrorSintactico(
                    "bloque sin cerrar: se esperaba '}'",
                    apertura.linea,
                    apertura.columna,
                )

            instrucciones.append(self.instruccion())

        self.esperar("SIMBOLO", "}")

        return Bloque(apertura, instrucciones)

    def condicional(self):
        """Reconoce PILAS con un bloque y una alternativa opcional."""
        palabra = self.esperar("RESERVADA", "PILAS")

        self.esperar("SIMBOLO", "(")
        condicion = self.condicion()
        self.esperar("SIMBOLO", ")")

        self.esperar("RESERVADA", "DE")
        self.esperar("RESERVADA", "UNA")
        entonces = self.bloque()

        alternativa = None

        if (
            self.actual().tipo == "RESERVADA"
            and self.actual().texto == "O"
        ):
            self.esperar("RESERVADA", "O")
            self.esperar("RESERVADA", "SI")
            self.esperar("RESERVADA", "NO")
            alternativa = self.bloque()

        self.esperar("FIN_INSTRUCCION", "LISTO")

        return Condicional(
            palabra,
            condicion,
            entonces,
            alternativa,
        )

    def instruccion(self):
        token = self.actual()

        if token.tipo == "RESERVADA" and token.texto == "PILLE":
            return self.declaracion()

        if token.tipo == "RESERVADA" and token.texto == "QUIUBO":
            return self.salida()

        if token.tipo == "IDENTIFICADOR":
            return self.asignacion()

        if token.tipo == "RESERVADA" and token.texto == "PILAS":
            return self.condicional()

        if token.tipo == "RESERVADA" and token.texto == "MIENTRAS":
            return self.mientras()

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

    def aritmetica(self):
        izq = self.termino()

        while (
            self.actual().tipo == "OPERADOR"
            and self.actual().texto in ("+", "-")
        ):
            operador = self.avanzar()
            der = self.termino()
            izq = OperacionBinaria(izq, operador, der)

        return izq

    def termino(self):
        izq = self.unario()

        while (
            self.actual().tipo == "OPERADOR"
            and self.actual().texto in ("*", "/")
        ):
            operador = self.avanzar()
            der = self.unario()
            izq = OperacionBinaria(izq, operador, der)

        return izq

    def unario(self):
        """Reconoce el negativo antes de continuar con un factor."""
        token = self.actual()

        if token.tipo == "OPERADOR" and token.texto == "-":
            operador = self.avanzar()
            operando = self.unario()

            return OperacionUnaria(operador, operando)

        return self.factor()

    def condicion(self):
        """Reconoce la expresión que el intérprete exigirá como booleana."""
        return self.expresion()

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

    def mientras(self):
        """Reconoce la condición y el bloque de un ciclo."""
        palabra = self.esperar("RESERVADA", "MIENTRAS")

        self.esperar("SIMBOLO", "(")
        condicion = self.condicion()
        self.esperar("SIMBOLO", ")")

        self.esperar("RESERVADA", "DE")
        self.esperar("RESERVADA", "UNA")
        cuerpo = self.bloque()

        self.esperar("FIN_INSTRUCCION", "LISTO")

        return Mientras(palabra, condicion, cuerpo)

    def es_reservada(self, palabra):
        token = self.actual()
        return token.tipo == "RESERVADA" and token.texto == palabra

    def expresion(self):
        """Una expresión puede incluir aritmética, comparaciones y lógica."""
        return self.logica_o()

    def logica_o(self):
        izq = self.logica_y()

        while self.es_reservada("O"):
            operador = self.esperar("RESERVADA", "O")
            self.esperar("RESERVADA", "DE")
            self.esperar("RESERVADA", "PRONTO")

            der = self.logica_y()
            izq = OperacionLogica(izq, operador, der)

        return izq

    def logica_y(self):
        izq = self.logica_no()

        while self.es_reservada("Y"):
            operador = self.esperar("RESERVADA", "Y")
            self.esperar("RESERVADA", "ADEMÁS")

            der = self.logica_no()
            izq = OperacionLogica(izq, operador, der)

        return izq

    def logica_no(self):
        if self.es_reservada("NADA"):
            operador = self.esperar("RESERVADA", "NADA")
            self.esperar("RESERVADA", "DE")

            return Negacion(operador, self.logica_no())

        return self.comparacion()

    def comparacion(self):
        izq = self.aritmetica()

        if self.actual().tipo == "COMPARADOR":
            operador = self.avanzar()
            der = self.aritmetica()

            return Comparacion(izq, operador, der)

        return izq
