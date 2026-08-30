#!/usr/bin/env python3
"""Construye el PDF del manuscrito con maqueta de libro (5,5 x 8,5 pulgadas, formato KDP)."""
import re, html, pathlib, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parents[2] / 'manuscrito'
OUT  = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('/tmp')
CHROME = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'

TITULO   = 'Nadie va a venir a elegirte'
SUBTITULO = 'Cómo se decide de verdad quién asciende — y cómo entrar en esa decisión'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'⟦AUTOR:\s*(.*?)⟧', r'<span class="nota nota-a"><b>AUTOR</b> \1</span>', t, flags=re.S)
    t = re.sub(r'⟦VERIFICAR:\s*(.*?)⟧', r'<span class="nota nota-v"><b>VERIFICAR</b> \1</span>', t, flags=re.S)
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', t)
    return t

def convert(md):
    lines, out, i, n = md.split('\n'), [], 0, len(md.split('\n'))
    primer_parrafo = True
    while i < n:
        ln = lines[i]
        if ln.startswith('>'):
            buf = []
            while i < n and lines[i].startswith('>'):
                buf.append(lines[i].lstrip('>').strip()); i += 1
            txt = ' '.join(buf)
            cls = 'gancho' if txt.startswith('GANCHO') else 'cita'
            txt = re.sub(r'^GANCHO\s*—\s*', '', txt)
            out.append(f'<div class="{cls}"><p>{inline(txt)}</p></div>')
            continue
        m = re.match(r'^(#{1,3})\s+(.*)$', ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                num, _, rest = txt.partition(' · ')
                if not rest: num, rest = '', txt
                out.append('<header class="capcab">'
                           + (f'<div class="capnum">{inline(num)}</div>' if num else '')
                           + f'<h1>{inline(rest)}</h1></header>')
                primer_parrafo = True
            else:
                out.append(f'<h2>{inline(txt)}</h2>')
                primer_parrafo = True
            i += 1; continue
        if ln.strip():
            buf = [ln.strip()]; i += 1
            while i < n and lines[i].strip() and not re.match(r'^\s*(#{1,3}\s|>)', lines[i]):
                buf.append(lines[i].strip()); i += 1
            cls = ' class="primero"' if primer_parrafo else ''
            primer_parrafo = False
            out.append(f'<p{cls}>{inline(" ".join(buf))}</p>')
            continue
        i += 1
    return '\n'.join(out)

files = sorted(BASE.glob('[0-9]*.md'))
caps = []
for f in files:
    src = f.read_text()
    caps.append(f'<section class="cap">{convert(src)}</section>')

CSS = r'''
@page { size: 5.5in 8.5in; margin: 0.72in 0.56in 0.68in 0.82in; }
@page :first { margin: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Bitstream Charter","Charter",Georgia,serif; font-size: 11.4pt;
       line-height: 1.62; color: #14181c; margin: 0; text-align: justify;
       hyphens: auto; -webkit-hyphens: auto; }
.cover { width: 5.5in; height: 8.5in; padding: 1.5in 0.7in 0.8in; background: #12474d;
         color: #eef4f5; page-break-after: always; display: flex; flex-direction: column; }
.cover .kick { font-family: "DejaVu Sans",sans-serif; font-size: 7pt; letter-spacing: .24em;
               text-transform: uppercase; color: #8fc3c6; margin-bottom: 1.1in; }
.cover h1 { font-size: 40pt; line-height: .95; letter-spacing: -.015em; margin: 0 0 .28in;
            font-weight: 700; text-align: left; hyphens: none; }
.cover .sub { font-size: 11pt; line-height: 1.35; color: #c9e0e2; text-align: left;
              border-top: 1px solid rgba(255,255,255,.28); padding-top: .18in; }
.cover .pie { margin-top: auto; font-family: "DejaVu Sans",sans-serif; font-size: 7.4pt;
              letter-spacing: .1em; text-transform: uppercase; color: #8fc3c6; }
.cap { page-break-before: always; }
.capcab { margin: 1.15in 0 .40in; text-align: left; }
.capnum { font-family: "DejaVu Sans",sans-serif; font-size: 7.6pt; letter-spacing: .2em;
          text-transform: uppercase; color: #9a6c22; margin-bottom: .1in; }
.capcab h1 { font-size: 23pt; line-height: 1.1; margin: 0; font-weight: 700;
             letter-spacing: -.01em; hyphens: none; }
.capcab h1::after { content: ""; display: block; width: .8in; height: 2px;
                    background: #12474d; margin-top: .13in; }
h2 { font-family: "DejaVu Sans",sans-serif; font-size: 10.2pt; font-weight: 700;
     letter-spacing: .02em; color: #12474d; margin: .30in 0 .11in; text-align: left;
     hyphens: none; page-break-after: avoid; }
p { margin: 0; text-indent: 1.1em; orphans: 2; widows: 2; }
p.primero { text-indent: 0; }
p.primero::first-letter { font-size: 1.06em; }
strong { font-weight: 700; }
.cita { margin: .16in 0; padding-left: .18in; border-left: 2px solid #c9d4d9; }
.cita p { text-indent: 0; font-style: italic; color: #33424c; }
.gancho { margin: .28in 0 0; padding: .13in .16in; background: #f1f5f6;
          border-top: 2px solid #12474d; page-break-inside: avoid; }
.gancho p { text-indent: 0; font-size: 10.4pt; line-height: 1.5; color: #21303a; }
.gancho p::before { content: "▸ "; color: #9a6c22; font-weight: 700; }
.nota { display: block; margin: .1in 0; padding: .09in .12in; background: #fdf6e6;
        border-left: 2px solid #9a6c22; font-family: "DejaVu Sans",sans-serif;
        font-size: 7.8pt; line-height: 1.35; color: #5a4413; text-align: left;
        text-indent: 0; hyphens: none; }
.nota b { letter-spacing: .1em; }
'''

doc = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{html.escape(TITULO)}</title><style>{CSS}</style></head><body>
<div class="cover">
  <div class="kick">Manuscrito · borrador completo</div>
  <h1>{html.escape(TITULO)}</h1>
  <div class="sub">{html.escape(SUBTITULO)}</div>
  <div class="pie">Prólogo · 14 capítulos · Epílogo</div>
</div>
{"".join(caps)}
</body></html>'''

OUT.mkdir(parents=True, exist_ok=True)
htmlp = OUT / 'manuscrito.html'
pdfp  = OUT / 'manuscrito-nadie-va-a-venir-a-elegirte.pdf'
htmlp.write_text(doc)
subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                '--no-pdf-header-footer', f'--print-to-pdf={pdfp}',
                f'file://{htmlp}'], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(pdfp, pdfp.stat().st_size, 'bytes')
