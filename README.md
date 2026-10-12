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
`reglas.txt`.

## Clasificación de las variables

| Variable             | Tipo Java | Ejemplo          |
|----------------------|-----------|------------------|
| puntos               | int       | 1500             |
| bonus                | int       | 500              |
| racha                | int       | 3                |
| vidas                | int       | 2                |
| numero_pregunta      | int       | 7                |
| total_preguntas      | int       | 15               |
| jugadores_conectados | int       | 12               |
| segundos_restantes   | int       | 0                |
| ranking              | int       | 1                |
| dificultad           | int       | 2                |
| multiplicador        | int       | 2                |
| tiempo_respuesta     | double    | 3.5              |
| respuesta_correcta   | boolean   | true             |
| partida_activa       | boolean   | true             |
| es_primero           | boolean   | false            |
| uso_comodin          | boolean   | false            |
| modo_relampago       | boolean   | true             |
| es_final             | boolean   | false            |
| insignia             | boolean   | true             |
| estado               | boolean   | true             |
| logro                | String    | "campeon limpio" |
| nombre_jugador       | String    | "anggy"          |
| categoria            | String    | "deportes"       |

## Sintaxis del lenguaje

## Sintaxis del lenguaje

Tuquiquilulu permite declarar variables y escribir reglas condicionales.

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

Están documentadas con su significado y su categoría en `palabras_reservadas.md`.

## Archivos del proyecto

```text
README.md
    Descripción general, tipos y sintaxis de Tuquiquilulu.

reglas.txt
    Quince reglas del juego en lenguaje natural, Tuquiquilulu
    y su representación simbólica.

palabras_reservadas.md
    Palabras reservadas, tipos, operadores y delimitadores.

paso1.py
    Ejercicios introductorios de Python.

entregable_uno.py
    Evolución del lexer durante las tareas 1, 2 y 3.

entregable_dos.py
    Evolución del lexer desde la tarea 4 hasta la tarea 6.3.