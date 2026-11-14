# Grupo 1 - Los Más Chimbas

Proyecto de Lenguajes Formales — EAM

## Integrantes

- Juan David Rodríguez
- Anggy Ruiz
- Valentina Marín
- Diego Osorio

## Dominio del sistema

Nuestro sistema es un juego de preguntas en línea tipo Kahoot. Varios jugadores
se conectan a una sala, responden preguntas contra el reloj y van ganando puntos
según si aciertan y qué tan rápido contestan. El sistema tiene que decidir cosas
como cuántos puntos dar, cuándo bajar la dificultad, cuándo quitar una vida y
cuándo se acaba la partida.

Al lenguaje lo llamamos **Tuquiquilulu** y está escrito en jerga colombiana:
en vez de SI y ENTONCES usamos PILAS y DE UNA.

## Las 15 reglas

**Con una sola condición**

1. Si el jugador responde correctamente, se le suman 100 puntos.
2. Si responde en menos de 5 segundos, gana 500 puntos de bonificación.
3. Si el jugador se queda sin vidas, la partida le sale mal.
4. Si el puntaje pasa de 1000, se le entrega una insignia.
5. Si la partida no está activa, el contador de jugadores vuelve a cero.

**Con condiciones compuestas (Y / O)**

6. Si lleva 3 o más aciertos seguidos y además responde en menos de 10 segundos, su puntaje se multiplica por 2.
7. Si quedan menos de 2 jugadores o se acaba el tiempo, la partida termina.
8. Si el puntaje está entre 800 y 1500, la dificultad sube a nivel 2.
9. Si lleva 5 aciertos seguidos y todavía tiene vidas, o si va de primero en el ranking, su puntaje se multiplica por 3.
10. Si va en la última pregunta, es el primero del ranking y aún tiene vidas, gana la partida.

**Combinando tipos de datos (numérico + booleano)**

11. Si acierta y además lo hace en 3 segundos o menos, la jugada se considera perfecta.
12. Si usó un comodín o le queda una sola vida, las preguntas bajan al nivel más fácil.
13. Si está en modo relámpago y falla la pregunta, pierde una vida.
14. Si falla y traía una racha, la racha se reinicia.
15. Si es la última pregunta, tiene más de 2000 puntos y nunca usó un comodín, se lleva el logro de campeón limpio.

Las mismas 15 reglas escritas en el lenguaje y en su forma simbólica están en
`docs/reglas.txt`.

## Clasificación de las variables

| Variable               | Tipo Tuquiquilulu | Equivalencia Python | Ejemplo           |
|------------------------|--------------------|---------------------|-------------------|
| puntos                 | ENTERO             | int                 | 1500              |
| bonus                  | ENTERO             | int                 | 500               |
| racha                  | ENTERO             | int                 | 3                 |
| vidas                  | ENTERO             | int                 | 2                 |
| numero_pregunta        | ENTERO             | int                 | 7                 |
| total_preguntas        | ENTERO             | int                 | 15                |
| jugadores_conectados   | ENTERO             | int                 | 12                |
| segundos_restantes     | ENTERO             | int                 | 0                 |
| ranking                | ENTERO             | int                 | 1                 |
| dificultad             | ENTERO             | int                 | 2                 |
| multiplicador          | ENTERO             | int                 | 2                 |
| tiempo_respuesta       | DECIMAL            | float               | 3.5               |
| respuesta_correcta     | BOOLEANO           | bool                | True              |
| partida_activa         | BOOLEANO           | bool                | True              |
| es_primero             | BOOLEANO           | bool                | False             |
| uso_comodin            | BOOLEANO           | bool                | False             |
| modo_relampago         | BOOLEANO           | bool                | True              |
| es_final               | BOOLEANO           | bool                | False             |
| insignia               | BOOLEANO           | bool                | True              |
| estado                 | BOOLEANO           | bool                | True              |
| logro                  | TEXTO              | str                 | "campeon limpio"  |
| nombre_jugador         | TEXTO              | str                 | "anggy"           |
| categoria              | TEXTO              | str                 | "deportes"        |

## Diseño del lenguaje (incluye construcciones aún pendientes)

El diseño de Tuquiquilulu incluye declaraciones y reglas condicionales. El parser del 14 de noviembre implementa declaraciones, asignaciones y expresiones; las reglas condicionales se incorporarán después.

### Declaración de variables

Una declaración tiene la siguiente estructura:

```text
PILLE <variable> COMO <tipo> = <valor> LISTO
```

Ejemplos:

```text
PILLE puntos COMO ENTERO = 0 LISTO
PILLE tiempo COMO DECIMAL = 3.5 LISTO
PILLE categoria COMO TEXTO = "Historia" LISTO
PILLE partida_activa COMO BOOLEANO = SISAS LISTO
```

Su sintaxis en BNF es:

```bnf
<declaracion> ::= PILLE <variable> COMO <tipo>
                  <inicializacion> LISTO

<tipo> ::= ENTERO
         | DECIMAL
         | TEXTO
         | BOOLEANO

<inicializacion> ::= = <expresion> | ε
```

El símbolo `ε` significa que la inicialización es opcional. Por ejemplo:

```text
PILLE puntos COMO ENTERO LISTO
```

declara la variable sin asignarle inicialmente un valor.

### Reglas condicionales

Una regla tiene la siguiente estructura:

```text
PILAS <condicion> DE UNA <accion> LISTO
```

Su sintaxis en BNF es:

```bnf
<regla> ::= PILAS <condicion> DE UNA <accion> LISTO

<condicion> ::= <comparacion>
              | <variable_bool>
              | NADA DE <condicion>
              | <condicion> Y ADEMÁS <condicion>
              | <condicion> O DE PRONTO <condicion>
              | ( <condicion> )

<comparacion> ::= <variable> <operador_relacional> <valor>
                | <variable> <operador_relacional> <variable>

<accion> ::= <variable> = <expresion>

<expresion> ::= <valor>
              | <variable>
              | <expresion> <operador_aritmetico> <expresion>

<operador_relacional> ::= >
                        | <
                        | >=
                        | <=
                        | ==
                        | !=

<operador_aritmetico> ::= +
                        | -
                        | *

<variable> ::= identificador en minúsculas con guion bajo

<valor> ::= <numero>
          | <texto>
          | SISAS
          | NONAS
          | MELO
          | PAILA
```

### Diferencia entre `PILLE` y `PILAS`

- `PILLE` comienza la declaración de una variable.
- `PILAS` comienza una regla condicional.
- `COMO` indica el tipo de la variable.
- `DE UNA` separa la condición de la acción.
- `LISTO` termina tanto declaraciones como reglas.

## Convención de escritura

- Las palabras reservadas van siempre en MAYÚSCULA.
- Las variables van en minúscula con guion bajo: `tiempo_respuesta`.
- Como las reservadas son mayúsculas y las variables minúsculas, nunca se pueden confundir.
- `=` asigna un valor y `==` compara. No son lo mismo.
- Toda regla termina en LISTO.
- Los comentarios empiezan con `OJO:`.
- `PILLE` inicia la declaración de una variable.
- `COMO` indica el tipo de una variable.
- `PILAS` inicia una regla condicional.
- Los tipos del lenguaje son `ENTERO`, `DECIMAL`, `TEXTO` y `BOOLEANO`.
- `PILLE` y `PILAS` son palabras diferentes y cumplen funciones diferentes.
- Toda declaración y toda regla terminan con `LISTO`.

## Palabras reservadas

Están documentadas con su significado y su categoría en `docs/palabras_reservadas.md`.

## Archivos del proyecto

| Archivo o carpeta | Descripción |
|---|---|
| `main.py` | Lee un archivo, construye y muestra el árbol; presenta errores léxicos y sintácticos. |
| `tuquiquilulu/__init__.py` | Identifica el paquete del analizador. |
| `tuquiquilulu/lexer.py` | Configuración del vocabulario y función `tokenizar`, encargada del análisis léxico. |
| `tuquiquilulu/tokens.py` | `Token`, `ErrorDeLenguaje`, `ErrorLexico` y `ErrorSintactico`. |
| `tuquiquilulu/parser.py` | Gramática EBNF y parser por descenso recursivo. |
| `tuquiquilulu/arbol.py` | Nodos con tokens y funciones para representar el árbol. |
| `tests/test_parser_arbol.py` | 19 casos de sintaxis, árboles, posiciones y métodos auxiliares. |
| `tests/test_parser.py` | Pruebas de posiciones independientes, consulta sin movimiento y recorrido completo con protección de EOF. |
| `tests/__init__.py` | Identifica el paquete de pruebas. |
| `tests/test_lexer.py` | Casos de prueba con entradas, resultados esperados y comparación con los resultados reales. |
| `examples/programa_valido.txt` | Entrada válida para comprobar la lectura de archivos y el árbol de una declaración. |
| `examples/programa_invalido.txt` | Entrada con un error léxico para comprobar su ubicación y mensaje. |
| `examples/ejemplo.txt` | Programa de demostración del lexer con comentarios, decimales, cadenas, booleanos y operadores. |
| `docs/reglas.txt` | Quince reglas del juego en lenguaje natural, Tuquiquilulu y representación simbólica. |
| `docs/palabras_reservadas.md` | Documentación del vocabulario y los símbolos del lenguaje. |
| `historico/` | Ejercicios y entregables anteriores que conservan la evolución del proyecto. |
| `.gitignore` | Excluye archivos generados por Python y entornos virtuales del control de versiones. |
| `README.md` | Descripción general del proyecto, sintaxis e instrucciones de ejecución. |

La carpeta `historico/` contiene `paso1.py`, `entregable_uno.py`,
`entregable_dos.py` y `parcial.py`. La implementación actual está en
`tuquiquilulu/` y sus pruebas están en `tests/`.

## Entrega del 14 de noviembre: parser y árbol

Requiere Python 3.10 o superior. Ejecutar desde la raíz del repositorio.

```bash
python -m tests.test_lexer
python -m tests.test_parser
python -m tests.test_parser_arbol
python main.py examples/arbol_declaraciones.txt
python main.py examples/arbol_precedencia.txt
python main.py examples/arbol_resta.txt
python main.py examples/error_falta_listo.txt
python main.py examples/error_operadores.txt
python main.py examples/error_parentesis.txt
```

Resultados: 27 pruebas del lexer, 3 del recorrido original y 19 del parser con
árbol. Cada caso muestra entrada, salida esperada, salida real y coincidencia.
Los ejemplos inválidos terminan con código de salida 1: es el comportamiento esperado.

### Gramática implementada en EBNF

```ebnf
programa    ::= instruccion* EOF
instruccion ::= declaracion | asignacion
declaracion ::= "PILLE" IDENTIFICADOR "COMO" TIPO ("=" expresion)? "LISTO"
asignacion  ::= IDENTIFICADOR "=" expresion "LISTO"
expresion   ::= termino (("+" | "-") termino)*
termino     ::= factor (("*" | "/") factor)*
factor      ::= NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR | "(" expresion ")"
```

`*` fuera de comillas indica repetición; `?` indica una parte opcional. El `"*"`
entre comillas es el operador de multiplicación. Se conserva la inicialización
opcional del diseño original: su nodo tiene `valor=None` y aún no se ejecuta.
`TEXTO` y `BOOLEANO` aquí son tipos de tokens literales, no los tokens `TIPO`
que contienen las palabras TEXTO y BOOLEANO en una declaración.

### Qué cambió

- El lexer reconoce `/` después de comprobar los comentarios de bloque.
- Los errores heredan de `ErrorDeLenguaje`; `main.py` captura esa clase base.
- `avanzar()` devuelve el token consumido y mantiene la protección de EOF.
- `esperar()` comprueba tipo y, opcionalmente, texto; consume solo si coincide.
- Cada regla de la gramática tiene un método que devuelve un nodo.
- `termino()` agrupa multiplicación/división antes de suma/resta.
- Los ciclos de `expresion()` y `termino()` agrupan de izquierda a derecha.
- Los paréntesis hacen que `factor()` vuelva a llamar a `expresion()`.
- El árbol conserva los tokens y sus posiciones para las fases posteriores.

### Alcance y archivos de ejemplo

`main.py` muestra el árbol, no calcula resultados. No verifica todavía variables
no declaradas, compatibilidad de tipos ni división por cero. Tampoco reconoce
condicionales, ciclos, operadores lógicos ni menos unario en el parser.
Los booleanos se guardan como nodos; su ejecución será parte de una etapa posterior.

`examples/ejemplo.txt` sigue siendo una muestra histórica del lexer y contiene
instrucciones que este parser aún no admite. Para esta entrega usar los archivos
`arbol_*.txt`. Los archivos `error_*.txt` demuestran errores sintácticos;
`programa_invalido.txt` sigue demostrando un error léxico.

La estructura exigida para la entrega final del 23 de noviembre se adaptará después:
los módulos principales deberán estar en la raíz. Esta etapa conserva el paquete
`tuquiquilulu` para centrarse en el entregable del 14 y mantener las pruebas anteriores.
