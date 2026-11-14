"""Clases utilizadas por el analizador léxico."""

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


class ErrorDeLenguaje(Exception):
    """Datos comunes de los errores de las fases del lenguaje."""

    fase = "Error"

    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

        super().__init__(
            f"{self.fase} en línea {linea}, "
            f"columna {columna}: {mensaje}"
        )

class ErrorLexico(ErrorDeLenguaje):
    fase = "Error léxico"


class ErrorSintactico(ErrorDeLenguaje):
    fase = "Error sintáctico"
