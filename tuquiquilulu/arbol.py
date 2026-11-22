"""Nodos del árbol: guardan estructura y tokens con su posición original."""

from dataclasses import dataclass
from .tokens import Token


@dataclass
class Numero:
    token: Token


@dataclass
class Cadena:
    token: Token


@dataclass
class Booleano:
    token: Token


@dataclass
class Variable:
    token: Token


@dataclass
class OperacionBinaria:
    izq: object
    operador: Token
    der: object


@dataclass
class Declaracion:
    tipo: Token
    nombre: Token
    valor: object | None


@dataclass
class Asignacion:
    nombre: Token
    valor: object

@dataclass
class Comparacion:
    izq: object
    operador: Token
    der: object

@dataclass
class Mostrar:
    palabra: Token
    valor: object


@dataclass
class Programa:
    instrucciones: list

@dataclass
class Bloque:
    apertura: Token
    instrucciones: list

def representar_arbol(nodo, nivel=0):
    """Devuelve texto para comparar en pruebas o mostrar en consola."""
    prefijo = "  " * nivel
    if isinstance(nodo, Programa):
        titulo, hijos = "Programa", nodo.instrucciones
    elif isinstance(nodo, Bloque):
        titulo, hijos = "Bloque", nodo.instrucciones
    elif isinstance(nodo, Declaracion):
        titulo = f"Declaracion {nodo.tipo.texto} {nodo.nombre.texto}"
        hijos = [] if nodo.valor is None else [nodo.valor]
        if nodo.valor is None:
            titulo += " (sin inicializacion)"
    elif isinstance(nodo, Asignacion):
        titulo, hijos = f"Asignacion {nodo.nombre.texto}", [nodo.valor]
    elif isinstance(nodo, OperacionBinaria):
        titulo, hijos = f"OperacionBinaria {nodo.operador.texto}", [nodo.izq, nodo.der]
    elif isinstance(nodo, (Numero, Cadena, Booleano, Variable)):
        titulo, hijos = f"{type(nodo).__name__} {nodo.token.texto}", []
    elif isinstance(nodo, Mostrar):
        titulo, hijos = "Mostrar", [nodo.valor]
    elif isinstance(nodo, Comparacion):
        titulo = f"Comparacion {nodo.operador.texto}"
        hijos = [nodo.izq, nodo.der]
    else:
        raise TypeError(f"Nodo desconocido: {type(nodo).__name__}")
    lineas = [prefijo + titulo]
    lineas.extend(representar_arbol(hijo, nivel + 1) for hijo in hijos)
    return "\n".join(lineas)


def mostrar_arbol(nodo):
    print(representar_arbol(nodo))
