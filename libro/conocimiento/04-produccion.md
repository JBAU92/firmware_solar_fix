# Producción: del markdown a KDP

El manuscrito vive en `manuscrito/*.md` y de ahí salen **las dos ediciones**. Eso no es comodidad:
es lo que hace que una corrección llegue al papel y al Kindle sin que nadie tenga que acordarse.

---

## El interior en papel — Typst

`build_libro.py`. Typst resuelve de fábrica lo que en un navegador hay que hacer a mano: guionado
en español, aperturas a página impar, folios, titulillos, índice con números de página reales e
incrustación de fuentes.

**Especificación KDP que se usó:** 5,5 × 8,5 pulgadas · tinta negra sin un solo valor de color ·
márgenes espejados (0,80" interior / 0,55" exterior / 0,72" arriba y abajo) · Source Serif 4 a
10,6 pt.

### Tres trampas de fuentes y composición

1. **Bitstream Charter no carga.** Está instalada pero en Type 1 (`.pfb`), que ni Chromium ni Typst
   leen. Caía en silencio a Liberation Serif, un clon de Times, y nadie se enteraba.
2. **La versión *variable* de Source Serif produce fuentes Type 3** — contornos sueltos en vez de
   fuente incrustada. **KDP lo rechaza** y el archivo se hincha. Hay que usar las **instancias
   estáticas** (Regular, It, Bold, BoldIt) en `~/.fonts`.
3. **El navegador no compone libros.** Hubo una versión con Chromium que iteraba saltos de página,
   silabeaba en Python y estampaba folios con `pypdf`. Funcionaba y era frágil. Typst hace las tres
   cosas de serie.

### Detalle de guionado

El coste de guionado se subió a **250 %** a propósito. Con el valor por defecto Typst partía 107
palabras y algunas quedaban feas siendo correctas —«reunio-nes», «promocio-nes»—: la línea acaba en
dos vocales y engancha la vista. A 250 % no queda ninguna.

### Verificación del PDF

`pypdf` necesita un apaño en este entorno: un `cryptography/__init__.py` de mentira que lanza
`ImportError`, cargado por `PYTHONPATH`. Sin eso, `pypdf` falla al importar.

---

## La cubierta de papel

Geometría para **144 páginas en papel crema**: 11,610 × 8,750 pulgadas, lomo de **0,360"** (9,14
mm), recuadro del código de barras de 2,00 × 1,20" a 0,25" del borde inferior y derecho.

El lomo depende del número de páginas: **si cambia la paginación, cambia la cubierta**. Es la
dependencia que más fácil se olvida.

---

## La edición Kindle — EPUB

`build_epub.py` y `check_epub.py`.

### Qué formato acepta KDP

| Formato | Veredicto |
|---|---|
| **EPUB** | ✅ Lo que usamos. Amazon lo acepta y dice explícitamente que puedes crearlo con cualquier herramienta de terceros |
| **KPF** | Solo sale de **Kindle Create**, aplicación de escritorio de Amazon. No se puede generar de otra manera |
| **DOCX** | Se acepta, pero la conversión «puede romper las tablas y el espaciado». Con cinco tablas, descartado |
| **PDF** | Se acepta y es la peor opción: página fija, el lector no puede cambiar el cuerpo de letra |
| **MOBI** | Muerto |

> ⚠️ **La trampa cara.** Kindle Create importa PDF, pero esa vía produce un **Print Replica** de
> página fija. Y cambiar de ajustable a Print Replica o al revés **obliga a despublicar y publicar
> como título nuevo**: pierdes la ficha, las reseñas y el ranking. No acerques el PDF de imprenta a
> Kindle Create.

### Qué se quita respecto al papel

Páginas de cortesía, aperturas a impar, folios, titulillos y el índice con números de página. El
índice del EPUB lleva enlaces, más el índice lógico (`nav.xhtml` + `toc.ncx`) que es el que usan el
botón «Ir a» y el menú del lector.

**No se incrusta ninguna tipografía.** En un Kindle la elige quien lee, y un libro que le pelea la
elección se lee peor.

### La posición de inicio de lectura

Dónde se abre el libro la primera vez y dónde arranca la muestra gratuita que decide la compra.
Kindle la saca del **`<guide>` del OPF**, que EPUB 3 tiene deprecado en favor de los *landmarks*
del `nav` — pero **el convertidor de Amazon sigue leyendo el `<guide>` viejo**. Poniendo solo el
moderno, KDP avisa de que no está fijada y el lector puede estrenar el libro en la página de
créditos. Hay que emitir los dos. Apunta al prólogo.

### Las tablas

Con reparto automático de columnas, `table-layout: fixed` reparte a partes iguales y la columna de
un número ocupa lo mismo que la de una frase de sesenta caracteres. El ancho se calcula midiendo el
contenido de cada columna, amortiguado con una raíz para que una columna de frases no se coma a las
demás. La **alineación** se decide por las celdas y **no por la cabecera**: «Puedo practicarla» es
un rótulo largo sobre una columna de cifras de un dígito.

Un cuadro con la mayoría de las casillas vacías no es un cuadro, es un formulario: se dibuja con la
cuadrícula visible.

### La portada del ebook

**Solo la cara delantera.** Nada de lomo ni contraportada. JPG o TIFF —**no PDF**—, proporción
1,6:1, ideal **1600 × 2560 px**, RGB, menos de 50 MB.

---

## Antes de subir nada

**Kindle Previewer.** Es lo que Amazon recomienda y lo único que reproduce su conversión.
`check_epub.py` verifica estructura y contenido; no sustituye a Previewer.
