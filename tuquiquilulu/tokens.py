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


class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

        super().__init__(
            f"Error léxico en línea {linea}, "
            f"columna {columna}: {mensaje}"
        )