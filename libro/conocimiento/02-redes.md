# Las redes

Tres programas y dos prácticas. Los programas están en `libro/tools/` y se ejecutan; las prácticas
hay que acordarse de hacerlas.

---

## `check_manuscrito.py` — 21 comprobaciones y 2 barridos

Devuelve 1 si hay algún fallo. Se ejecutaba después de cada tanda de cambios.

Las nueve trampas originales están en `manuscrito/REGLAS.md`; el verificador nació para
comprobarlas y **fue creciendo con cada defecto que se nos escapó**. Ese es el patrón: cada vez que
un lector encuentra algo, no basta con arreglarlo — hay que añadir la comprobación que lo habría
cazado.

### Las 21 etiquetas

| Etiqueta | Qué caza |
|---|---|
| `CIFRA FALSA` | Cifras que suenan a dato y no tienen fuente |
| `CIFRA EN ESCENA` | Datos estadísticos metidos dentro de una escena narrada |
| `LISTA NEGRA` | Citas y estudios contaminados (la lista está en el dossier 04) |
| `MULETILLAS` | Densidad de muletillas por capítulo |
| `SERMÓN` | Párrafos que predican en vez de mostrar |
| `HILO` | Que Marta y Javier aparezcan en los capítulos con revelación |
| `EXTENSIÓN` | Objetivo de palabras por capítulo, con objetivos propios para prólogo, epílogo y fuentes |
| `CADENCIA` | La cadencia de máquina: frases todas del mismo largo |
| `GANCHO` | Que el capítulo cierre abriendo el siguiente |
| `RAYA` | Uso de la raya y las comillas españolas |
| `METÁFORA` | **Colisión de marcos.** Que no se llame «puerta» a una escalera del cap. 2 ni «escalera» a una puerta del cap. 4 |
| `TRÍADAS` | Que los tres criterios (cap. 1) y las tres puertas (cap. 4) no se glosen con los términos del otro |
| `DEPÓSITOS` | Que la exclusiva del depósito que se vacía solo no contradiga las definiciones de los otros cuatro |
| `RECUENTO` | La cuenta de las siete cosas: ordinal, resto y capítulo, en las siete líneas |
| `ARITMÉTICA` | Que los números del texto cuadren entre sí |
| `CRONOLOGÍA` | Que la antigüedad de cada personaje sea la misma en todos los capítulos |
| `SALA` | El censo de la sala: cuánta gente hay y cuánta se afirma después que había |
| `COTEJO` | Referencias cruzadas a capítulos que existen |
| `CRUCE` | Remisiones internas coherentes |
| `COLUMNA/FILA` | Integridad de las tablas |
| `FRANQUEZA` | Fórmulas de falsa franqueza repetidas («no te voy a engañar», «no te voy a vender la moto») |

### Los 2 barridos de libro completo

**`ecos()`** — parte el libro en párrafos y busca pares que compartan tres o más 7-gramas. Es lo que
cazó la hamburguesa contada dos veces y el capítulo 14 rediscutiendo el 3. Excluye la bibliografía,
que repite títulos por oficio.

**`revisa_estribillos()`** — no comprueba el libro: **comprueba la red.** Verifica que cada
estribillo de la lista siga apareciendo al menos dos veces en el texto. Si un estribillo deja de
aparecer, es que el texto cambió y esa entrada ya no filtra nada — pero seguía ahí, dando la
sensación de estar protegiendo algo.

---

## `registro.py` — la huella de registro

Mide tres proxies por capítulo: marcas de segunda persona por mil palabras, imperativos por mil
palabras y longitud media de frase. No sirve para puntuar prosa; sirve para ver la curva del libro
y detectar el capítulo que se sale.

**El dato que dejó:** el original mantiene **entre 15 y 18 palabras por frase en los catorce
capítulos**. Es una constante sorprendentemente firme y es lo que hace que el libro suene a una
sola persona.

Tiene modo `--comparar` para poner al lado la huella de una traducción. Para el inglés el objetivo
es **13–16 palabras**, porque el castellano corre un 15–25 % más largo.

---

## `check_epub.py` — la red del ebook

Comprueba el envoltorio (mimetype primero y sin comprimir, container, manifiesto en las dos
direcciones, un único `nav`, spine, guide con su posición de inicio de lectura), que cada documento
sea XML válido y que no haya enlaces rotos.

Y lo que de verdad importa: **compara palabras, tablas y capítulos contra el manuscrito**. Es lo
único que demuestra que la conversión no se comió nada.

---

## Práctica 1 · Mirar, no deducir del marcado

Varias veces di por bueno un resultado leyendo el código o el HTML en vez de mirar la salida. Casi
siempre estaba mal.

**Renderiza y mira.** El EPUB se compiló, se extrajo, se metió en un contenedor del ancho de un
móvil y se hizo una captura. Ahí se vio que las tablas... estaban bien, y que lo roto era mi manera
de medir (ver `03-fallos.md`). Pero solo se supo mirando.

---

## Práctica 2 · Verificar la copia de marketing contra el manuscrito

La descripción de Amazon y el contenido A+ los redacta uno de memoria, y la memoria inventa. Al
cotejar cada afirmación con el texto aparecieron **siete errores** en una sola tanda: «dos cafés al
mes» cuando el libro dice *al año* en tres sitios, «todo lo que haces» cuando el capítulo 6 tiene
una sección titulada *No todo el trabajo cuenta igual*, una frase entrecomillada que no existía en
el libro, y un titular que invertía la tesis del capítulo 7.

**Ninguna frase de marketing sale sin su grep.**

---

## La regla que gobierna todas las redes

**Una red que deja de filtrar en silencio es peor que no tener red**, porque da tranquilidad falsa.
Pasó dos veces con los estribillos: entradas de más de siete palabras que nunca podían coincidir
con un 7-grama, y una entrada que se cortaba justo antes del punto donde el texto divergía, tapando
un defecto vivo.

De ahí `revisa_estribillos()`. **Toda red con una lista de patrones necesita otra red que compruebe
que los patrones siguen encontrando algo.**
