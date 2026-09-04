# Red de traducción

Notas de quien lo escribió, para quien lo traduzca. No es una guía de estilo: es la lista de
sitios donde una traducción literal rompe algo, con el sitio exacto y qué hay que decidir en su
lugar.

Regla general: **este libro no describe España, describe un mecanismo.** Todo lo que sea el
mecanismo se traduce. Todo lo que sea el envoltorio español se sustituye por el envoltorio del país
de destino. La parte difícil es que las dos cosas están mezcladas en la misma frase muchas veces.

---

## 1 · Lo que no puede cambiar

Si algo de esto se mueve, el libro deja de sostenerse. Se comprueba con `check_manuscrito.py`
antes y después.

**La aritmética del armazón.** Siete cosas encima de la mesa (caps. 6–12, una por capítulo, con el
recuento al cierre: «tercera encima de la mesa… quedan cuatro»). Cinco escaleras (cap. 2). Tres
puertas (cap. 4). Tres criterios (cap. 1). Cinco depósitos (cap. 5). Ocho señales (cap. 13). Cinco
rutas, cinco movimientos, tres defensas, tres respuestas, tres noes. Ningún número de estos es
decorativo y todos se citan otra vez en capítulos posteriores.

**Las referencias cruzadas.** Cuarenta y siete referencias a otros capítulos por su número. La
comprobación `CRUCE` las verifica.

**El aforo de la sala.** Cinco personas en el capítulo 1; el capítulo 10 sienta a tres «además de
su jefe». Comprobación `SALA`.

**Las cronologías.** Los cuatro años de espera de Pilar (tres menciones), los catorce meses de
Javier (dos), los once años de Ramón, los seis meses de Andrés. Comprobación `CRONOLOGÍA`.

**Las cifras de los estudios**, con sus reservas. El nueve y el cinco por ciento de Hamermesh y
Biddle, el veinte de Wong y Penner —y la frase que explica que **no son comparables**, que no se
puede perder—. Comprobación `COTEJO`.

---

## 2 · Los dos armazones que se pueden fundir en la traducción

Este es el riesgo más grave y ya se materializó una vez **en el original**.

- El capítulo 2 tiene **cinco escaleras** = las rutas de carrera.
- El capítulo 4 tiene **tres puertas** = las condiciones del ascenso.

En castellano el cuerpo del capítulo 2 llegó a decir «hay cinco puertas» mientras el título decía
«cinco escaleras», y como el capítulo 4 usa *puerta* para otra cosa, el lector tenía dos armazones
con el mismo nombre y distinto número. Está arreglado y vigilado por la comprobación `METÁFORA`.

**En traducción el peligro se multiplica**, porque muchas lenguas tienen menos palabras disponibles:
en inglés *door / doorway / gateway* y *ladder / staircase / stairway* obligan a elegir, y
*path*, *route* y *track* se cuelan solos. **Antes de traducir una línea hay que fijar un
diccionario de una sola entrada por concepto**, y no permitir sinónimos «para no repetir»:

| concepto | castellano | regla |
|---|---|---|
| las cinco rutas de carrera | **escalera** | un solo término, nunca el de las puertas |
| las tres condiciones del ascenso | **puerta** | un solo término, nunca el de las escaleras |
| donde se decide sobre ti | **la mesa** | es el estribillo del libro, aparece en los 14 capítulos |
| lo que se acumula y se gasta | **depósito** | cap. 5, retomado en el 10 y en las fuentes |
| la pantalla de la reunión | **cuadrícula** | cap. 1, la rejilla de 3 × 3 |
| subir un nivel | **peldaño** | coherente con *escalera* |

Y el estribillo, que va literal en los capítulos 1 y 4 y no puede variar entre los dos:

> *Si mañana se sentaran a hablar de ti, ¿qué tendrían encima de esa mesa aparte de tus números y
> lo que opine tu jefe?*

---

## 3 · Lo que hay que volver a decidir, no traducir

### 3.1 · La única frase que dice «en España»

- `01:206` — *«…cosa que en España nos da un pudor…»*. Se sustituye por la observación equivalente
  del país de destino, **o se quita**. No se traduce como «in Spain», porque el libro deja de
  hablarle al lector y pasa a hablarle de otros.

### 3.2 · El reloj y la jornada

El libro asume una oficina española de ocho a cinco y una cultura de quedarse tarde. Ya se corrigió
una vez en el original: «se iba a las seis y media» se leía como *tarde* y hubo que cambiarlo por
«se iba a su hora». En traducción cada referencia horaria hay que recalcularla, no convertirla:

- `01:49` — «el que se iba **a su hora** mientras ella se quedaba cerrando el mes». Funciona en
  cualquier país donde quedarse tarde sea la norma. **En Alemania o los Países Bajos irse a la hora
  es lo normal y la frase pierde todo el sentido**: allí la señal de compromiso es otra.
- `14:3` — «Le ofrecieron el puesto un jueves **a las seis de la tarde**». Comprobar que a esa hora
  todavía hay gente en la oficina en el país de destino.
- `07:7` — «un pasajero enfadado **a las tres de la mañana**». Aeropuerto, funciona en todas partes.
- `03:116` — «no hay que **madrugar** más, no hay que **sacrificar los sábados**». El sábado como
  día de descanso no es universal.
- Turnos de mañana / tarde / noche (`12:16`, `13:7`, `13:67`, `14:104`) y **campaña** de Navidad
  (`07:127`, `09:160`): el pico comercial anual cambia de fecha y de nombre según el país.

### 3.3 · Los tiempos de la promoción

Todo el calendario del libro es el de una empresa española mediana:

- «**Ocurre una vez al año**» (`01:5`) — la revisión anual. En muchas multinacionales es semestral
  o continua; en empresas pequeñas no existe como reunión formal.
- «**la revisión de mayo**», «**en qué fecha lo revisamos**» (cap. 12) — el ciclo presupuestario.
- «**catorce meses antes de que la vacante existiera**» (`12:213`) — depende de que las vacantes se
  vean venir, que es cierto en estructuras estables y falso en empresas que crecen a saltos.
- «**tres meses**» como margen, «**dos conversaciones al año**» con gente de fuera (cap. 10) — son
  criterio mío, no datos; se pueden recalibrar, pero **hay que recalibrarlos a la vez** en los
  capítulos 5, 10 y 13, donde se repiten.

### 3.4 · El derecho laboral — el punto más delicado

**El capítulo 14 entero se apoya en el Estatuto de los Trabajadores español**, y así se dice en las
fuentes (`16:198`). Las tres formas de pedir el paracaídas —periodo de prueba explícito,
interinidad o suplencia con fin fijado, y el compromiso por escrito en un correo— son figuras
españolas.

- **Interinidad** y **suplencia** no tienen equivalente directo en muchos países.
- **Categoría** (`03:181`, «funciones nuevas, categoría nueva, sueldo nuevo») es una noción de
  convenio colectivo. En una empresa estadounidense se diría *level* o *grade*, y en muchas no
  existe.
- **Convenio colectivo** (`02:76`, «está en la intranet, en la carpeta compartida de recursos
  humanos o **en el convenio**») — en países sin negociación colectiva sectorial esa frase manda al
  lector a un documento que no existe.
- **Plaza** (cap. 12, Pilar) es vocabulario de sanidad pública española.

**Esto no lo puede resolver un traductor solo.** Hay que revisar el capítulo 14 y las tres
menciones del convenio con alguien que conozca el marco laboral de destino, y reescribir la nota
legal de `16:198` para ese marco. Lo que sí es universal es el argumento: *el paracaídas se pide
antes porque el primer día sale gratis y el día doscientos se negocia desde abajo.*

### 3.5 · Los modismos que no sobreviven

Traducidos literalmente pierden el sentido o suenan a manual. Hay que buscar el equivalente
funcional, no el literal:

| en el libro | qué significa de verdad | trampa |
|---|---|---|
| **hacer la pelota** (caps. 1, 8) | congraciarse | Es el título de una sección y el eje del capítulo 8. El término elegido tiene que aguantar el capítulo entero y tener la misma carga negativa coloquial |
| **el efecto baba** (`08:167`) | el *slime effect* de Vonk | Aquí es al revés: el término técnico es inglés. En traducción hay que decidir si se usa el original o se acuña |
| **el marrón** (caps. 6, 7, 9, 12) | la tarea ingrata que nadie quiere | Aparece 6 veces y **titula una sección** («El marrón que nadie quiere»). Es una pieza central: el marrón es la oportunidad sin competencia |
| **funciona en cuatro días** (`11:106`) | funciona *enseguida* | **No es una duración.** Ya se rechazó una revisión externa que lo leyó como cuatro días literales |
| **echar horas** (`03:138`) | dedicar tiempo de más | |
| **a toro pasado** (`03:69`) | cuando ya ha ocurrido | Imagen taurina; en muchos mercados es inaceptable además de opaca |
| **llamar a puerta fría** (`04:4`) | venta a puerta fría | Y ojo: contiene *puerta*, que es el armazón del capítulo 4. Elegir un término que no colisione |
| **a lo bruto** (`07:43`, `11:144`) | sin sutilezas | |
| **vender la moto / esa moto** (`07:153`) | vender humo | |
| **dar la cara** (`11:247`) | responder de algo en público | Es uno de los cinco movimientos, tiene que quedar accionable |
| **quedar de quejica** (`13:125`) | parecer un quejumbroso | Titula una sección |

### 3.6 · Nombres y lugares

Catorce personajes con nombre español: **Javier** (45 menciones), **Marta** (36), **Nacho**,
**Rubén**, **Pilar**, **Andrés**, **Toni**, **Nando**, **Sonia**, **Nuria**, **Ramón**, **Rosa**,
**Quique**, **Lucía**.

Se localizan, no se transliteran. Dos condiciones al elegir los nuevos:

1. **Que se distingan entre sí en la primera letra y en la longitud.** Marta y Javier aparecen en
   nueve capítulos y a veces en la misma frase.
2. **Que no sean nombres de clase alta ni de ejecutivo.** El libro va deliberadamente de gente de
   tienda, almacén, cocina, planta de hospital y oficina normal. Un reparto de nombres
   aspiracionales cambia a quién le está hablando el libro.

**Lugares:** *Sagunto* (`10:9`, `10:119`) es el ejemplo de «una frase corta, verificable y con un
hecho dentro»; hace falta una ciudad industrial de segunda fila reconocible, no la capital.
*Barcelona* (`01:36`) igual. *«La oficina de otra provincia»* (`10:167`) necesita la unidad
administrativa del país de destino.

### 3.7 · Los sectores

Los catorce capítulos rotan de sector a propósito, y está vigilado en el verificador (tabla
`SECTOR`): oficina, técnico, ventas, restauración, logística, industria, jurídico, retail, sanidad.
Hay vocabulario de oficio dentro que un traductor generalista traducirá mal: **escandallo**,
**comanda**, **hoja de reposición**, **jefe de zona**, **supervisora de área**, **jefe de
plataforma**, **nave**. Cada uno necesita el término que usa esa profesión en el país de destino,
no el del diccionario.

---

## 4 · El registro

El libro **tutea de principio a fin**: 545 marcas de segunda persona del singular y ninguna de
usted. No es un detalle de estilo, es la relación que el libro establece con el lector, y sostiene
frases como «si esto te ha molestado, estamos empezando bien».

- **Inglés:** no hay problema formal, pero hay que vigilar que no se formalice solo. El inglés
  empresarial arrastra el tono de consultoría, que es exactamente el registro del que este libro
  se distingue.
- **Alemán, francés, italiano, neerlandés:** hay que **decidir explícitamente** *du/Sie*, *tu/vous*,
  *tu/Lei* antes de traducir la primera página, y sostenerlo 144 páginas. El *Sie* convertiría el
  libro en otro libro.
- **Japonés, coreano:** el nivel de cortesía cambia el género entero del texto.

**Sobre lo agresivo.** El original es directo pero nunca agresivo, y esa línea la marcan cosas
concretas que hay que conservar:

- Concede antes de discutir: *«Y no iba del todo desencaminada»*, *«tiene su parte de razón»*,
  *«es verdad y la sostengo»*.
- Nunca culpa al lector: el enemigo del libro es la **falta de información**, no la falta de
  carácter. La frase del epílogo es *«no hacen nada mal»*.
- Dice sus reservas en voz alta: *«esto no es un modelo científico validado»*, *«son datos de los
  años ochenta»*, *«es un estudio observacional»*. **Estas reservas no son relleno y no se recortan.**
- Y hay un límite ético explícito en el capítulo 8 y en el 13. Si la traducción sube el tono, el
  libro pasa a ser el manual de trepas del que se distingue en la página 1.

Un aviso sobre el mercado anglosajón en particular: **la tentación será subir el tono** —títulos
más agresivos, promesas más grandes, imperativos—. Ya se rechazó por eso un subtítulo propuesto
(«el sistema oculto para… hackear tu empresa y ganar lo que realmente mereces»): contradice el
capítulo de ética, contradice la corrección central del libro y usa el registro del que el libro
se separa.

---

## 5 · Las redes: qué sirve tal cual y qué hay que construir

`check_manuscrito.py` emite veintiuna etiquetas de error o aviso, más los dos barridos de libro
entero (`ECO` y `ESTRIBILLO`). Para una traducción se reparten así:

**Sirven sin tocar nada** (no miran palabras):
- `ECO` — párrafos del libro que se repiten entre sí por n-gramas. Funciona en cualquier lengua y
  es la que destapó que la historia de la hamburguesa estaba contada dos veces.
- Extensión por capítulo, densidad de párrafos.

**Sirven cambiando el diccionario** (misma lógica, otras palabras). Hay que traducir las tablas
`CUENTA`, `REPARTO`, `TRIADAS`, `METAFORA`, `ORDINALES`, `ESTRIBILLOS`, `FRANQUEZA`, `CRONOLOGIA`,
`ABSOLUTOS`, `PORCENTAJES_FALSOS`, `MULETAS`, `SERMON`, `DECENA`, `COTEJO`:
- `CUENTA`, `CRUCE`, `SALA`, `CRONOLOGÍA`, `TRIADAS`, `METÁFORA`, `COTEJO`, `DEPÓSITOS`,
  `COLUMNA/FILA`, `FRANQUEZA`.

**Hay que rehacerla entera:**
- `RAYA` — la raya española pegada al texto (`lo mismo —pero se nota`) no es la convención del
  inglés (*em dash* sin espacios o *spaced en dash*), del alemán ni del francés (que además pone
  espacio fino antes de `:` y `?`). Es puramente tipográfica y hay que reescribirla por lengua.

**Hay que construirla nueva, y es la más importante de todas para una traducción:**

> **`PARIDAD`** — comparar el original y la traducción capítulo a capítulo y verificar que **todas
> las cantidades sobreviven**. Se extraen las cifras de cada capítulo del original (en dígitos y en
> letra) y las del capítulo correspondiente traducido, y se comparan los multiconjuntos. Si el
> capítulo 4 en castellano dice «siete» nueve veces y en la traducción aparece siete veces, algo se
> ha perdido por el camino. Es la red que caza el fallo más típico y más caro de una traducción de
> este libro: que el armazón numérico se erosione frase a frase sin que nadie lo note hasta que un
> lector suma.

Y una segunda, más barata: **verificar que las 47 referencias cruzadas siguen apuntando al mismo
capítulo**, que es mecánico y no depende de la lengua si se comparan por posición.

---

## 6 · Cómo se traduce sin saltarse las redes

El orden natural —capítulo 1, luego el 2, luego el 3— es el que produce la
deriva. Todos los defectos que hubo que arreglar en el original eran de deriva:
las cinco escaleras que en el capítulo 2 se volvieron puertas mientras el 4 ya
tenía las suyas; la historia de la hamburguesa contada en el 2 y otra vez en el
3; el capítulo 14 volviendo a argumentar lo que el 3 ya había argumentado; el
recuento de las siete rompiéndose entre el 6 y el 12; los dos años de Pilar
contra los cuatro dentro de la misma sección; una sala con tres sillas en el
capítulo 1 y cuatro personas sentadas en el 10.

Todos aparecieron escribiendo en orden, con libertad total sobre el texto. En
una traducción la superficie cambia en cada línea y los anclajes dejan de ser
cadenas idénticas, así que la deriva es **más** fácil, no menos. De ahí este
orden, que no es el natural.

**Fase 0 — congelar las decisiones.** Un `GLOSARIO.<lengua>.md` con el
diccionario de un término por concepto (§ 2), el registro (§ 4), el reparto de
nombres (§ 3.6) y las equivalencias de modismos (§ 3.5). Por escrito y cerrado.
La deriva es, casi siempre, volver a decidir en la página 90 algo que ya se
decidió en la 12.

**Fase 1 — traducir los anclajes antes que la prosa.** Fuera de orden y como
lista, no como texto seguido. Son unas **190 unidades**: 17 títulos de capítulo,
111 de sección, 13 ganchos, 36 filas de tabla y 13 frases literales de las que
el lector tiene que decir en voz alta, más el estribillo y los siete cierres con
recuento. Se fijan primero y los capítulos se traducen **alrededor** de cadenas
ya congeladas. Es el movimiento que más deriva evita, porque pone a salvo justo
lo que más se repite.

**Fase 2 — los capítulos, en orden**, con el glosario delante y releyendo el
cierre del capítulo anterior antes de empezar el siguiente. El 16, las fuentes,
**el último**: las reservas tienen que decir lo que el texto traducido acabe
afirmando, no lo que afirmaba el original.

**Fase 3 — la máquina.** Traducir las tablas de palabras del verificador (§ 5),
pasarlo, y añadir `PARIDAD`. Y `registro.py --comparar`, que pone la huella de
tono del original al lado de la de la traducción capítulo a capítulo.

**Fase 4 — retrotraducción a ciegas del 10 % más delicado.** Coger los pasajes
de más riesgo —las definiciones de los cinco depósitos, las tres puertas, las
cinco reglas del capítulo 8, los cinco movimientos del 11, el guion del 12— y
traducirlos de vuelta al castellano **sin mirar el original**. Luego comparar.
Donde el sentido se ha movido, se ve. Ninguna comprobación automática caza eso.

**Fase 5 — cinco lectores del país de destino**, de sectores distintos. Lo que
hay que preguntarles no es si se entiende:

- ¿Reconoces la sala del capítulo 1? ¿Existe esa reunión en tu empresa?
- ¿Te suena falso algún ejemplo?
- ¿En qué momento has pensado «esto aquí no funciona así»?
- ¿El libro te trata como a un igual o te está vendiendo algo?

---

## 7 · La huella de tono del original

Medida con `libro/tools/registro.py`. Son proxies groseros —lista cerrada de
imperativos, la segunda persona sin desambiguar—, y no sirven para puntuar
prosa. Sirven para una cosa: **ver si un capítulo se sale de la curva.**

| cap. | 2ª pers./1.000 | imperativos/1.000 | palabras por frase |
|---|---|---|---|
| 1 | 22 | 5,4 | 15,9 |
| 5 | 18 | 11,9 | 15,9 |
| 8 | 11 | 6,0 | 18,2 |
| 9 | 30 | 8,4 | 16,3 |
| 10 | 27 | 3,7 | 17,1 |
| 14 | 12 | 6,9 | 17,2 |
| 16 | 3 | 1,4 | 10,3 |

El cuerpo se mueve entre 11 y 30 de segunda persona, entre 3,7 y 12,3 de
imperativo, y **la frase se mantiene entre 15 y 18 palabras en los catorce
capítulos**. Esa última es la más estable y la más reveladora: si un capítulo
traducido sube a 24 palabras por frase, ha cambiado de género aunque cada frase
suelta esté bien.

El 16 se sale a propósito —es la bibliografía y tiene otro registro—; sirve de
control: si un capítulo del cuerpo se le empieza a parecer, algo va mal.

---

## 8 · Resumen del orden de trabajo

1. Fijar el **diccionario de una entrada por concepto** (§ 2) y el **registro** (§ 4). Por escrito,
   antes de traducir nada.
2. Elegir el **reparto de nombres y lugares** (§ 3.6) entero de una vez, no sobre la marcha.
3. Resolver el **capítulo 14 y el marco laboral** (§ 3.4) con alguien del país. Puede obligar a
   reescribir la sección, no solo a traducirla.
4. Traducir.
5. Traducir las tablas del verificador y pasarlo. Añadir `PARIDAD`.
6. **Prueba de lectura con cinco lectores del país de destino**, de sectores distintos, que es lo
   que el original tampoco ha tenido todavía.

Lo que hay que preguntarle a cada uno de esos cinco no es si se entiende. Es esto:

- ¿Reconoces la sala del capítulo 1? ¿Existe esa reunión en tu empresa?
- ¿Te suena falso algún ejemplo?
- ¿En qué momento has pensado «esto aquí no funciona así»?
- ¿El libro te trata como a un igual o te está vendiendo algo?
