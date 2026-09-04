#!/usr/bin/env python3
"""Compone la edición Kindle (EPUB 3) desde el mismo manuscrito que el PDF.

El PDF y el EPUB salen del mismo markdown a propósito: cualquier corrección en
`manuscrito/` llega a las dos ediciones sin que haya que acordarse de nada.

Lo que cambia respecto al papel, porque no tiene sentido en pantalla:
  · no hay páginas de cortesía ni aperturas a impar
  · no hay folios ni titulillos
  · el índice no lleva números de página: lleva enlaces, y además va el índice
    lógico (nav + ncx) que es el que usan el botón «Ir a» y el menú del lector
  · no se incrusta ninguna tipografía: en un Kindle manda el lector, y un libro
    que le pelea la fuente elegida se lee peor, no mejor

Uso:  build_epub.py <directorio_de_salida> [--portada portada.jpg]

Después de generarlo hay que pasarlo por Kindle Previewer, que es lo que Amazon
recomienda y lo único que reproduce de verdad su conversión.
"""
import re, sys, uuid, pathlib, zipfile, datetime, argparse
import xml.etree.ElementTree as ET

BASE = pathlib.Path(__file__).resolve().parents[2] / 'manuscrito'

TITULO    = 'Nadie va a venir a elegirte'
SUBTITULO = ('Cómo se decide quién asciende, y las siete cosas que ponen tu '
             'nombre encima de esa mesa')
AUTOR     = 'Adrian K. Wells'
ANIO      = '2026'
IDIOMA    = 'es'
# Identificador propio del EPUB. No es el ISBN: Amazon asigna un ASIN al
# publicar y el ISBN del papel es de otra edición. Fijo, para que una
# reconstrucción del archivo no parezca un libro distinto.
URN = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL,
                                   'nadie-va-a-venir-a-elegirte/' + AUTOR))

# ------------------------------------------------------------------ markdown
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def linea(s):
    s = esc(s)
    s = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', s)
    return s

def tabla(cab, filas):
    """Las mismas dos formas que en el papel: cuadro de lectura y formulario.

    Un cuadro con la mayoría de las casillas vacías no es un cuadro: es una
    plantilla para rellenar, y se dibuja con la cuadrícula visible.

    El ancho de cada columna se reparte aquí y no se deja al lector. Con el
    reparto automático, en la pantalla de un teléfono la tabla se sale y lo que
    cae fuera desaparece sin avisar: la cuadrícula del capítulo 1 perdía la
    columna donde está Marta, y el inventario del 5 perdía la del total. Se mide
    el contenido de cada columna y se le da su parte, amortiguada con una raíz
    para que una columna de frases largas no se coma a las demás."""
    sueltas = [c for f in filas for c in f[1:]]
    form = bool(sueltas) and sum(1 for c in sueltas if not c) * 2 > len(sueltas)
    cls = 'form' if form else 'cuadro'
    if len(cab) >= 5:
        cls += ' estrecha'

    n = len(cab)
    largo = [max([len(cab[j])] + [len(f[j]) for f in filas if j < len(f)])
             for j in range(n)]
    peso = [max(l, 3) ** 0.6 for l in largo]
    total = sum(peso)
    anchos = [round(100 * w / total, 1) for w in peso]
    # Una columna de frases se lee alineada a la izquierda; una de cifras o de
    # casillas para marcar, centrada. Se decide midiendo las celdas y no la
    # cabecera: «Puedo practicarla» es un rótulo largo sobre una columna de
    # cifras de un dígito, y alinearla por el rótulo la deja descolgada.
    cuerpos = [max([0] + [len(f[j]) for f in filas if j < len(f)])
               for j in range(n)]
    izq = [l > 9 for l in cuerpos]
    marca = lambda j: ' class="izq"' if izq[j] else ''

    out = [f'<table class="{cls}">', '<colgroup>']
    out += [f'<col style="width:{a}%"/>' for a in anchos]
    out += ['</colgroup>', '<thead><tr>']
    out += [f'<th{marca(j)}>{linea(c)}</th>' for j, c in enumerate(cab)]
    out += ['</tr></thead>', '<tbody>']
    for f in filas:
        out.append('<tr>' + ''.join(
            f'<td{marca(j)}>{linea(c) if c else "&#160;"}</td>'
            for j, c in enumerate(f)) + '</tr>')
    out += ['</tbody>', '</table>']
    return '\n'.join(out)

def cuerpo(md):
    """markdown → xhtml. Mismo dialecto que build_libro.py."""
    ls = md.split('\n'); out = []; i = 0; n = len(ls); titulo = num = ''
    while i < n:
        ln = ls[i]
        if ln.startswith('>'):
            buf = []
            while i < n and ls[i].startswith('>'):
                buf.append(ls[i].lstrip('>').strip()); i += 1
            t = ' '.join(buf).strip()
            gancho = t.startswith('GANCHO')
            t = re.sub(r'^GANCHO\s*—\s*', '', t)
            out.append(f'<div class="{"gancho" if gancho else "cita"}">'
                       f'<p>{linea(t)}</p></div>')
            continue
        if re.match(r'^\s*---+\s*$', ln):
            out.append('<p class="filete">§</p>'); i += 1; continue
        if (ln.strip().startswith('|') and i + 1 < n
                and re.match(r'^\s*\|[\s:|-]*-[\s:|-]*\|\s*$', ls[i + 1])):
            cel = lambda s: [c.strip() for c in s.strip().strip('|').split('|')]
            cab = cel(ln); i += 2; filas = []
            while i < n and ls[i].strip().startswith('|'):
                filas.append(cel(ls[i])); i += 1
            out.append(tabla(cab, filas)); continue
        m = re.match(r'^(#{1,3})\s+(.*)$', ln)
        if m:
            lvl, t = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                num, _, resto = t.partition(' · ')
                if not resto: num, resto = '', t
                titulo = resto
                if num:
                    out.append(f'<p class="numcap">{linea(num)}</p>')
                out.append(f'<h1>{linea(resto)}</h1>')
            else:
                out.append(f'<h2>{linea(t)}</h2>')
            i += 1; continue
        if ln.strip():
            buf = [ln.strip()]; i += 1
            while (i < n and ls[i].strip()
                   and not re.match(r'^\s*(#{1,3}\s|>|\||---+\s*$)', ls[i])):
                buf.append(ls[i].strip()); i += 1
            out.append('<p>' + linea(' '.join(buf)) + '</p>')
            continue
        i += 1
    return '\n'.join(out), titulo, num

# ------------------------------------------------------------------ plantillas
XHTML = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{idioma}" lang="{idioma}">
<head>
<meta charset="utf-8"/>
<title>{titulo}</title>
<link rel="stylesheet" type="text/css" href="estilo.css"/>
</head>
<body epub:type="{tipo}">
{cuerpo}
</body>
</html>
'''

CSS = '''@charset "utf-8";
/* Hoja deliberadamente corta. En un lector de tinta electrónica manda quien
   lee: cuerpo, tipografía, interlineado y márgenes los pone el aparato. Aquí
   solo se define lo que el texto necesita para no perder sentido. */

body        { margin: 0; padding: 0; font-family: serif; widows: 2; orphans: 2; }
p           { margin: 0; text-indent: 1.2em; text-align: justify;
              line-height: 1.45; }
/* Un primer párrafo con sangría después de un título parece un error. */
h1 + p, h2 + p, .numcap + p, .filete + p, .gancho + p, .cita + p,
table + p, p.primera { text-indent: 0; }

h1          { page-break-before: always; break-before: page;
              margin: 0 0 1.1em 0; padding: 0;
              font-size: 1.6em; font-weight: bold; line-height: 1.2;
              text-align: left; text-indent: 0; }
h2          { margin: 1.5em 0 0.5em 0; font-size: 1em; font-weight: bold;
              text-align: left; text-indent: 0; page-break-after: avoid; }
p.numcap    { margin: 0 0 0.4em 0; text-indent: 0; text-align: left;
              font-size: 0.75em; letter-spacing: 0.16em;
              text-transform: uppercase; }
p.filete    { margin: 1.1em 0; text-indent: 0; text-align: center;
              letter-spacing: 0.4em; }

.cita       { margin: 0.9em 0 0.9em 1.4em; font-style: italic; }
.cita p     { text-indent: 0; text-align: left; }
/* El gancho abre capítulo en el papel con un filete encima. Aquí igual. */
.gancho     { margin: 1.3em 0 0.9em 0; padding-top: 0.7em;
              border-top: 2px solid; }
.gancho p   { text-indent: 0; font-style: italic; text-align: left; }

table       { width: 100%; table-layout: fixed; border-collapse: collapse;
              margin: 1.1em 0; font-size: 0.85em; page-break-inside: avoid; }
th, td      { padding: 0.35em 0.3em; text-align: center;
              vertical-align: middle;
              word-wrap: break-word; overflow-wrap: break-word; }
th          { font-weight: bold; }
th.izq, td.izq { text-align: left; }
table.cuadro thead tr  { border-top: 2px solid; border-bottom: 1px solid; }
table.cuadro tbody tr:last-child { border-bottom: 2px solid; }
/* Formulario: se ve la cuadrícula porque hay que copiarla y rellenarla. */
table.form th, table.form td { border: 1px solid; }
table.form td { height: 1.6em; }
/* Seis columnas no caben en un teléfono con el cuerpo normal. */
table.estrecha { font-size: 0.68em; }
table.estrecha th, table.estrecha td { padding: 0.25em 0.12em; }

/* Preliminares */
.portadilla { text-align: center; margin-top: 25%; }
.portadilla .tit { font-size: 2em; font-weight: bold; line-height: 1.15;
                   margin: 0 0 0.7em 0; text-indent: 0; text-align: center; }
.portadilla .sub { font-size: 1.05em; font-style: italic; line-height: 1.4;
                   margin: 0 0 2.2em 0; text-indent: 0; text-align: center; }
.portadilla .aut { font-size: 1em; letter-spacing: 0.18em;
                   text-transform: uppercase; text-indent: 0;
                   text-align: center; margin: 0; }
.creditos   { font-size: 0.82em; }
.creditos p { text-indent: 0; text-align: left; margin: 0 0 0.8em 0;
              line-height: 1.4; }
nav.indice ol      { list-style: none; margin: 0; padding: 0; }
nav.indice li      { margin: 0 0 0.55em 0; line-height: 1.35; }
nav.indice a       { text-decoration: none; }
nav.indice .n      { font-size: 0.8em; letter-spacing: 0.1em;
                     text-transform: uppercase; }
h1.sinsalto { page-break-before: avoid; break-before: auto; }
'''

# ------------------------------------------------------------------ montaje
def construir(salida, portada=None):
    fich = sorted(BASE.glob('[0-9]*.md'))
    if not fich:
        sys.exit('no encuentro el manuscrito en ' + str(BASE))

    caps, docs = [], {}
    for f in fich:
        html, titulo, num = cuerpo(f.read_text())
        nombre = f.stem + '.xhtml'
        docs[nombre] = XHTML.format(idioma=IDIOMA, titulo=esc(titulo),
                                    tipo='bodymatter', cuerpo=html)
        caps.append((nombre, titulo, num))

    # --- preliminares
    docs['portadilla.xhtml'] = XHTML.format(
        idioma=IDIOMA, titulo=esc(TITULO), tipo='titlepage',
        cuerpo=('<div class="portadilla">'
                f'<p class="tit">{esc(TITULO)}</p>'
                f'<p class="sub">{esc(SUBTITULO)}</p>'
                f'<p class="aut">{esc(AUTOR)}</p></div>'))

    creditos = [
        f'{esc(TITULO)}<br/>© {ANIO}, {esc(AUTOR)}<br/>Primera edición, {ANIO}.',
        'Reservados todos los derechos. Queda prohibida la reproducción total o '
        'parcial de esta obra, por cualquier medio o procedimiento, sin la '
        'autorización escrita del titular de los derechos.',
        'Los nombres de las personas que aparecen en los ejemplos y las '
        'situaciones descritas han sido modificados. Cualquier parecido con '
        'personas concretas es casual.',
        'Esta obra tiene una finalidad divulgativa y no constituye asesoramiento '
        'jurídico, laboral ni profesional de ningún tipo. Las decisiones que el '
        'lector tome a partir de su lectura son de su exclusiva responsabilidad. '
        'Para cuestiones legales o laborales conviene acudir a un profesional '
        'cualificado.']
    docs['creditos.xhtml'] = XHTML.format(
        idioma=IDIOMA, titulo='Créditos', tipo='copyright-page',
        cuerpo='<div class="creditos">' +
               ''.join(f'<p>{p}</p>' for p in creditos) + '</div>')

    # Índice visible. El lógico va aparte, en nav.xhtml y toc.ncx.
    def entrada(d, t, n):
        rotulo = '<span class="n">%s</span><br/>' % esc(n) if n else ''
        return '<li>%s<a href="%s">%s</a></li>' % (rotulo, d, esc(t))
    filas = ''.join(entrada(d, t, n) for d, t, n in caps)
    docs['indice.xhtml'] = XHTML.format(
        idioma=IDIOMA, titulo='Índice', tipo='frontmatter',
        cuerpo=('<h1 class="sinsalto">Índice</h1>'
                f'<nav class="indice" epub:type="toc" id="visible" role="doc-toc">'
                f'<ol>{filas}</ol></nav>'))

    orden = ['portadilla.xhtml', 'creditos.xhtml', 'indice.xhtml'] + \
            [d for d, _, _ in caps]
    if portada:
        docs['portada.xhtml'] = XHTML.format(
            idioma=IDIOMA, titulo='Portada', tipo='cover',
            cuerpo='<div style="text-align:center;margin:0;padding:0">'
                   f'<img src="{portada.name}" alt="{esc(TITULO)}" '
                   'style="max-width:100%;height:auto"/></div>')
        orden.insert(0, 'portada.xhtml')

    # --- nav.xhtml (índice lógico EPUB 3)
    nav_items = ''.join(f'<li><a href="{d}">{esc(t)}</a></li>'
                        for d, t, _ in caps)
    nav = XHTML.format(
        idioma=IDIOMA, titulo='Índice', tipo='frontmatter',
        cuerpo=('<nav epub:type="toc" id="toc" role="doc-toc"><h1>Índice</h1>'
                f'<ol>{nav_items}</ol></nav>'
                '<nav epub:type="landmarks" id="landmarks" hidden="hidden"><ol>'
                + (f'<li><a epub:type="cover" href="portada.xhtml">Portada</a></li>'
                   if portada else '')
                + '<li><a epub:type="toc" href="indice.xhtml">Índice</a></li>'
                f'<li><a epub:type="bodymatter" href="{caps[0][0]}">Comienzo</a></li>'
                '</ol></nav>'))

    # --- toc.ncx (lo siguen usando los Kindle antiguos)
    puntos = ''.join(
        f'<navPoint id="np{k}" playOrder="{k}"><navLabel><text>{esc(t)}</text>'
        f'</navLabel><content src="{d}"/></navPoint>'
        for k, (d, t, _) in enumerate(caps, 1))
    ncx = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" '
           f'xml:lang="{IDIOMA}"><head>'
           f'<meta name="dtb:uid" content="{URN}"/>'
           '<meta name="dtb:depth" content="1"/>'
           '<meta name="dtb:totalPageCount" content="0"/>'
           '<meta name="dtb:maxPageNumber" content="0"/></head>'
           f'<docTitle><text>{esc(TITULO)}</text></docTitle>'
           f'<docAuthor><text>{esc(AUTOR)}</text></docAuthor>'
           f'<navMap>{puntos}</navMap></ncx>')

    # --- content.opf
    ident = lambda d: 'x' + d.replace('.', '-')
    manif = [f'<item id="{ident(d)}" href="{d}" media-type="application/xhtml+xml"/>'
             for d in orden]
    manif.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" '
                 'properties="nav"/>')
    manif.append('<item id="ncx" href="toc.ncx" '
                 'media-type="application/x-dtbncx+xml"/>')
    manif.append('<item id="css" href="estilo.css" media-type="text/css"/>')
    if portada:
        tipo = 'image/png' if portada.suffix.lower() == '.png' else 'image/jpeg'
        manif.append(f'<item id="cover-image" href="{portada.name}" '
                     f'media-type="{tipo}" properties="cover-image"/>')
    ahora = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    apellido = AUTOR.rsplit(' ', 1)[-1] + ', ' + AUTOR.rsplit(' ', 1)[0]
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="{IDIOMA}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="pub-id">{URN}</dc:identifier>
<dc:title id="t">{esc(TITULO)}</dc:title>
<meta refines="#t" property="title-type">main</meta>
<dc:title id="s">{esc(SUBTITULO)}</dc:title>
<meta refines="#s" property="title-type">subtitle</meta>
<dc:creator id="a">{esc(AUTOR)}</dc:creator>
<meta refines="#a" property="role" scheme="marc:relators">aut</meta>
<meta refines="#a" property="file-as">{esc(apellido)}</meta>
<dc:language>{IDIOMA}</dc:language>
<dc:date>{ANIO}-01-01</dc:date>
<dc:rights>© {ANIO}, {esc(AUTOR)}</dc:rights>
<meta property="dcterms:modified">{ahora}</meta>
{'<meta name="cover" content="cover-image"/>' if portada else ''}
</metadata>
<manifest>
{chr(10).join(manif)}
</manifest>
<spine toc="ncx">
{chr(10).join(f'<itemref idref="{ident(d)}"/>' for d in orden)}
</spine>
</package>
'''

    # --- escritura del zip
    salida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(salida, 'w') as z:
        # el mimetype va primero y sin comprimir, o no es un epub
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip',
                   compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml',
                   '<?xml version="1.0" encoding="utf-8"?>\n'
                   '<container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/></rootfiles>'
                   '</container>', zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/content.opf', opf, zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/nav.xhtml', nav, zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/toc.ncx', ncx, zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/estilo.css', CSS, zipfile.ZIP_DEFLATED)
        for d, t in docs.items():
            z.writestr('OEBPS/' + d, t, zipfile.ZIP_DEFLATED)
        if portada:
            z.write(portada, 'OEBPS/' + portada.name, zipfile.ZIP_DEFLATED)
    return orden, docs, caps

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('salida', nargs='?', default='/tmp')
    ap.add_argument('--portada', help='jpg o png de la cubierta (solo la cara '
                                      'delantera, 1600x2560)')
    a = ap.parse_args()
    portada = pathlib.Path(a.portada) if a.portada else None
    if portada and not portada.exists():
        sys.exit('no existe ' + str(portada))
    destino = pathlib.Path(a.salida) / 'nadie-va-a-venir-a-elegirte.epub'
    orden, docs, caps = construir(destino, portada)
    print(f'{destino}  ·  {len(caps)} secciones  ·  '
          f'{destino.stat().st_size / 1024:.0f} KB')
    if not portada:
        print('  sin portada incrustada: pásala con --portada cuando la tengas')
    return 0

if __name__ == '__main__':
    sys.exit(main())
