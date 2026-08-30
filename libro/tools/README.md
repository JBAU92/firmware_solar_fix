# Herramientas

## `build_pdf.py`

Genera un PDF único (A4, con portada e índice) a partir de los once documentos del dossier.
No necesita pandoc ni librerías externas: convierte el markdown a HTML y lo imprime con Chromium.

```bash
python3 libro/tools/build_pdf.py
CHROME=/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell
$CHROME --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
        --print-to-pdf=ESCALA-estudio-preproduccion.pdf \
        file://$PWD/pdf-source.html
```

En otra máquina, cualquier Chrome o Chromium sirve: `chrome --headless --print-to-pdf=...`.
Ajusta `BASE` y `OUT` al principio del script si cambian las rutas.

Tipografías usadas: Bitstream Charter (texto), DejaVu Sans (tablas y etiquetas),
DejaVu Sans Mono (código). Si no están instaladas, cae en Georgia y en la sans del sistema.
