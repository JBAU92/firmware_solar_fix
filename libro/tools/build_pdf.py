#!/usr/bin/env python3
"""Construye un PDF único a partir del dossier en markdown."""
import re, html, pathlib, sys

BASE = pathlib.Path('/home/user/firmware_solar_fix/libro')
OUT = pathlib.Path('/tmp/claude-0/-home-user-firmware-solar-fix/d54e8afc-d969-5329-905b-cb28cecb98fa/scratchpad')

ORDER = [
    ('README.md',                     'Ficha del proyecto'),
    ('01-concepto-y-propuesta.md',    'Concepto y propuesta editorial'),
    ('02-arquitectura-narrativa.md',  'Arquitectura narrativa'),
    ('03-esqueleto-capitulos.md',     'Esqueleto capítulo a capítulo'),
    ('04-bibliografia-y-evidencia.md','Bibliografía y base de evidencia'),
    ('05-casos-y-testimonios.md',     'Casos, contra-casos y testimonios'),
    ('06-enganche-del-lector.md',     'Cómo mantener al lector enganchado'),
    ('07-leccion-de-los-bestsellers.md','Ingeniería inversa de los bestsellers'),
    ('08-produccion-kdp.md',          'Validación, producción y KDP'),
    ('09-plan-de-trabajo.md',         'Plan de trabajo'),
    ('10-piezas-redactadas.md',       'Piezas ya redactadas'),
    ('11-expediente-de-promocion.md', 'El expediente de promoción'),
    ('12-sistema-de-promocion.md',    'La promoción como sistema'),
    ('13-influencia-y-defensa.md',    'Influencia real y defensa'),
]

# ---------------------------------------------------------------- inline
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    # enlaces
    def link(m):
        txt, href = m.group(1), m.group(2)
        if '.md' in href and not href.startswith('http'):
            import re as _re
            if _re.fullmatch(r'\d{2}', txt.strip()):
                return f'<em>secci\u00f3n {txt.strip()}</em>'
            return f'<em>{txt}</em>'
        return f'<a href="{html.escape(href, quote=True)}">{txt}</a>'
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, t)
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', t)
    return t

def cell_align(sep):
    a = []
    for c in sep:
        c = c.strip()
        if c.startswith(':') and c.endswith(':'): a.append('center')
        elif c.endswith(':'): a.append('right')
        else: a.append('left')
    return a

def split_row(line):
    line = line.strip()
    if line.startswith('|'): line = line[1:]
    if line.endswith('|'): line = line[:-1]
    return [c.strip() for c in line.split('|')]

# ---------------------------------------------------------------- blocks
def convert(md, sec_id):
    lines = md.split('\n')
    out, i, n = [], 0, len(lines)
    list_stack = []

    def close_lists():
        while list_stack:
            out.append('</ul>' if list_stack.pop() == 'ul' else '</ol>')

    while i < n:
        ln = lines[i]

        # código
        if ln.strip().startswith('```'):
            close_lists(); i += 1
            buf = []
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(html.escape(lines[i])); i += 1
            i += 1
            out.append('<pre>' + '\n'.join(buf) + '</pre>')
            continue

        # tabla
        if ln.strip().startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i+1]):
            close_lists()
            head = split_row(ln)
            align = cell_align(split_row(lines[i+1]))
            i += 2
            body = []
            while i < n and lines[i].strip().startswith('|'):
                body.append(split_row(lines[i])); i += 1
            wide = ' class="wide"' if len(head) >= 5 else ''
            t = [f'<div class="tw"><table{wide}><thead><tr>']
            for k, h in enumerate(head):
                al = align[k] if k < len(align) else 'left'
                t.append(f'<th style="text-align:{al}">{inline(h)}</th>')
            t.append('</tr></thead><tbody>')
            for row in body:
                t.append('<tr>')
                for k, c in enumerate(row):
                    al = align[k] if k < len(align) else 'left'
                    t.append(f'<td style="text-align:{al}">{inline(c)}</td>')
                t.append('</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            continue

        # cita
        if ln.startswith('>'):
            close_lists()
            buf = []
            while i < n and lines[i].startswith('>'):
                buf.append(lines[i][1:].lstrip()); i += 1
            paras = '\n'.join(buf).split('\n\n')
            out.append('<blockquote>' + ''.join(
                f'<p>{inline(" ".join(p.split()))}</p>' for p in paras if p.strip()) + '</blockquote>')
            continue

        # regla
        if re.match(r'^\s*---+\s*$', ln):
            close_lists(); out.append('<hr>'); i += 1; continue

        # encabezados
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            close_lists()
            lvl, txt = len(m.group(1)), m.group(2).strip()
            hid = f'{sec_id}-h{i}'
            out.append(f'<h{lvl+1} id="{hid}">{inline(txt)}</h{lvl+1}>')
            i += 1; continue

        # listas
        m = re.match(r'^(\s*)([-*])\s+(.*)$', ln)
        mo = re.match(r'^(\s*)(\d+)\.\s+(.*)$', ln)
        if m or mo:
            ordered = mo is not None
            g = mo if ordered else m
            indent, txt = len(g.group(1)), g.group(3)
            want = 'ol' if ordered else 'ul'
            depth = 1 + (indent // 2 if indent else 0)
            while len(list_stack) > depth:
                out.append('</ul>' if list_stack.pop() == 'ul' else '</ol>')
            if len(list_stack) < depth:
                out.append(f'<{want}>'); list_stack.append(want)
            elif list_stack and list_stack[-1] != want:
                out.append('</ul>' if list_stack.pop() == 'ul' else '</ol>')
                out.append(f'<{want}>'); list_stack.append(want)
            cls = ''
            if txt.startswith('[ ] '):
                txt, cls = txt[4:], ' class="chk"'
            elif txt.startswith('[x] ') or txt.startswith('[X] '):
                txt, cls = txt[4:], ' class="chk done"'
            # continuación indentada
            i += 1
            cont = []
            while i < n and lines[i].strip() and not re.match(r'^\s*([-*]|\d+\.)\s', lines[i]) \
                  and not lines[i].startswith('#') and not lines[i].strip().startswith('|') \
                  and lines[i].startswith(' '):
                cont.append(lines[i].strip()); i += 1
            full = txt + (' ' + ' '.join(cont) if cont else '')
            out.append(f'<li{cls}>{inline(full)}</li>')
            continue

        # párrafo
        if ln.strip():
            close_lists()
            buf = [ln.strip()]
            i += 1
            while i < n and lines[i].strip() and not re.match(
                    r'^\s*(#{1,4}\s|[-*]\s|\d+\.\s|\||>|```|---+\s*$)', lines[i]):
                buf.append(lines[i].strip()); i += 1
            out.append(f'<p>{inline(" ".join(buf))}</p>')
            continue

        i += 1

    close_lists()
    return '\n'.join(out)

# ---------------------------------------------------------------- ensamblado
sections, toc = [], []
for idx, (fn, title) in enumerate(ORDER, start=0):
    src = (BASE / fn).read_text()
    # quitar el primer H1 (lo ponemos nosotros como cabecera de sección)
    src = re.sub(r'^#\s+.*\n', '', src, count=1)
    sec_id = f's{idx}'
    num = '—' if idx == 0 else f'{idx:02d}'
    body = convert(src, sec_id)
    sections.append(f'''
<section class="doc" id="{sec_id}">
  <header class="dochead"><span class="docnum">{num}</span><h1>{html.escape(title)}</h1></header>
  {body}
</section>''')
    toc.append((num, title, sec_id))

toc_html = '\n'.join(
    f'<li><span class="tnum">{n}</span><a href="#{i}">{html.escape(t)}</a></li>' for n, t, i in toc)

CSS = r'''
@page {
  size: A4;
  margin: 20mm 18mm 18mm 18mm;
}
@page :first { margin: 0; }

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Bitstream Charter", "Charter", Georgia, serif;
  font-size: 9.6pt;
  line-height: 1.5;
  color: #16212a;
  margin: 0;
}
:root{
  --teal:#0d565d;
  --brass:#9a6c22;
  --rule:#c9d4d9;
  --rulesoft:#e0e8ec;
  --muted:#5b6f7b;
  --tint:#f2f6f7;
}

/* ---------- portada ---------- */
.cover {
  height: 297mm; width: 210mm;
  padding: 34mm 24mm 20mm;
  display: flex; flex-direction: column;
  background: #0d565d; color: #eef5f6;
  page-break-after: always;
}
.cover .kicker {
  font-family: "DejaVu Sans", sans-serif;
  font-size: 7.6pt; letter-spacing: .22em; text-transform: uppercase;
  color: #9fd0d2; margin-bottom: 26mm;
}
.cover h1 {
  font-size: 74pt; line-height: .88; letter-spacing: -.02em;
  margin: 0; font-weight: 700; color: #fff;
}
.cover .sub {
  font-size: 15pt; line-height: 1.3; font-style: italic;
  margin-top: 9mm; max-width: 118mm; color: #cfe6e7;
}
.cover .rule { height: 2px; background: #9a6c22; margin: 12mm 0 8mm; width: 42mm; }
.cover .facts {
  font-family: "DejaVu Sans", sans-serif; font-size: 8.4pt; line-height: 1.85;
  color: #cfe6e7;
}
.cover .facts b { color: #fff; font-weight: 600; }
.cover .foot {
  margin-top: auto;
  font-family: "DejaVu Sans", sans-serif; font-size: 7.6pt;
  letter-spacing: .1em; text-transform: uppercase; color: #8fc3c6;
  border-top: 1px solid #1d6a71; padding-top: 5mm;
  display: flex; justify-content: space-between;
}

/* ---------- índice ---------- */
.toc { page-break-after: always; padding-top: 4mm; }
.toc h2 {
  font-family: "DejaVu Sans", sans-serif; font-size: 8pt; letter-spacing: .2em;
  text-transform: uppercase; color: var(--muted); font-weight: 500;
  border-bottom: 1.5px solid #16212a; padding-bottom: 3mm; margin: 0 0 7mm;
}
.toc ol { list-style: none; margin: 0; padding: 0; }
.toc li {
  display: flex; gap: 8mm; align-items: baseline;
  padding: 2.6mm 0; border-bottom: 1px solid var(--rulesoft);
  font-size: 11.5pt;
}
.toc .tnum {
  font-family: "DejaVu Sans Mono", monospace; font-size: 8pt;
  color: var(--brass); min-width: 8mm;
}
.toc a { color: #16212a; text-decoration: none; }
.verdict {
  margin: 9mm 0 0; padding: 6mm 7mm;
  border-left: 3px solid var(--brass); background: #faf6ef;
}
.verdict .lbl {
  font-family: "DejaVu Sans", sans-serif; font-size: 7.4pt; letter-spacing: .18em;
  text-transform: uppercase; color: var(--brass); display: block; margin-bottom: 2.5mm;
}
.verdict p { margin: 0 0 2.5mm; font-size: 10pt; }
.verdict p:last-child { margin-bottom: 0; }

/* ---------- secciones ---------- */
.doc { page-break-before: always; }
.dochead {
  border-bottom: 1.5px solid #16212a; padding-bottom: 3.5mm; margin-bottom: 7mm;
  display: flex; align-items: baseline; gap: 6mm;
}
.docnum {
  font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; color: var(--brass);
}
.dochead h1 {
  font-size: 21pt; margin: 0; letter-spacing: -.015em; line-height: 1.1; font-weight: 700;
}

h2, h3, h4, h5 { page-break-after: avoid; letter-spacing: -.01em; }
h2 { font-size: 14.5pt; margin: 8mm 0 2.5mm; line-height: 1.18; }
h3 { font-size: 11.6pt; margin: 6mm 0 2mm; color: var(--teal); }
h4 { font-size: 10pt; margin: 4.5mm 0 1.5mm; }
h5 { font-size: 9.4pt; margin: 4mm 0 1.5mm; font-style: italic; }
p { margin: 0 0 2.6mm; orphans: 2; widows: 2; }
strong { font-weight: 700; }
a { color: var(--teal); text-decoration: none; border-bottom: .4pt solid #a8c6c9; }
hr { border: none; border-top: 1px solid var(--rule); margin: 7mm 0; }
code {
  font-family: "DejaVu Sans Mono", monospace; font-size: .82em;
  background: var(--tint); padding: .5mm 1mm; border-radius: 1pt;
}
pre {
  font-family: "DejaVu Sans Mono", monospace; font-size: 7.4pt; line-height: 1.45;
  background: var(--tint); border: 1px solid var(--rulesoft); border-radius: 2pt;
  padding: 3.5mm 4mm; overflow-wrap: break-word; white-space: pre-wrap;
  page-break-inside: avoid; margin: 3mm 0;
}
blockquote {
  margin: 4mm 0; padding: 4mm 5mm;
  border-left: 2.5px solid var(--brass); background: #faf7f2;
  page-break-inside: avoid;
}
blockquote p { margin: 0 0 2mm; font-size: 10pt; }
blockquote p:last-child { margin: 0; }

ul, ol { margin: 0 0 3mm; padding-left: 5.5mm; }
li { margin-bottom: 1.2mm; }
li.chk { list-style: none; margin-left: -4mm; }
li.chk::before { content: "☐  "; color: var(--muted); }

/* ---------- tablas ---------- */
.tw { margin: 3.5mm 0 5mm; }
table {
  width: 100%; border-collapse: collapse;
  font-family: "DejaVu Sans", sans-serif; font-size: 7.7pt; line-height: 1.4;
}
table.wide { font-size: 6.9pt; }
thead { display: table-header-group; }
th {
  text-align: left; font-weight: 600; font-size: 6.9pt;
  letter-spacing: .06em; text-transform: uppercase; color: var(--muted);
  border-bottom: 1.2px solid #16212a; padding: 1.8mm 2mm; vertical-align: bottom;
}
td { padding: 1.8mm 2mm; border-bottom: .5px solid var(--rulesoft); vertical-align: top; }
tr { page-break-inside: avoid; }
tbody tr:nth-child(even) { background: #f7fafb; }
'''

doc = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>ESCALA — Estudio de preproducción</title>
<style>{CSS}</style></head><body>

<div class="cover">
  <div class="kicker">Estudio de preproducción · Amazon KDP · v3.1</div>
  <h1>ESCALA</h1>
  <div class="sub">El plan de carrera que tu empresa diseña para unos pocos, traducido para cualquier trabajador</div>
  <div class="rule"></div>
  <div class="facts">
    Método <b>Elige · Sitúate · Construye · Amplifica · Lidera · Asegura</b><br>
    Extensión objetivo <b>57.000–62.000 palabras</b> · ~250 páginas · nº de capítulos a decidir por prueba<br>
    Entregable del lector <b>Un expediente de promoción de 14 páginas</b><br>
    Mercado <b>Amazon.es</b> · eBook Kindle y tapa blanda
  </div>
  <div class="foot"><span>Documento de trabajo — no es el manuscrito</span><span>30 de agosto de 2026</span></div>
</div>

<div class="toc">
  <h2>Contenido</h2>
  <ol>{toc_html}</ol>
  <div class="verdict">
    <span class="lbl">Veredicto editorial</span>
    <p><strong>Validar antes de escribir.</strong> La promesa es útil y diferenciable, pero dos
    puertas siguen cerradas: la demanda real en español no está medida y la autoridad del autor no
    está verificada. Ninguna idea buena compensa esas dos cosas.</p>
    <p>Siguiente hito: un sprint de validación de 3–4 semanas —mercado, credencial, 15 lectores y
    8 entrevistas de recursos humanos—. Solo después, dos capítulos prototipo. El manuscrito
    completo, más tarde.</p>
  </div>
</div>

{''.join(sections)}
</body></html>'''

(OUT / 'pdf-source.html').write_text(doc)
print(f'HTML generado: {len(doc):,} bytes · {len(sections)} secciones')
