"""Ejecuta el árbol de Tuquiquilulu de forma progresiva."""

from .arbol import (
    Numero,
    Cadena,
    Comparacion,
    Booleano,
    OperacionBinaria,
    Variable,
    Declaracion,
    Asignacion,
    Mostrar,
    Bloque,
    Condicional,
)
from .tokens import ErrorSemantico

ACEPTA = {
    "ENTERO": (int,),
    "DECIMAL": (int, float),
    "TEXTO": (str,),
    "BOOLEANO": (bool,),
}

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

        if isinstance(nodo, Variable):
            datos = self.buscar_variable(nodo.token)

            if not datos["inicializada"]:
                raise ErrorSemantico(
                    f"la variable '{nodo.token.texto}' "
                    "no tiene un valor asignado",
                    nodo.token.linea,
                    nodo.token.columna,
                )

            return datos["valor"]

        if isinstance(nodo, Comparacion):
            izquierdo = self.evaluar(nodo.izq)
            derecho = self.evaluar(nodo.der)

            return self.comparar(
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

    def buscar_variable(self, token):
        """Busca una variable o informa que no ha sido declarada."""
        nombre = token.texto

        if nombre not in self.entorno:
            raise ErrorSemantico(
                f"la variable '{nombre}' no ha sido declarada",
                token.linea,
                token.columna,
            )

        return self.entorno[nombre]

    def validar_tipo(self, tipo, valor, token):
        """Comprueba el tipo y devuelve el valor listo para guardar."""
        if type(valor) not in ACEPTA[tipo]:
            raise ErrorSemantico(
                f"no se puede guardar ese valor en la variable "
                f"'{token.texto}' de tipo {tipo}",
                token.linea,
                token.columna,
            )

        # Las variables DECIMAL guardan sus números como float.
        if tipo == "DECIMAL":
            return float(valor)

        return valor

    def ejecutar_programa(self, programa):
        """Ejecuta las instrucciones en el orden del archivo."""
        for instruccion in programa.instrucciones:
            self.ejecutar(instruccion)

    def ejecutar(self, nodo):
        """Ejecuta una declaración, asignación o salida."""

        if isinstance(nodo, Declaracion):
            nombre = nodo.nombre.texto

            if nombre in self.entorno:
                linea_anterior = self.entorno[nombre]["linea"]

                raise ErrorSemantico(
                    f"la variable '{nombre}' ya fue declarada "
                    f"en la línea {linea_anterior}",
                    nodo.nombre.linea,
                    nodo.nombre.columna,
                )

            inicializada = nodo.valor is not None
            valor = None

            if inicializada:
                valor = self.evaluar(nodo.valor)
                valor = self.validar_tipo(
                    nodo.tipo.texto,
                    valor,
                    nodo.nombre,
                )

            self.entorno[nombre] = {
                "tipo": nodo.tipo.texto,
                "valor": valor,
                "linea": nodo.nombre.linea,
                "inicializada": inicializada,
            }
            return

        if isinstance(nodo, Asignacion):
            datos = self.buscar_variable(nodo.nombre)

            valor = self.evaluar(nodo.valor)
            valor = self.validar_tipo(
                datos["tipo"],
                valor,
                nodo.nombre,
            )

            datos["valor"] = valor
            datos["inicializada"] = True
            return

        if isinstance(nodo, Mostrar):
            valor = self.evaluar(nodo.valor)

            if type(valor) is bool:
                print("SISAS" if valor else "NONAS")
            else:
                print(valor)

            return

        if isinstance(nodo, Bloque):
            for instruccion in nodo.instrucciones:
                self.ejecutar(instruccion)
            return

        if isinstance(nodo, Condicional):
            resultado = self.evaluar(nodo.condicion)

            if type(resultado) is not bool:
                raise ErrorSemantico(
                    "la condición de PILAS debe ser un booleano",
                    nodo.palabra.linea,
                    nodo.palabra.columna,
                )

            if resultado:
                self.ejecutar(nodo.entonces)
            elif nodo.alternativa is not None:
                self.ejecutar(nodo.alternativa)

            return

        raise NotImplementedError(
            f"No se ha implementado la ejecución de "
            f"{type(nodo).__name__}"
        )

    def comparar(self, izquierdo, operador, derecho):
        """Compara valores aplicando las reglas de nuestro lenguaje."""
        signo = operador.texto

        ambos_numeros = (
            type(izquierdo) in (int, float)
            and type(derecho) in (int, float)
        )

        mismo_tipo = type(izquierdo) is type(derecho)

        # Igualdad y diferencia admiten números, textos y booleanos.
        if signo in ("==", "!="):
            if not (ambos_numeros or mismo_tipo):
                raise ErrorSemantico(
                    "no se pueden comparar valores de tipos incompatibles",
                    operador.linea,
                    operador.columna,
                )

            if signo == "==":
                return izquierdo == derecho

            return izquierdo != derecho

        # Las comparaciones de orden solo admiten números.
        if not ambos_numeros:
            raise ErrorSemantico(
                f"el comparador '{signo}' requiere números",
                operador.linea,
                operador.columna,
            )

        if signo == "<":
            return izquierdo < derecho

        if signo == ">":
            return izquierdo > derecho

        if signo == "<=":
            return izquierdo <= derecho

        if signo == ">=":
            return izquierdo >= derecho

        raise NotImplementedError(
            f"Comparador todavía no implementado: {signo}"
        )