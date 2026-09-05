#!/usr/bin/env python3
"""Comprueba el EPUB antes de subirlo a KDP.

No sustituye a Kindle Previewer, que es lo único que reproduce la conversión de
Amazon. Lo que hace es cazar lo que Previewer no dice con claridad o dice tarde:
que el archivo esté bien formado, que no falte ni sobre nada en el manifiesto, y
—lo que de verdad importa— que en el EPUB esté todo el texto del manuscrito.

Uso:  check_epub.py libro.epub
"""
import sys, re, zipfile, pathlib, posixpath
import xml.etree.ElementTree as ET

BASE = pathlib.Path(__file__).resolve().parents[2] / 'manuscrito'
NS = {'opf': 'http://www.idpf.org/2007/opf',
      'dc':  'http://purl.org/dc/elements/1.1/',
      'c':   'urn:oasis:names:tc:opendocument:xmlns:container',
      'x':   'http://www.w3.org/1999/xhtml',
      'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}

fallos, avisos = [], []
def mal(m):  fallos.append(m)
def ojo(m):  avisos.append(m)

def palabras(t):
    """Palabras de un texto, sin marcas. Sirve para comparar orígenes distintos."""
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&#160;', ' ').replace('&amp;', '&')
    t = re.sub(r'[*_#>|`]', ' ', t)
    t = re.sub(r'^\s*[-:\s|]+$', ' ', t, flags=re.M)
    return [w for w in re.split(r'\s+', t) if re.search(r'\w', w)]

def revisar(ruta):
    z = zipfile.ZipFile(ruta)
    nombres = z.namelist()

    # --- 1. el envoltorio
    if nombres[0] != 'mimetype':
        mal('el primer archivo del zip no es «mimetype»')
    else:
        inf = z.getinfo('mimetype')
        if inf.compress_type != zipfile.ZIP_STORED:
            mal('«mimetype» está comprimido y tiene que ir tal cual')
        if z.read('mimetype') != b'application/epub+zip':
            mal('«mimetype» no dice application/epub+zip')
    if 'META-INF/container.xml' not in nombres:
        return mal('falta META-INF/container.xml'), None

    cont = ET.fromstring(z.read('META-INF/container.xml'))
    rf = cont.find('.//c:rootfile', NS)
    opf_ruta = rf.get('full-path')
    if opf_ruta not in nombres:
        return mal(f'container.xml apunta a «{opf_ruta}», que no está'), None
    raiz = posixpath.dirname(opf_ruta)

    # --- 2. el manifiesto
    opf = ET.fromstring(z.read(opf_ruta))
    meta = opf.find('opf:metadata', NS)
    uid = opf.get('unique-identifier')
    ids = {e.get('id') for e in meta.findall('dc:identifier', NS)}
    if uid not in ids:
        mal(f'unique-identifier «{uid}» no corresponde a ningún dc:identifier')
    for etiqueta in ('dc:title', 'dc:creator', 'dc:language'):
        if meta.find(etiqueta, NS) is None:
            mal(f'falta {etiqueta} en los metadatos')
    if meta.find('opf:meta[@property="dcterms:modified"]', NS) is None:
        mal('falta dcterms:modified, que EPUB 3 exige')

    items = {i.get('id'): i.get('href')
             for i in opf.findall('opf:manifest/opf:item', NS)}
    props = {i.get('id'): (i.get('properties') or '')
             for i in opf.findall('opf:manifest/opf:item', NS)}
    ruta_de = lambda h: posixpath.normpath(posixpath.join(raiz, h))

    for i, h in items.items():
        if ruta_de(h) not in nombres:
            mal(f'el manifiesto declara «{h}» y no está en el zip')
    declarados = {ruta_de(h) for h in items.values()}
    for n in nombres:
        if n in ('mimetype', 'META-INF/container.xml') or n == opf_ruta:
            continue
        if n.endswith('/') or n in declarados:
            continue
        mal(f'«{n}» está en el zip y no en el manifiesto')

    navs = [i for i, p in props.items() if 'nav' in p.split()]
    if len(navs) != 1:
        mal(f'tiene que haber exactamente un item con properties="nav"; hay {len(navs)}')

    lomo = [r.get('idref') for r in opf.findall('opf:spine/opf:itemref', NS)]
    if not lomo:
        mal('el spine está vacío')
    for r in lomo:
        if r not in items:
            mal(f'el spine referencia «{r}», que no está en el manifiesto')
    ncx_id = opf.find('opf:spine', NS).get('toc')
    if ncx_id and ncx_id not in items:
        mal('el spine declara un toc.ncx que no está en el manifiesto')

    # De aquí saca Kindle la «posición de inicio de lectura»: dónde se abre el
    # libro la primera vez y dónde arranca la muestra gratuita. Si falta, KDP lo
    # avisa y el lector puede estrenar el libro en la página de créditos.
    arranque = None
    guia = opf.find('opf:guide', NS)
    if guia is None:
        mal('falta el <guide>: Kindle no sabrá dónde abrir el libro')
    else:
        refs = {r.get('type'): r.get('href') for r in guia.findall('opf:reference', NS)}
        arranque = refs.get('text')
        if not arranque:
            mal('el <guide> no trae reference type="text", que es la posición '
                'de inicio de lectura')
        for t, h in refs.items():
            if h and ruta_de(h.split('#')[0]) not in nombres:
                mal(f'el <guide> apunta a «{h}» ({t}), que no está en el zip')
        if arranque and ('creditos' in arranque or 'portadilla' in arranque
                         or 'indice' in arranque):
            ojo(f'el libro se abriría en «{arranque}»; debería abrirse en el '
                f'primer texto que se lee')

    # --- 3. cada documento, bien formado, y sus enlaces
    docs = [ruta_de(items[r]) for r in lomo if r in items]
    for i, h in items.items():
        d = ruta_de(h)
        if not d.endswith(('.xhtml', '.html')):
            continue
        try:
            arbol = ET.fromstring(z.read(d))
        except ET.ParseError as e:
            mal(f'{h} no es XML válido: {e}')
            continue
        for a in arbol.iter('{http://www.w3.org/1999/xhtml}a'):
            href = (a.get('href') or '').split('#')[0]
            if not href or '://' in href:
                continue
            if ruta_de(posixpath.join(posixpath.dirname(h), href)) not in nombres:
                mal(f'{h}: el enlace «{href}» no lleva a ninguna parte')
        for img in arbol.iter('{http://www.w3.org/1999/xhtml}img'):
            src = img.get('src') or ''
            if src and ruta_de(posixpath.join(posixpath.dirname(h), src)) not in nombres:
                mal(f'{h}: la imagen «{src}» no está')

    if ncx_id:
        ncx = ET.fromstring(z.read(ruta_de(items[ncx_id])))
        puntos = ncx.findall('.//ncx:navPoint', NS)
        if not puntos:
            mal('el toc.ncx no tiene ni un navPoint')
        for p in puntos:
            c = p.find('ncx:content', NS).get('src').split('#')[0]
            if ruta_de(c) not in nombres:
                mal(f'toc.ncx apunta a «{c}», que no está')

    # --- 4. lo que de verdad importa: que esté todo el texto
    fuentes = sorted(BASE.glob('[0-9]*.md'))
    total_md = total_ep = 0
    for f in fuentes:
        d = ruta_de(f.stem + '.xhtml')
        if d not in nombres:
            mal(f'falta en el EPUB la sección «{f.stem}»')
            continue
        pm = len(palabras(f.read_text()))
        pe = len(palabras(z.read(d).decode()))
        total_md += pm; total_ep += pe
        # el xhtml suma «Índice», títulos repetidos y poco más; un desvío
        # grande significa que se ha perdido un bloque por el camino
        if abs(pe - pm) > max(12, pm * 0.02):
            mal(f'{f.stem}: {pm} palabras en el manuscrito y {pe} en el EPUB')

    tablas_md = sum(1 for f in fuentes
                    for i, l in enumerate(f.read_text().split('\n'))
                    if re.match(r'^\s*\|[\s:|-]*-[\s:|-]*\|\s*$', l))
    tablas_ep = sum(z.read(d).decode().count('<table')
                    for d in docs if d.endswith('.xhtml'))
    if tablas_md != tablas_ep:
        mal(f'{tablas_md} tablas en el manuscrito y {tablas_ep} en el EPUB')

    h1_md = sum(1 for f in fuentes for l in f.read_text().split('\n')
                if re.match(r'^#\s+', l))
    h1_ep = sum(z.read(d).decode().count('<h1') for d in docs)
    if h1_ep < h1_md:
        mal(f'{h1_md} títulos de capítulo en el manuscrito y {h1_ep} en el EPUB')

    if total_md and abs(total_ep - total_md) > total_md * 0.01:
        ojo(f'{total_md} palabras en el manuscrito y {total_ep} en el EPUB')
    return dict(arranque=arranque, secciones=len(docs), palabras=total_ep, origen=total_md, tablas=tablas_ep,
                capitulos=h1_md, peso=pathlib.Path(ruta).stat().st_size)

def main():
    if len(sys.argv) < 2:
        sys.exit('uso: check_epub.py libro.epub')
    r = revisar(sys.argv[1])
    if r:
        print(f"{r['secciones']} secciones · {r['capitulos']} capítulos · "
              f"{r['palabras']:,} palabras (manuscrito: {r['origen']:,}) · "
              f"{r['tablas']} tablas · abre en {r['arranque']} · "
              f"{r['peso']/1024:.0f} KB".replace(',', '.'))
    for a in avisos: print('aviso  ' + a)
    for f in fallos: print('FALLO  ' + f)
    print(f"\n{len(fallos)} fallos, {len(avisos)} avisos")
    if not fallos:
        print('Estructura y contenido correctos. Falta pasarlo por Kindle '
              'Previewer, que es lo que reproduce la conversión de Amazon.')
    return 1 if fallos else 0

if __name__ == '__main__':
    sys.exit(main())
