# Palabras reservadas

**Grupo 1 - Los Más Chimbas**

Nuestro lenguaje se llama Tuquiquilulu y usa jerga colombiana en vez de las
palabras clave de siempre (SI, ENTONCES, Y, O). Cada palabra tiene un símbolo
que significa lo mismo, así que una regla se puede escribir de las dos formas.

Las palabras reservadas van en MAYÚSCULA y las variables en minúscula con guion
bajo, para que nunca se confundan entre ellas.

---

## Palabras clave

**TUQUIQUILULU** — abre el programa.

**FIN** — cierra el programa.

**PILLE** — inicia la declaración de una variable.

**COMO** — indica el tipo de una variable dentro de una declaración.

Una declaración utiliza la siguiente estructura:

```text
PILLE <variable> COMO <tipo> = <valor> LISTO

**PILAS** (símbolo `:-`) — anuncia la condición. Equivale a "si se cumple que".

**DE UNA** (símbolo `:-`) — anuncia la acción. Equivale a "entonces".

**QUIUBO** (símbolo `?`) — consulta el valor de un dato.

PILAS y DE UNA siempre van en la misma regla, con la condición en el medio.

---

## Operadores lógicos

**Y ADEMÁS** (símbolo `,`) — se tienen que cumplir las dos condiciones.

**O DE PRONTO** (símbolo `;`) — basta con que se cumpla una de las dos.

**NADA DE** (símbolo `!`) — niega la condición que va después.

---

## Operadores relacionales

Comparan dos valores y el resultado es verdadero o falso.

`>` mayor que
`<` menor que
`>=` mayor o igual que
`<=` menor o igual que
`==` igual a
`!=` distinto de

Los cuatro primeros solo funcionan con números. `==` y `!=` también sirven para
booleanos y para texto.

---

## Operador de asignación

`=` le da un valor a una variable.

Ojo con no confundirlo: `=` asigna un valor y `==` compara dos valores.

---

## Literales

**SISAS** (símbolo `1`) — verdadero.

**NONAS** (símbolo `0`) — falso.

**MELO** (símbolo `1`) — al jugador le fue bien.

**PAILA** (símbolo `0`) — al jugador le fue mal.

MELO y PAILA valen lo mismo que SISAS y NONAS. Los usamos cuando el resultado
dice cómo le fue al jugador en la partida.

---

## Delimitadores

**LISTO** (símbolo `.`) — termina la regla.

**OJO:** (símbolo `%`) — comentario, se ignora hasta el final de la línea.

`( )` agrupan condiciones para cambiar el orden en que se evalúan.

`" "` encierran un texto.

---

## Cómo se arma una regla

Toda regla tiene esta forma:

```
PILAS <condición> DE UNA <acción> LISTO
```

Por ejemplo, "si el jugador acierta gana 100 puntos" queda así:

```
PILAS respuesta_correcta DE UNA puntos = puntos + 100 LISTO
```

Y esa misma regla escrita con símbolos:

```
puntos = puntos + 100 :- respuesta_correcta.
```

En la versión con símbolos la acción va primero y la condición después del `:-`,
igual que en Prolog.

Una regla con condición compuesta se ve así:

```
PILAS respuesta_correcta Y ADEMÁS tiempo_respuesta <= 3 DE UNA estado = MELO LISTO
```

---

## Lo que no son palabras reservadas

Las variables se escriben en minúscula con guion bajo: `tiempo_respuesta`.

Los números enteros van sin punto (`1500`) y los decimales con punto (`3.5`).

Los textos van entre comillas: `"campeon limpio"`.

---

## De dónde salen las palabras

Casi todas son colombianismos de todos los días: pilas, de una, quiubo, sisas,
nonas, melo, paila y listo.

TUQUIQUILULU no es jerga real, es una palabra que nos inventamos nosotros para
ponerle nombre al lenguaje.
