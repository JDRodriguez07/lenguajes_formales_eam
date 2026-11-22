"""Ejecuta el árbol de Tuquiquilulu de forma progresiva."""

from .arbol import Numero, Cadena, Booleano


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

        # Durante el desarrollo, señala los nodos aún no implementados.
        raise NotImplementedError(
            f"No se ha implementado la evaluación de "
            f"{type(nodo).__name__}"
        )