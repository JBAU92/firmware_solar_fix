# Herramientas

## `build_libro.py` — el interior del libro para KDP

Genera el PDF de imprenta a partir de `manuscrito/*.md`. Compone con **Typst**, que se
encarga del guionado en español, de que cada capítulo abra en página impar, de los folios,
los titulillos, el índice con números de página reales y la incrustación de las fuentes.

```bash
python3 libro/tools/build_libro.py <directorio_de_salida>
```

Deja en ese directorio `libro.typ` (fuente compuesta) y el PDF final.

**Qué produce:** 5,5 × 8,5 pulgadas · tinta negra, sin un solo valor de color · márgenes
espejados (0,80" interior / 0,55" exterior / 0,72" arriba y abajo) · Source Serif 4 a 10,6 pt
incrustada en subconjuntos TrueType.

### Requisitos

```bash
# Typst
curl -sSL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz \
  | tar xJ && sudo mv typst-*/typst /usr/local/bin/

# Source Serif 4, instancias estáticas (NO la variable, ver abajo)
mkdir -p ~/.fonts && cd ~/.fonts
for s in Regular It Bold BoldIt; do
  curl -sSLO "https://raw.githubusercontent.com/adobe-fonts/source-serif/release/TTF/SourceSerif4-$s.ttf"
done && fc-cache -f
```

### Tres trampas que costaron caro y conviene no repetir

1. **Bitstream Charter no sirve aquí.** Está instalada, pero en formato Type 1 (`.pfb`), que
   ni Chromium ni Typst cargan. Caía sin avisar a Liberation Serif, un clon de Times.
2. **La versión *variable* de Source Serif produce fuentes Type 3**, es decir, contornos
   sueltos en vez de una fuente incrustada de verdad: KDP lo rechaza y el archivo se hincha.
   Con las instancias estáticas se incrusta TrueType correctamente.
3. **La composición en navegador no llega.** Chromium ignora `break-before: right`, no trae
   diccionario de guionado en español y no sabe numerar páginas. Hubo una versión que
   resolvía las tres cosas a mano —iterando saltos, silabeando en Python y estampando folios
   con `pypdf`— y era frágil. Typst hace las tres de fábrica.

## `check_manuscrito.py` — el verificador

Comprueba las nueve trampas de `manuscrito/REGLAS.md` en cada capítulo: cifras inventadas en
escena, citas de la lista negra, densidad de muletillas, sermones, presencia del hilo de Marta
y Javier en los capítulos con revelación, extensión, cadencia de máquina y el gancho final.

```bash
python3 libro/tools/check_manuscrito.py     # devuelve 1 si hay algún fallo
```

Prólogo, epílogo y el apartado de fuentes tienen objetivo de extensión propio, y el de fuentes
está exento de la lista negra porque su cometido es precisamente nombrarla.

## `build_epub.py` — la edición Kindle

Genera el EPUB 3 a partir del **mismo** `manuscrito/*.md` que el PDF, para que una
corrección llegue a las dos ediciones sin que nadie tenga que acordarse.

```bash
python3 libro/tools/build_epub.py <directorio_de_salida> [--portada portada.jpg]
```

**Qué cambia respecto al papel:** no hay páginas de cortesía ni aperturas a impar, no hay
folios ni titulillos, el índice lleva enlaces en vez de números de página, y va además el
índice lógico (`nav.xhtml` + `toc.ncx`) que es el que usan el botón «Ir a» y el menú del
lector. No se incrusta ninguna tipografía: en un Kindle la elige quien lee.

La portada del ebook es **solo la cara delantera**, JPG o TIFF, proporción 1,6:1 —lo suyo
1600 × 2560 px— y en RGB. La cubierta envolvente del papel, con lomo y código de barras, no
vale aquí.

### La trampa de las tablas

Con el reparto de columnas automático, en una pantalla estrecha la tabla se sale y lo que
cae fuera **desaparece sin avisar**: la cuadrícula del capítulo 1 perdía la columna donde
está Marta. Por eso el ancho de cada columna se calcula midiendo su contenido, amortiguado
con una raíz para que una columna de frases largas no se coma a las demás, y la tabla va con
`table-layout: fixed`.

Aviso sobre cómo comprobarlo: Chromium en modo *headless* **maqueta a 500 px aunque le pases
`--window-size=390`** y luego recorta la captura. Una tabla que parece salirse puede estar
perfectamente encajada. Para verlo de verdad hay que meter el contenido en un contenedor de
ancho fijo y hacer que la propia página escriba su anchura dentro de la captura.

## `check_epub.py` — la red del EPUB

```bash
python3 libro/tools/check_epub.py libro.epub    # devuelve 1 si hay algún fallo
```

Comprueba el envoltorio (`mimetype` primero y sin comprimir, `container.xml`, el manifiesto
completo en las dos direcciones, un único `nav`, el `spine`), que cada documento sea XML
válido y que ningún enlace del índice ni del `toc.ncx` lleve a un archivo que no está.

Y sobre todo compara el recuento de palabras, tablas y capítulos **contra el manuscrito**,
que es lo único que demuestra que en la conversión no se ha quedado nada por el camino.

No sustituye a **Kindle Previewer**, que es lo que Amazon recomienda y lo único que reproduce
su conversión. Hay que pasarlo por ahí antes de subir.

## `build_pdf.py` — el dosier de preproducción

Genera un PDF A4 del dosier de trabajo (`libro/*.md`), que es material interno, no el libro.
Convierte el markdown a HTML y lo imprime con Chromium; no necesita nada más.

```bash
python3 libro/tools/build_pdf.py
```
