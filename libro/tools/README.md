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

## `build_pdf.py` — el dosier de preproducción

Genera un PDF A4 del dosier de trabajo (`libro/*.md`), que es material interno, no el libro.
Convierte el markdown a HTML y lo imprime con Chromium; no necesita nada más.

```bash
python3 libro/tools/build_pdf.py
```
