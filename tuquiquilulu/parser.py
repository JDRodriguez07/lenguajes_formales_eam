"""Prototipo del parser de tuquiquilulu."""

class Parser:
    """Recorre una lista de tokens terminada en EOF."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        """Devuelve el token actual sin cambiar de posición."""
        return self.tokens[self.posicion]

    def avanzar(self):
        """Avanza al siguiente token sin sonbrepasar EOPF."""
        if self.actual().tipo != "EOF":
            self.posicion += 1
            