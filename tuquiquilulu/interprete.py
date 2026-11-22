"""Ejecuta el árbol de Tuquiquilulu de forma progresiva."""

from .arbol import Numero, Cadena, Booleano, OperacionBinaria
from .tokens import ErrorSemantico

class Interprete:
    def __init__(self):
        # Aquí guardaremos las variables cuando implementemos declaraciones.
        self.entorno = {}

    def evaluar(self, nodo):
        """Convierte un nodo de expresión en un valor de Python."""

        if isinstance(nodo, Numero):
            texto = nodo.token.texto

            if "." in texto:
                return float(texto)

            return int(texto)

        if isinstance(nodo, Cadena):
            # El token conserva las comillas; el valor no las necesita.
            return nodo.token.texto[1:-1]

        if isinstance(nodo, Booleano):
            return nodo.token.texto in {"SISAS", "MELO", "true"}

        if isinstance(nodo, OperacionBinaria):
            izquierdo = self.evaluar(nodo.izq)
            derecho = self.evaluar(nodo.der)

            return self.operar(
                izquierdo,
                nodo.operador,
                derecho,
            )

        # Durante el desarrollo, señala los nodos aún no implementados.
        raise NotImplementedError(
            f"No se ha implementado la evaluación de "
            f"{type(nodo).__name__}"
        )

    def operar(self, izquierdo, operador, derecho):
        """Aplica las reglas de Tuquiquilulu a una operación binaria."""
        signo = operador.texto

        # Dos textos pueden unirse mediante +.
        if type(izquierdo) is str or type(derecho) is str:
            if (
                signo == "+"
                and type(izquierdo) is str
                and type(derecho) is str
            ):
                return izquierdo + derecho

            raise ErrorSemantico(
                f"no se puede usar '{signo}' con esos valores de texto",
                operador.linea,
                operador.columna,
            )

        # Los booleanos no participan en operaciones aritméticas.
        if (
            type(izquierdo) not in (int, float)
            or type(derecho) not in (int, float)
        ):
            raise ErrorSemantico(
                f"el operador '{signo}' requiere números",
                operador.linea,
                operador.columna,
            )

        if signo == "+":
            return izquierdo + derecho

        if signo == "-":
            return izquierdo - derecho

        if signo == "*":
            return izquierdo * derecho

        if signo == "/":
            if derecho == 0:
                raise ErrorSemantico(
                    "división por cero",
                    operador.linea,
                    operador.columna,
                )

            if type(izquierdo) is int and type(derecho) is int:
                # División entera truncada hacia cero.
                cociente = abs(izquierdo) // abs(derecho)

                if (izquierdo < 0) != (derecho < 0):
                    return -cociente

                return cociente

            return izquierdo / derecho

        raise NotImplementedError(
            f"Operador todavía no implementado: {signo}"
        )