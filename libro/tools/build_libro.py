#!/usr/bin/env python3
"""Compone el interior del libro para KDP con Typst.

Genera un .typ desde el manuscrito en markdown y lo compila. Typst se encarga
de lo que antes se hacía a mano: guionado en español, aperturas a página impar,
folios, titulillos, índice con números de página y fuentes incrustadas.

Uso:  build_libro.py <directorio_de_salida>
"""
import re, pathlib, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parents[2] / 'manuscrito'
OUT  = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp')

TITULO    = 'Nadie va a venir a elegirte'
SUBTITULO = 'Cómo se decide de verdad quién asciende, y cómo entrar en esa decisión'
AUTOR     = 'NOMBRE DEL AUTOR'
ANIO      = '2026'

# --------------------------------------------------------------- md → typst
NEG, NEGF, CUR, CURF = '\x01', '\x02', '\x03', '\x04'

def texto(s):
    s = re.sub(r'\*\*\*(.+?)\*\*\*', NEG + CUR + r'\1' + CURF + NEGF, s)
    s = re.sub(r'\*\*(.+?)\*\*', NEG + r'\1' + NEGF, s)
    s = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', CUR + r'\1' + CURF, s)
    for c in '\\#$[]<>@*_`':
        s = s.replace(c, '\\' + c)
    return (s.replace(NEG, '*').replace(NEGF, '*')
             .replace(CUR, '_').replace(CURF, '_'))

def convertir(md):
    lineas = md.split('\n'); out = []; i = 0; n = len(lineas)
    while i < n:
        ln = lineas[i]
        if ln.startswith('>'):
            buf = []
            while i < n and lineas[i].startswith('>'):
                buf.append(lineas[i].lstrip('>').strip()); i += 1
            t = ' '.join(buf)
            fn = 'gancho' if t.startswith('GANCHO') else 'cita'
            t = re.sub(r'^GANCHO\s*—\s*', '', t)
            out.append('#%s[%s]\n' % (fn, texto(t)))
            continue
        if re.match(r'^\s*---+\s*$', ln):
            out.append('#filete()\n'); i += 1; continue
        if ln.strip().startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lineas[i+1]):
            celdas = lambda s: [c.strip() for c in s.strip().strip('|').split('|')]
            cab = celdas(ln); i += 2; filas = []
            while i < n and lineas[i].strip().startswith('|'):
                filas.append(celdas(lineas[i])); i += 1
            fmt = lambda fs: '(' + ', '.join('[%s]' % texto(c) for c in fs) + ',)'
            # una tabla con la mayoría de casillas vacías es un formulario:
            # se dibuja con cuadrícula para que se vea dónde escribir
            cel = [c for f in filas for c in f[1:]]
            form = 'true' if cel and sum(1 for c in cel if not c) * 2 > len(cel) else 'false'
            out.append('#tabla(%s, (%s), formulario: %s)\n'
                       % (fmt(cab), ' '.join(fmt(f) + ',' for f in filas), form))
            continue
        m = re.match(r'^(#{1,3})\s+(.*)$', ln)
        if m:
            lvl, t = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                num, _, rest = t.partition(' · ')
                if not rest: num, rest = '', t
                out.append(f'#cap("{texto(num)}")[{texto(rest)}]\n')
            else:
                out.append(f'== {texto(t)}\n')
            i += 1; continue
        if ln.strip():
            buf = [ln.strip()]; i += 1
            while i < n and lineas[i].strip() and not re.match(r'^\s*(#{1,3}\s|>|---+\s*$)', lineas[i]):
                buf.append(lineas[i].strip()); i += 1
            out.append(texto(' '.join(buf)) + '\n')
            continue
        i += 1
    return '\n'.join(out)

cuerpo = '\n'.join(convertir(f.read_text()) + '\n#metadata(none) <finsec>\n'
                   for f in sorted(BASE.glob('[0-9]*.md')))

PLANTILLA = r'''
#let TITULO    = "%(titulo)s"
#let SUBTITULO = "%(subtitulo)s"
#let AUTOR     = "%(autor)s"
#let ANIO      = "%(anio)s"

#let numcap = state("numcap", "")

// `pagebreak(to: "odd")` deja una par en blanco antes de cada capítulo. Esa
// página tiene que ir sin folio ni titulillo. Se reconoce porque no lleva la
// marca <finsec> —que va al final de cada sección— y la siguiente abre capítulo.
#let cortesia(p) = {
  let abre = query(heading.where(level: 1)).map(h => h.location().page())
  let fines = query(<finsec>).map(m => m.location().page())
  (not abre.contains(p)) and abre.contains(p + 1) and (not fines.contains(p))
}
// La primera página del prólogo es el folio 1; todo lo anterior va sin numerar.
#let pag-inicio() = {
  let caps = query(heading.where(level: 1))
  if caps.len() > 0 { caps.first().location().page() } else { 0 }
}

// ------------------------------------------------------------------ página
#set page(
  width: 5.5in, height: 8.5in, binding: left,
  margin: (inside: 0.80in, outside: 0.55in, top: 0.72in, bottom: 0.72in),
  header: context {
    let p = here().page()
    let abre = query(heading.where(level: 1)).any(h => h.location().page() == p)
    let ini = pag-inicio()
    if abre or cortesia(p) or ini == 0 or p < ini { return }
    let f = counter(page).at(here()).first()
    let previos = query(heading.where(level: 1).before(here()))
    let cap = if previos.len() > 0 { previos.last().body } else { TITULO }
    set text(size: 8pt, tracking: 0.9pt)
    if calc.even(p) {
      grid(columns: (auto, 1fr), [#f], align(right, upper(TITULO)))
    } else {
      grid(columns: (1fr, auto), upper(cap), [#f])
    }
  },
  footer: context {
    let p = here().page()
    let abre = query(heading.where(level: 1)).any(h => h.location().page() == p)
    let ini = pag-inicio()
    if not abre or ini == 0 or p < ini { return }
    set text(size: 8.6pt)
    align(center)[#counter(page).at(here()).first()]
  },
)

// -------------------------------------------------------------- tipografía
#set text(lang: "es", font: "Source Serif 4", size: 10.6pt, hyphenate: true)
#set par(justify: true, leading: 0.76em, spacing: 0.76em, first-line-indent: 1.15em)
#show par: set block(below: 0.76em)

#show heading.where(level: 1): it => {
  pagebreak(to: "odd", weak: true)
  v(0.95in)
  context {
    let n = numcap.get()
    if n != "" {
      block(below: 0.12in)[#text(size: 8.4pt, tracking: 1.7pt, fill: luma(45))[#upper(n)]]
    }
  }
  block(below: 0.40in)[
    #set text(size: 20pt, weight: 700, hyphenate: false)
    #set par(justify: false, leading: 0.42em, first-line-indent: 0pt)
    #it.body
    #v(0.14in, weak: true)
    #line(length: 0.62in, stroke: 1.5pt)
  ]
}
#show heading.where(level: 2): it => block(above: 0.30in, below: 0.13in)[
  #set text(size: 10.4pt, weight: 700, hyphenate: false)
  #set par(justify: false, first-line-indent: 0pt)
  #it.body
]

#let cap(num, cuerpo) = { numcap.update(num); heading(level: 1, cuerpo) }
// Tabla de libro: filetes horizontales y nada más. La primera columna a la
// izquierda, el resto centradas, que es como se leen las casillas de puntuar.
#let tabla(cab, filas, formulario: false) = block(
    above: 0.20in, below: 0.24in, breakable: false)[
  #set text(size: 9pt, hyphenate: false)
  #set par(justify: false, first-line-indent: 0pt, leading: 0.52em)
  #table(
    columns: (auto,) + (1fr,) * (cab.len() - 1),
    stroke: if formulario { 0.4pt + luma(150) } else { none },
    inset: (x: 4pt, y: if formulario { 10pt } else { 5.5pt }),
    align: (c, r) => if c == 0 { left + horizon } else { center + horizon },
    table.hline(stroke: 1.1pt),
    ..cab.map(c => strong(c)),
    table.hline(stroke: if formulario { 0.9pt } else { 0.5pt }),
    ..filas.flatten(),
    table.hline(stroke: 1.1pt),
  )
]
#let filete() = align(center, block(above: 0.22in, below: 0.22in,
  text(size: 10pt, tracking: 4pt, fill: luma(60))[§]))
#let cita(c) = block(above: 0.17in, below: 0.17in, inset: (left: 0.28in))[
  #set text(style: "italic"); #set par(first-line-indent: 0pt); #c]
#let gancho(c) = block(width: 100%%, above: 0.28in, breakable: false,
  stroke: (top: 1.3pt + black), inset: (top: 0.13in))[
  #set text(size: 10.1pt, style: "italic")
  #set par(first-line-indent: 0pt, leading: 0.70em); #c]

// ---------------------------------------------------------- preliminares
#set page(numbering: none)
#counter(page).update(1)

#align(center)[#v(2.5in) #text(size: 14pt, tracking: 2.4pt)[#upper(TITULO)]]
#pagebreak(to: "odd")
#align(center)[
  #v(1.8in)
  #text(size: 29pt, weight: 700)[#TITULO]
  #v(0.22in)
  #block(width: 3.5in)[#set par(justify: false, first-line-indent: 0pt)
    #text(size: 11.5pt, style: "italic")[#SUBTITULO]]
  #v(0.85in)
  #text(size: 11pt, tracking: 2.2pt)[#upper(AUTOR)]
]
#pagebreak()
#v(3.1in)
#block[
  #set text(size: 8.4pt, hyphenate: false)
  #set par(justify: false, first-line-indent: 0pt, leading: 0.62em, spacing: 0.62em)
  #TITULO \
  © #ANIO, #AUTOR \
  Primera edición, #ANIO. \
  ISBN:
  #v(0.14in)
  Reservados todos los derechos. Queda prohibida la reproducción total o parcial de esta
  obra, por cualquier medio o procedimiento, sin la autorización escrita del titular de los
  derechos.
  #v(0.10in)
  Los nombres de las personas que aparecen en los ejemplos y las situaciones descritas han
  sido modificados. Cualquier parecido con personas concretas es casual.
  #v(0.10in)
  Esta obra tiene una finalidad divulgativa y no constituye asesoramiento jurídico, laboral
  ni profesional de ningún tipo. Las decisiones que el lector tome a partir de su lectura
  son de su exclusiva responsabilidad. Para cuestiones legales o laborales conviene acudir
  a un profesional cualificado.
]

#pagebreak(to: "odd")
#align(center)[#text(size: 12.5pt, tracking: 2.4pt)[#upper("Índice")]]
#v(0.30in)
#show outline.entry: it => context {
  let n = numcap.at(it.element.location())
  set text(size: 9.8pt, hyphenate: false)
  block(below: 0.105in)[
    #grid(columns: (0.50in, 1fr, auto), column-gutter: 0.10in,
      align(right)[#text(fill: luma(50))[#n]],
      box(width: 100%%)[#it.element.body #box(width: 1fr,
        repeat(text(fill: luma(120))[.\u{2009}]))],
      align(right)[#it.page()])
  ]
}
#outline(title: none, depth: 1)

// ------------------------------------------------------------------ cuerpo
#pagebreak(to: "odd")
#counter(page).update(1)

%(cuerpo)s
'''

OUT.mkdir(parents=True, exist_ok=True)
typ = OUT / 'libro.typ'
typ.write_text(PLANTILLA % dict(titulo=TITULO, subtitulo=SUBTITULO, autor=AUTOR,
                                anio=ANIO, cuerpo=cuerpo))
pdf = OUT / 'interior-nadie-va-a-venir-a-elegirte.pdf'
r = subprocess.run(['typst', 'compile', '--font-path', str(pathlib.Path.home() / '.fonts'),
                    str(typ), str(pdf)], capture_output=True, text=True)
if r.returncode:
    print(r.stderr[:4000]); sys.exit(1)
print('→', pdf, '·', round(pdf.stat().st_size / 1048576, 2), 'MB')
