# Catálogo de fallos

Todo lo que salió mal, cómo se detectó y qué lo previene ahora. Ordenado por clase, porque las
clases se repiten y los casos concretos no.

---

# A · Defectos de deriva

**La clase dominante.** Algo que se decidió de una manera y más adelante se volvió a decidir
distinto. Ningún capítulo suena mal por separado; el libro entero es incoherente. Son invisibles
leyendo por capítulos y saltan leyendo seguido.

### A1 · La escalera que se volvió puerta

*Página 22: «Andrés tardó seis meses en descubrir cuál era su puerta»* — pero las cinco rutas del
capítulo 2 son **escaleras**, y las puertas son las tres del capítulo 4. Dos marcos distintos
colisionando en una palabra.

**Causa:** «abrir puertas» es una expresión hecha y se cuela sola.
**Detección:** el autor leyendo el PDF.
**Red:** `METÁFORA` — prohíbe «puerta» en el capítulo 2, «cinco puertas» y «tres escaleras» en todo
el libro.

> Para el libro 2: **cada metáfora estructural se reserva a su marco y su palabra queda prohibida
> fuera de él.** Decidirlo antes de escribir y ponerlo en el verificador el mismo día.

### A2 · La hamburguesa contada dos veces

La misma anécdota, con las mismas palabras, en dos capítulos.
**Detección:** el barrido `ecos()`, pares de párrafos con tres o más 7-gramas en común.
**Red:** `ecos()`. Es la que más defectos de este tipo cazó.

### A3 · El capítulo 14 rediscutiendo el capítulo 3

Un argumento ya cerrado se vuelve a abrir y a resolver, con otras palabras, once capítulos después.
**Detección:** `ecos()` otra vez.

### A4 · La cuenta de las siete cosas rota

El capítulo 10 decía «cinco cosas» y quedaban los capítulos 11 y 12, o sea dos: 5+2=7 ✓. Pero en
otro punto la cuenta no cuadraba. Con siete líneas de recuento, cada una con ordinal, resto y
capítulo, hay veintiuna cifras que tienen que encajar.

**Red:** `RECUENTO` verifica las tres cifras en las siete líneas.

> Para el libro 2: **si el libro lleva una cuenta, la cuenta se escribe entera y de una sentada,
> en su propio archivo, antes que los capítulos.** No se redacta capítulo a capítulo.

### A5 · Pilar, dos años o cuatro

Misma persona, dos antigüedades distintas en páginas 108 y 109.
**Red:** `CRONOLOGÍA`, con la antigüedad declarada de cada personaje.

### A6 · La sala con tres sillas y cuatro ocupantes

El capítulo 10 afirma que en la reunión había tres personas que conocían a Javier; el censo
establecido antes no daba esa cuenta.
**Red:** `SALA` — cruza el aforo declarado con lo que se afirma después.

### A7 · El depósito que se vacía solo

El capítulo 5 afirma que **solo uno** de los cinco depósitos se vacía sin que hagas nada. Pero las
definiciones de los otros cuatro decían que también se vacían con el tiempo. Una exclusiva que el
propio texto contradecía tres párrafos más arriba.

**Detección:** el autor leyendo, y dudando de su propia lectura («o no sé, revísalo, a lo mejor
estoy equivocado» — no lo estaba).
**Red:** `DEPÓSITOS`.

> **Cuidado con las exclusivas.** «El único que…», «la única oportunidad por la que no compite
> nadie», «lo único que…». Cada una es una afirmación fuerte que hay que cotejar con todo lo demás.

### A8 · Los dos estudios que parecían contradecirse

Página 65: un estudio dice que las personas atractivas ganan un 20 % más, y unas líneas antes otro
dice un 5 % por hora. No se contradicen —miden cosas distintas— pero puestos así el lector lee una
contradicción.

**Lección:** dos cifras del mismo fenómeno juntas necesitan **una frase que diga por qué son
distintas**, o una se va.

### A9 · El estribillo que derivó

El capítulo 1 decía «*la opinión de tu jefe*»; el capítulo 4 y el prólogo, «*lo que opine tu
jefe*». Un defecto vivo en el libro impreso.

**Lo grave:** la red lo tapaba. La entrada de `ESTRIBILLOS` se cortaba justo antes del punto donde
el texto divergía, así que las dos versiones coincidían con el patrón.
**Detección:** un agente revisor, comparando el original con los anclajes de la traducción.

### A10 · El narrador que sabía demasiado

Capítulo 14: «*hay una cosa que me dijo [Marta]*». Pero el narrador del libro solo conoce a Marta
por su expediente y por aquella sala. Hablar con ella rompe la posición desde la que está contado
todo.

**Detección:** el autor.
**Mi error al arreglarlo:** sobrepasé el encargo. Añadí al capítulo 1 un párrafo que justificaba
cómo el narrador conoce a Marta. El autor lo rechazó — *«todo lo de antes me parecía una licencia
válida, lo único lo del capítulo 14»* — y tenía razón: el problema era una frase, no la
arquitectura.

> **Arreglar lo que se rompió, no lo que se te ocurra de camino.**

### A11 · La sección que no se integraba

El capítulo 11 incorporó una sección sobre el rol dentro del grupo, con su estudio y sus datos, y
el autor la rechazó: *«se ve un pegote que no se integra y no da información muy útil, parece
informativo»*.

**Diagnóstico correcto:** no le faltaba integración, le faltaba **acción**. En un libro práctico,
una sección que informa y no dice qué hacer el lunes se lee como relleno por bien escrita que esté.

---

# B · Redes que mentían

**Peor que no tener red**, porque dan tranquilidad falsa.

### B1 · Estribillos que no podían coincidir nunca

Varias entradas de `ESTRIBILLOS` tenían más de siete palabras. Como el barrido compara 7-gramas,
esas entradas **no podían filtrar nada jamás**. Llevaban meses ahí sin hacer nada.
**Arreglo:** `revisa_estribillos()`, que comprueba que cada entrada siga apareciendo dos veces.

### B2 · Estribillos que tapaban n-gramas sueltos

La primera versión enmascaraba n-gramas individuales, no el tramo completo del estribillo. Un
estribillo largo seguía generando ecos solapados y yo los iba parcheando de uno en uno.
**Arreglo:** enmascarar el tramo entero (`_gramas` con el vector `fijo`).

### B3 · La regex que contaba filas vacías como tablas

`check_epub.py` daba «9 tablas en el manuscrito y 5 en el EPUB». El EPUB estaba bien: mi expresión
`^\s*\|[\s:\-|]+\|\s*$` también coincidía con `| | | | |`, las cuatro filas vacías del formulario
del capítulo 5.
**Arreglo:** exigir un guion en el separador. Aplicado también al generador, por si acaso.

### B4 · La tabla que se construía y no se imprimía

`registro.py` montaba cuidadosamente cada fila y no la sacaba por pantalla. Faltaba el `print`.
**Causa:** escribirlo del tirón sin ejecutarlo.

---

# C · Artefactos de medición

**Tres veces perseguí un problema que no existía.** Es la clase que más tiempo costó y la más fácil
de repetir.

### C1 · Los píxeles de la portada

Medir regiones de la cubierta por color dio, en distintos intentos: una costura azul marino de un
píxel tomada por un borde, texto blanco tomado por el recuadro del código de barras, y el fondo
crema tomado por el texto de cabecera.
**Lo que funcionó:** dejar de medir y mirar un recorte ampliado.

### C2 · El recorte de la cuadrícula A+

Se sospechaba que la palabra «MUCHO» quedaba cortada por el borde de una celda. Las medidas no
concluían. Un recorte ampliado lado a lado lo resolvió en diez segundos.

### C3 · Chromium maqueta a 500 px aunque le pidas 390

**El más caro de todos.** Las tablas del EPUB aparecían cortadas por la derecha en las capturas: la
cuadrícula del capítulo 1 perdía la columna donde está Marta, el inventario perdía la del total.
Pasé por tres «arreglos» —anchos calculados, `colgroup`, `box-sizing`— y ninguno cambiaba nada.

La causa: **`chrome --headless --window-size=390` maqueta la página a 500 px y recorta la captura a
390.** Las tablas nunca se habían salido.

**Cómo se resolvió:** haciendo que la propia página escribiera su anchura **dentro** de la captura.
`VIEWPORT=500` impreso sobre una imagen de 390 px de ancho. Sin dos fuentes que pudieran discrepar.

> **La regla que sale de las tres:** cuando una medida y una impresión discrepan, sospecha de la
> medida antes que del objeto. Y si vas a medir, **que la medida y lo medido salgan del mismo
> sitio**, no de dos invocaciones distintas.

De todo aquello se quedó una cosa que sí valía: el reparto de anchos por columna calculado según el
contenido. Sin él las columnas salen iguales y la columna del número ocupa lo mismo que la de la
frase larga.

---

# D · Afirmaciones mías que no eran ciertas

Las anoto porque el patrón se repite y es evitable: **afirmar sobre el texto desde la memoria en
vez de desde el texto.**

| Afirmé | La realidad |
|---|---|
| Que una frase estaba en el capítulo 14 | La había borrado yo esa misma sesión; la única instancia real estaba en el 9 |
| Que el glosario y los anclajes coincidían | El glosario prohibía *track* y los anclajes llamaban «Expert track» a una escalera |
| Que la sección §2 era idéntica en los dos idiomas | El castellano había derivado (A9) |
| Que el libro no usaba la palabra «reglas» | Aparece **6** veces en los capítulos, una de ellas en el 1: *«no puedes decidir no jugar a un juego cuyas reglas desconoces»* |
| Que el verificador tenía veinticinco comprobaciones | Tiene 21 etiquetas y 2 barridos. No las había contado |
| Que Amazon rechaza el texto incrustado en las imágenes A+ | Falso. Es práctica normal en la mayoría de las fichas |
| Nombres de subcategorías de KDP | No existían en el mercado del autor |

**Remedio único y suficiente:** `grep` antes de afirmar. Cuesta tres segundos.

Y una nota que vale por todo el apartado: al escribir esta tabla puse «once veces» de memoria. Son seis. El fallo se cometió **dentro del apartado que lo describe**, y solo salió porque antes de subir el archivo se comprobó cada cifra. Es exactamente por eso que la comprobación no puede ser un propósito: tiene que ser un paso del procedimiento.

---

# E · Dónde el autor tenía razón y yo no

Vale la pena dejarlo escrito, porque las tres veces el argumento era de mercado y el mío de
diseño.

**El «7» de la portada.** Lo quité por limpieza. *«Creo que quitar el 7 de la portada puede no ser
la mejor elección»* — cierto: el número es lo que hace que un comprador pare.

**La palabra «ascensos» en la cejilla.** La quité y el autor la reclamó: *«me gusta lo de los
ascensos porque da más impacto»*. Es la palabra que el comprador necesita para saber de qué va el
libro en medio segundo.

**El acrónimo.** El dossier lo defendía; el autor dejó de usarlo al escribir. Acertó.

> En decisiones de portada y de mercado, la intuición de quien va a vender el libro pesa más que
> el criterio de composición. En decisiones de coherencia interna, al revés.
