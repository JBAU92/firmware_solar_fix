#!/usr/bin/env python3
"""Huella de registro del manuscrito, capítulo a capítulo.

Para qué sirve: el libro mantiene un tono constante —directo, en segunda
persona, con frases cortas— y eso es lo primero que se pierde en una
traducción larga, sin que nadie lo note hasta que un lector dice que el
capítulo 11 «suena a otra persona».

Aquí se miden tres proxies groseros pero estables, y lo importante no es su
valor absoluto sino que la curva del libro traducido siga la del original:

  · 2ª persona   marcas de tuteo por cada 1.000 palabras
  · imperativos  verbos de orden por cada 1.000 palabras (lista cerrada)
  · frase        longitud media de frase en palabras

Advertencia honesta: las tres son aproximaciones. La lista de imperativos es
cerrada y se le escapan formas; la de segunda persona no distingue «tu» de
«tú». Sirven para ver una curva y detectar un capítulo que se sale, no para
puntuar prosa.

  registro.py                      la huella del original
  registro.py --comparar ../en     la del original y la de otra carpeta, al lado
"""
import re, sys, pathlib, statistics, argparse

BASE = pathlib.Path(__file__).resolve().parents[2] / 'manuscrito'

# Un paquete por lengua. Para traducir el libro se añade el suyo y se pasa
# --lengua. Si falta, el aviso lo dice en vez de medir con las palabras de otro
# idioma y dar una curva sin sentido.
LENGUAS = {
    'es': dict(
        p2=r'\b(tú|te|ti|tu|tus|tuyo|tuya|tuyos|tuyas|contigo)\b',
        imp=r'\b(mira|fíjate|piensa|coge|escribe|elige|apunta|vuelve|léelo|dile|'
            r'pide|haz|busca|prueba|ponle|ponte|empieza|termina|acuérdate|olvida|'
            r'deja|manda|pregunta|cuenta|suma|imagina|recuerda|léela|anota|marca)\b'),
    'en': dict(
        p2=r'\b(you|your|yours|yourself)\b',
        imp=r'\b(look|notice|think|take|write|choose|pick|go back|tell|ask|do|'
            r'find|try|put|start|finish|remember|forget|leave|send|count|add|'
            r'imagine|read|note|mark)\b'),
}

def huella(texto, pack):
    t = re.sub(r'^[#>|].*$', '', texto, flags=re.M)          # fuera títulos, citas y tablas
    pal = len(t.split()) or 1
    fr = [len(s.split()) for s in re.split(r'(?<=[.?!])\s', t) if s.split()]
    par = [len(p.split()) for p in re.split(r'\n\s*\n', t) if len(p.split()) > 4]
    return dict(
        palabras=pal,
        p2=1000 * len(re.findall(pack['p2'], t, re.I)) / pal,
        imp=1000 * len(re.findall(pack['imp'], t, re.I)) / pal,
        frase=statistics.mean(fr) if fr else 0,
        parrafo=statistics.mean(par) if par else 0)

def leer(carpeta, pack):
    out = {}
    for f in sorted(pathlib.Path(carpeta).glob('[0-9]*.md')):
        n = int(re.match(r'(\d+)', f.stem).group(1))
        out[n] = huella(f.read_text(), pack)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lengua', default='es')
    ap.add_argument('--comparar', help='carpeta con la traducción')
    ap.add_argument('--lengua-comparada', default='en')
    a = ap.parse_args()
    for k in (a.lengua, a.lengua_comparada if a.comparar else a.lengua):
        if k not in LENGUAS:
            print(f"no hay paquete de palabras para «{k}». Añádelo a LENGUAS "
                  f"antes de medir, o la curva no significará nada."); return 2

    orig = leer(BASE, LENGUAS[a.lengua])
    trad = leer(a.comparar, LENGUAS[a.lengua_comparada]) if a.comparar else {}

    cab = f"{'cap':<5}{'palabras':>9}{'2ª pers':>9}{'imperat':>9}{'frase':>8}{'párrafo':>9}"
    print(cab + ("      │ " + cab if trad else ""))
    print('-' * (len(cab) + (len(cab) + 8 if trad else 0)))
    dif = []
    for n, h in orig.items():
        fila = (f"{n:<5}{h['palabras']:>9}{h['p2']:>9.0f}{h['imp']:>9.1f}"
                f"{h['frase']:>8.1f}{h['parrafo']:>9.1f}")
        if trad:
            t = trad.get(n)
            if not t:
                fila += "      │  (falta el capítulo en la traducción)"
            else:
                fila += ("      │ " + f"{n:<5}{t['palabras']:>9}{t['p2']:>9.0f}"
                         f"{t['imp']:>9.1f}{t['frase']:>8.1f}{t['parrafo']:>9.1f}")
                for clave, tol, nom in (('p2', .40, '2ª persona'), ('imp', .50, 'imperativos'),
                                        ('frase', .25, 'longitud de frase')):
                    o, v = h[clave], t[clave]
                    if o and abs(v - o) / o > tol:
                        dif.append(f"  cap. {n}: {nom} {o:.1f} → {v:.1f} "
                                   f"({100*(v-o)/o:+.0f} %)")
        print(fila)
    if trad:
        print()
        print("Desvíos por encima de la tolerancia (2ª pers. 40 %, imperativos 50 %, "
              "frase 25 %):")
        print('\n'.join(dif) if dif else "  ninguno.")
        print("\nUn desvío no es un error: el inglés necesita más «you» que el "
              "castellano\ny las frases se acortan al traducir. Lo que importa es "
              "que el desvío sea\nparecido en todos los capítulos. Uno solo que se "
              "salga es el sospechoso.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
