# 1. Tuquiquilulu — Lenguajes Formales

Proyecto de Lenguajes Formales — EAM

Grupo 1: Los Más Chimbas

## Integrantes

- Juan David Rodríguez
- Diego Andrés Osorio
- Valentina Marín Flórez
- Anggy Dahiana Ruiz

Tuquiquilulu es un lenguaje educativo implementado en Python, con
vocabulario inspirado en expresiones colombianas. El proyecto evolucionó
desde la tokenización hasta un intérprete con variables, operaciones,
condicionales, ciclos, ámbitos y lectura de datos.

# 2. Cómo ejecutar

## Requisitos

- Python 3.10 o superior.
- Archivos de entrada guardados en UTF-8.
- No requiere instalar dependencias externas.

Ejecutar desde la raíz del repositorio:

```bash
python main.py programa.txt
```

`programa.txt` debe contener instrucciones de Tuquiquilulu.

El procesamiento sigue estas etapas:

1. El lexer transforma el texto en tokens con línea y columna.
2. El parser comprueba la sintaxis y construye el árbol.
3. El intérprete recorre el árbol, comprueba las reglas semánticas
   durante la ejecución y ejecuta las instrucciones.

Si ocurre un error del lenguaje, se muestra su mensaje, posición,
línea de código y un indicador `^`. El programa termina con código 1.
Una ejecución correcta termina con código 0.

La validación semántica ocurre durante la ejecución: una salida
impresa antes de un error se conserva.

## Los tres programas de muestra

### Tabla de multiplicar del 3

```bash
python main.py examples/tabla_del_3.txt
```

Salida:

```text
3
6
9
12
15
```

### Factorial de 5

```bash
python main.py examples/factorial_de_5.txt
```

Salida:

```text
120
```

### Promedio de tres notas

```bash
python main.py examples/promedio_notas.txt
```

Salida:

```text
4.0
aprueba
```

## Pruebas

```bash
python -m tests.test_lexer
python -m tests.test_parser
python -m tests.test_parser_arbol
python -m tests.test_comparaciones
python -m tests.test_interprete
python -m tests.test_ejecucion
python -m tests.test_entrega_final
```

Las pruebas presentan la entrada, el resultado esperado, el resultado
real y si coinciden. Las pruebas de lectura simulan el teclado para
poder repetirse automáticamente.

## Archivos principales

| Archivo | Responsabilidad |
|---|---|
| `tokens.py` | Define los tokens y los errores del lenguaje. |
| `lexer.py` | Reconoce palabras, literales, operadores y símbolos; ignora comentarios. |
| `arbol.py` | Define los nodos y permite representar el árbol como texto. |
| `parser.py` | Comprueba la sintaxis y construye el árbol respetando la precedencia. |
| `interprete.py` | Ejecuta instrucciones, evalúa expresiones y administra entornos. |
| `main.py` | Lee el archivo, conecta las etapas y presenta errores. |
| `tests/` | Pruebas de las distintas etapas. |
| `examples/` | Programas válidos y ejemplos de errores. |
| `historico/` | Ejercicios de etapas anteriores. |
| `docs/` | Documentación de la evolución del proyecto. |

La especificación de la versión final es este README. Los documentos
históricos pueden contener sintaxis o alcances anteriores.

# 3. Ficha del lenguaje

## Nombre e identidad

El nombre Tuquiquilulu identifica nuestra propuesta de un lenguaje
con un estilo cercano y expresiones colombianas. Su vocabulario,
como `PILLE`, `PILAS`, `QUIUBO` y `LISTO`, refleja esa identidad.

La idea inicial del proyecto estaba relacionada con reglas para un
juego de preguntas. El intérprete final permite escribir programas
pequeños de cálculo y control de flujo.

## Equivalencias con Java

| Concepto | Java | Tuquiquilulu |
|---|---|---|
| Tipos | `int`, `double`, `String`, `boolean` | `ENTERO`, `DECIMAL`, `TEXTO`, `BOOLEANO` |
| Declaración | `int x = 5;` | `PILLE x COMO ENTERO = 5 LISTO` |
| Asignación | `x = 8;` | `x = 8 LISTO` |
| Fin de instrucción | `;` | `LISTO` |
| Salida | `System.out.println(x);` | `QUIUBO(x) LISTO` |
| Condicional | `if (c) { ... } else { ... }` | `PILAS (c) DE UNA { ... } O SI NO { ... } LISTO` |
| Ciclo | `while (c) { ... }` | `MIENTRAS (c) DE UNA { ... } LISTO` |
| Comentario de línea | `// comentario` | `OJO: comentario` |
| Comentario de bloque | `/* comentario */` | `/* comentario */` |
| Conjunción | `a && b` | `a Y ADEMÁS b` |
| Disyunción | `a || b` | `a O DE PRONTO b` |
| Negación | `!a` | `NADA DE a` |

En los ejemplos, `c` representa una condición y `...` representa
instrucciones; no son elementos que deban copiarse literalmente.

## Decisión de diseño

Elegimos palabras y expresiones cercanas al habla colombiana para
identificar las instrucciones. Usamos `LISTO` como terminador explícito.

También exigimos booleanos en condiciones y operaciones lógicas:
un número como `1` no se interpreta automáticamente como verdadero.

## Ejemplo

```text
PILLE puntos COMO ENTERO = 7 LISTO

PILAS (puntos >= 1 Y ADEMÁS puntos <= 10) DE UNA {
    QUIUBO("En rango") LISTO
} O SI NO {
    QUIUBO("Fuera de rango") LISTO
} LISTO
```

# 4. Gramática final en EBNF

Convenciones:

- Las comillas indican texto literal.
- `|` separa alternativas.
- `*` fuera de comillas significa cero o más repeticiones.
- `?` indica una parte opcional.
- `EOF` es el token de fin de archivo; no se escribe en el programa.

```ebnf
programa    ::= instruccion* EOF

instruccion ::= declaracion | asignacion | salida
              | condicional | mientras | lectura

declaracion ::= "PILLE" IDENTIFICADOR "COMO" TIPO
                ("=" expresion)? "LISTO"

asignacion  ::= IDENTIFICADOR "=" expresion "LISTO"

salida      ::= "QUIUBO" "(" expresion ")" "LISTO"

lectura     ::= "LEA" "(" IDENTIFICADOR ")" "LISTO"

bloque      ::= "{" instruccion* "}"

condicional ::= "PILAS" "(" condicion ")" "DE" "UNA" bloque
                ("O" "SI" "NO" bloque)? "LISTO"

mientras    ::= "MIENTRAS" "(" condicion ")" "DE" "UNA"
                bloque "LISTO"

condicion   ::= expresion
expresion   ::= logica_o

logica_o    ::= logica_y ("O" "DE" "PRONTO" logica_y)*
logica_y    ::= logica_no ("Y" "ADEMÁS" logica_no)*
logica_no   ::= "NADA" "DE" logica_no | comparacion

comparacion ::= aritmetica (COMPARADOR aritmetica)?
aritmetica  ::= termino (("+" | "-") termino)*
termino     ::= unario (("*" | "/") unario)*
unario      ::= "-" unario | factor

factor      ::= NUMERO | TEXTO | BOOLEANO | IDENTIFICADOR
              | "(" expresion ")"

TIPO        ::= "ENTERO" | "DECIMAL" | "TEXTO" | "BOOLEANO"
COMPARADOR  ::= "==" | "!=" | "<" | ">" | "<=" | ">="
BOOLEANO    ::= "SISAS" | "NONAS" | "MELO" | "PAILA"
              | "true" | "false"
```

`TEXTO` y `BOOLEANO` en `factor` representan tokens de valores
literales. Las palabras de los tipos en las declaraciones se
clasifican como `TIPO`.

## Reglas léxicas

- Se distinguen mayúsculas y minúsculas.
- Los identificadores comienzan con una letra y continúan con
  letras, dígitos o guion bajo. No pueden ser palabras reservadas,
  nombres de tipos ni literales booleanos.
- El lexer usa `isalpha()` e `isalnum()`, por lo que admite letras
  Unicode, incluidas las letras con tilde.
- Los números se escriben con dígitos; los decimales requieren
  dígitos antes y después del punto, como `3.5`.
- El signo negativo es un operador separado del token numérico.
- Los textos usan comillas dobles y ocupan una sola línea.
  No se implementan secuencias de escape.
- Los comentarios `OJO:` terminan al finalizar la línea.
- Los comentarios `/* ... */` pueden ocupar varias líneas y
  no admiten anidamiento.
- Los espacios, tabulaciones y comentarios no producen tokens.
- Las expresiones de varias palabras se reconocen como tokens
  separados y el parser comprueba su orden.
- Se conserva el reconocimiento léxico de `if`, `else`, `while`,
  coma, punto y punto y coma de ejercicios anteriores. Eso no
  implica que el parser acepte instrucciones Java ni `;` como
  terminador: la sintaxis ejecutable es la descrita arriba.

## Precedencia y agrupación

De menor a mayor prioridad:

1. `O DE PRONTO`.
2. `Y ADEMÁS`.
3. `NADA DE`.
4. Comparaciones.
5. Suma y resta.
6. Multiplicación y división.
7. Menos unario.

Los paréntesis permiten cambiar la agrupación. La suma, resta,
multiplicación y división se agrupan de izquierda a derecha.

No se admiten comparaciones encadenadas como `1 < x < 10`.
Se escribe `1 < x Y ADEMÁS x < 10`.

# 5. Reglas de operaciones entre tipos

## Variables y ámbitos

- Una variable debe declararse antes de usarse.
- La inicialización es opcional, pero leer una variable sin valor
  produce un error.
- No se permite declarar dos veces el mismo nombre en un ámbito.
- Cada bloque crea un entorno local conectado con su entorno padre.
- Una declaración local puede ocultar una variable exterior del
  mismo nombre.
- La búsqueda y la asignación utilizan la variable más cercana,
  recorriendo los entornos hacia afuera.
- Al terminar un bloque se recupera el entorno anterior.
- Cada vuelta de un ciclo crea un nuevo entorno para su cuerpo.

## Tipos y operaciones

| Operación | Regla |
|---|---|
| Guardar en `ENTERO` | Solo admite valores enteros. |
| Guardar en `DECIMAL` | Admite enteros y decimales; guarda el valor como decimal. |
| Guardar en `TEXTO` | Solo admite texto. |
| Guardar en `BOOLEANO` | Solo admite booleanos. |
| `+`, `-`, `*` entre números | Calculan el resultado; si interviene un decimal, el resultado es decimal. |
| `/` entre enteros | División truncada hacia cero: `7 / 2` da `3`; `-7 / 2` da `-3`. |
| `/` con algún decimal | División decimal: `7 / 2.0` da `3.5`. |
| División entre cero | Produce un error semántico. |
| `+` entre textos | Concatena: `"ho" + "la"` da `"hola"`. |
| Texto con número | No se convierte automáticamente; la operación produce un error. |
| Menos unario | Solo admite números. |
| `<`, `>`, `<=`, `>=` | Solo comparan números. |
| `==`, `!=` | Admiten números entre sí, textos entre sí y booleanos entre sí. |
| Operadores lógicos | Exigen valores booleanos en los operandos evaluados. |
| Condiciones | Deben producir un booleano. |

Los booleanos no se consideran enteros en las operaciones del lenguaje.

`Y ADEMÁS` y `O DE PRONTO` usan cortocircuito: no evalúan el
operando derecho cuando el izquierdo ya determina el resultado.

`MIENTRAS` vuelve a evaluar su condición antes de cada vuelta.
Como protección, cada ejecución de un ciclo permite hasta 100.000
iteraciones; si necesita otra vuelta, produce un error semántico.

# 6. Requerimientos electivos escogidos

## Electivo 1: tipo booleano

Los valores verdaderos son `SISAS`, `MELO` y `true`.
Los falsos son `NONAS`, `PAILA` y `false`.

Se pueden guardar resultados de comparaciones y usar variables
booleanas directamente en condiciones:

```text
PILLE puntos COMO ENTERO = 7 LISTO
PILLE listo COMO BOOLEANO = puntos > 3 LISTO

PILAS (listo) DE UNA {
    QUIUBO("Listo para continuar") LISTO
} LISTO
```

Al imprimir un booleano, la salida se normaliza a `SISAS` o `NONAS`.

Ejemplo:

```bash
python main.py examples/logicos.txt
```

## Electivo 2: lectura de datos

`LEA(variable) LISTO` pide un dato y lo convierte al tipo declarado.
La variable debe existir antes de la lectura.

```text
PILLE edad COMO ENTERO LISTO
LEA(edad) LISTO
QUIUBO(edad + 1) LISTO
```

| Tipo | Entrada |
|---|---|
| `ENTERO` | Dígitos con signo negativo opcional, como `20` o `-5`. |
| `DECIMAL` | Un entero o un decimal con punto, como `7` o `3.5`; admite signo negativo. |
| `TEXTO` | Se conserva el contenido ingresado, sin exigir comillas. |
| `BOOLEANO` | Uno de los seis literales booleanos admitidos. |

En números y booleanos se ignoran espacios externos.
En texto se conservan. Los decimales ingresados deben ser finitos.

Si la conversión falla, se informa un error semántico en la posición
de la variable. Si se agota la entrada, también se informa un error.
El valor anterior no se reemplaza cuando la lectura falla.

Ejemplos:

```bash
python main.py examples/lectura_basica.txt
python main.py examples/error_lectura.txt
```