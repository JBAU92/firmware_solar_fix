# El método, tal como funcionó

## El orden que resultó ser el bueno

No fue el orden en que se trabajó. Es el orden que se deduce de dónde aparecieron los problemas.

**1 · Congelar lo que se repite, antes de escribir nada.**

Un libro de no ficción práctica está hecho de unas pocas cadenas que vuelven una y otra vez: el
estribillo, los nombres de los marcos, la lista de las siete cosas, el reparto de personajes, la
cuenta que avanza. Si cada capítulo las vuelve a redactar de memoria, derivan. Y derivan poco a
poco, de forma que ningún capítulo suena mal por separado y el libro entero es incoherente.

Lo aprendimos tarde y a base de parches. Se formalizó al preparar la traducción, en
`manuscrito-en/ANCLAJES.en.md`: se traducen primero las cadenas repetidas, fuera de orden, y los
capítulos se escriben *alrededor* de cadenas ya fijadas. **Eso mismo hay que hacerlo en el idioma
original, desde el primer día.**

Lo que hay que congelar antes del primer capítulo:
- el estribillo, palabra por palabra, y su respuesta
- el nombre de cada marco y su metáfora (escalera, puerta, depósito) — y qué palabra queda
  **prohibida** fuera de su marco
- la tabla maestra, si la hay, con su numeración
- las líneas de cuenta, si el libro lleva una cuenta («la tercera de las siete, quedan cuatro»)
- el reparto: nombre, sector, edad, antigüedad, y qué le pasa en cada capítulo

**2 · Escribirlo entero una persona, en una voz.** Esto sí se hizo y fue acertado. La instrucción
original —«lo tienes que escribir tú todo»— es lo que hace que el libro tenga una voz y no cinco.

**3 · Pero no del tirón.** Es la contradicción que hay que sostener: una sola mano, sí; una sola
sentada, no. Los errores más tontos del proyecto salieron de trabajar seguido sin releer. El
emblema es `registro.py`, que construía cuidadosamente cada fila de una tabla y **nunca la
imprimía**. Nadie lo vio hasta ejecutarlo.

**4 · Verificar contra el texto, no contra el recuerdo.** Casi todas las afirmaciones erróneas de
este proyecto —mías— fueron de la forma «el libro dice X» cuando el libro no decía X. Se citó una
frase que se había borrado esa misma sesión. Se afirmó que el libro no usaba la palabra «reglas»
cuando aparece once veces. La regla es simple: **antes de afirmar qué dice el libro, hacer grep.**

---

## Qué se desvió del plan, y por qué estuvo bien

**El acrónimo se cayó.** El dossier construía todo sobre ESCALA (Elige, Sitúate, Construye,
Amplifica, Lidera, Asegura). Al escribir se vio que el acrónimo era andamio del autor: obligaba a
meter capítulos donde tocaba la letra, no donde los pedía el argumento. El libro final no lo
menciona ni una vez y es mejor libro.

**Lección para el libro 2:** un método con nombre bonito se defiende solo mientras no escribes. En
cuanto escribes, o el capítulo lo necesita o sobra. Que el plan no lo decida por ti.

**Las 170 páginas se quedaron en 144.** No por recortar, sino porque los capítulos cerraban antes.
Un capítulo de no ficción práctica termina cuando el lector ya puede hacer algo; estirarlo hasta el
objetivo de palabras es engordar, que además es una de las nueve trampas de `REGLAS.md`.

**Apareció una sección que no estaba en el plan** —el rol dentro del grupo, en el capítulo 11— y
apareció porque la pidió el lector, no el autor. La primera versión era informativa y sonaba a
pegote; se rehízo cuando el lector dijo exactamente eso. **La crítica «esto no se integra» casi
siempre significa «esto no lleva a una acción».**

---

## La lectura en voz alta del propio lector

El hallazgo de proceso más rentable de todo el proyecto: **el autor leyendo el PDF maquetado, por
páginas, y anotando lo que le chirría.** De ahí salieron prácticamente todos los defectos de
deriva del catálogo. Ni el verificador ni ninguna relectura por capítulos los encontró, porque
todos ellos requieren tener dos capítulos lejanos en la cabeza a la vez.

Lo que lo hace funcionar es la maqueta: leer «página 22» y «página 108» en su forma final activa
una memoria distinta que leer archivos markdown sueltos.

**Para el libro 2:** compilar el PDF y leerlo entero, seguido, en cuanto haya borrador completo.
Antes de corregir nada. Con un cuaderno al lado.

---

## Los agentes en paralelo, y cuándo sirven

Se lanzaron tres revisores en paralelo sobre el glosario y los anclajes de la traducción, **antes**
de traducir una sola línea. Encontraron dos errores en archivos que yo daba por congelados y
revisados, una veintena de colisiones de términos, y **un defecto vivo del original en castellano**
que llevaba meses ahí.

La lección no es «usa agentes». Es **cuándo**: sobre material corto y ya cerrado, antes de
construir encima. Revisar 37.000 palabras en paralelo no habría dado nada; revisar dos archivos de
decisiones congeladas dio mucho, porque son los archivos de los que cuelga todo lo demás.

---

## Deuda que no se pagó

**La prueba con lectores.** Cinco lectores de sectores distintos, leyendo el borrador completo y
contestando tres preguntas: dónde te has aburrido, qué no has entendido, qué vas a hacer el lunes.
Estaba en el plan desde el principio. No se hizo. El libro se publicó sin que nadie ajeno lo
hubiera leído entero.

Ningún verificador sustituye eso. El verificador comprueba que el libro es coherente consigo mismo;
sólo un lector comprueba que sirve.

**Para el libro 2: la prueba con lectores es una puerta, no una tarea.** Nada de maquetar la
portada mientras tanto.
