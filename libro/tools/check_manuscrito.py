#!/usr/bin/env python3
"""Verificador del manuscrito. Comprueba las nueve trampas del archivo 00-reglas."""
import re, sys, pathlib, collections

BASE = pathlib.Path(__file__).resolve().parents[2] / 'manuscrito'
SECTOR = {0:'— prólogo —',1:'oficina',2:'tecnico',3:'oficina',4:'ventas',5:'libre',
          6:'restauracion',7:'logistica',8:'industria',9:'juridico',10:'retail',11:'oficina',
          12:'sanidad',13:'retail/industria',14:'oficina',15:'— epílogo —',
          16:'— fuentes —'}
# piezas de marco: objetivo propio, mucho más corto que un capítulo
MARCO = {0:(600,1000), 15:(600,1000), 16:(1200,2200)}
REVELACION = {1,6,8,10,11,12,14}
NEGRAS = ['Gino','Ariely','power posing','postura de poder','10.000 horas','diez mil horas',
          '93 %','93%','Mehrabian','70-20-10','uno de cada siete','1 de cada 7','siete segundos']
MULETAS = ['podría ser','en cierto modo','de alguna manera','hasta cierto punto','por lo general',
           'en general','quizás','tal vez','probablemente','suele ser','tiende a']
SERMON = ['es importante recordar','debemos ','hay que ser consciente','no olvidemos','conviene recordar']

def bloques_escena(t):
    out=[]
    for m in re.finditer(r'^> .*$(\n^> .*$)*', t, re.M):
        out.append((m.start(), m.group(0)))
    return out

def check(path):
    n = int(re.match(r'(\d+)', path.stem).group(1)) if re.match(r'\d+', path.stem) else 0
    t = path.read_text()
    cuerpo = re.sub(r'⟦[^⟧]*⟧','',t)
    palabras = len(re.findall(r"[\wáéíóúñü']+", cuerpo))
    errs, warns = [], []

    # 1 · cifras inventadas en escena
    for pos, blk in bloques_escena(cuerpo):
        for m in re.finditer(r'\b\d+([.,]\d+)?\s*(%|por ciento|euros|€)?', blk):
            tok = m.group(0).strip()
            if re.fullmatch(r'(19|20)\d\d', tok): continue          # años, permitidos
            if tok in ('1','2','3','4','5','6','7','8','9','10','12','15','20','30','40','50','100'):
                warns.append(f"cifra en escena: «{tok}» — ¿viene de fuente?")
            else:
                errs.append(f"CIFRA EN ESCENA: «{tok}» — prohibido salvo fuente citada")

    # 2 · citas de la lista negra
    # El apartado de fuentes (16) las nombra a propósito, para decir que NO se han usado.
    for neg in ([] if n == 16 else NEGRAS):
        if re.search(re.escape(neg), cuerpo, re.I):
            errs.append(f"LISTA NEGRA: «{neg}»")

    # 3 · muletillas
    mul = sum(len(re.findall(r'\b'+re.escape(m), cuerpo, re.I)) for m in MULETAS)
    dens = 1000*mul/max(palabras,1)
    if dens > 6: errs.append(f"MULETILLAS: {mul} ({dens:.1f}/1000 palabras, máx 6)")
    elif dens > 4: warns.append(f"muletillas altas: {dens:.1f}/1000")

    # 4 · sermón
    for sp in SERMON:
        if re.search(re.escape(sp), cuerpo, re.I): errs.append(f"SERMÓN: «{sp}»")

    # 5 · hilo narrativo
    if n in REVELACION and not re.search(r'Marta|Javier', cuerpo):
        errs.append("HILO: capítulo con revelación asignada y sin Marta ni Javier")

    # 6 · extensión
    if n in MARCO:
        lo, hi = MARCO[n]
        if not (lo <= palabras <= hi):
            warns.append(f"EXTENSIÓN: {palabras} palabras (objetivo {lo}–{hi})")
    elif n and not (1900 <= palabras <= 2600):
        (errs if (palabras>2900 or palabras<1500) else warns).append(
            f"EXTENSIÓN: {palabras} palabras (objetivo 2.000–2.500)")

    # 8 · cadencia de máquina — las piezas de marco no exigen párrafo largo

    noesx = len(re.findall(r'\bno es\b[^.]{1,60}\bes\b', cuerpo, re.I))
    if noesx > 2: errs.append(f"CADENCIA: «no es… es» {noesx} veces (máx 2)")
    rayas = len(re.findall(r'—', cuerpo))
    if 1000*rayas/max(palabras,1) > 14: warns.append(f"rayas: {1000*rayas/max(palabras,1):.0f}/1000")
    parras = [len(p.split()) for p in re.split(r'\n\s*\n', cuerpo) if len(p.split())>4 and not p.startswith(('|','#','>'))]
    if parras and not any(p<=25 for p in parras): warns.append("sin párrafo corto")
    if parras and n not in MARCO and not any(p>=90 for p in parras):
        warns.append("sin párrafo largo")

    # 9 · gancho
    if n and n < 14 and '> GANCHO' not in t:
        errs.append("GANCHO: falta el bloque «> GANCHO» final")

    return n, palabras, errs, warns

def main():
    files = sorted(BASE.glob('[0-9]*.md'))
    if not files: print("sin capítulos todavía"); return 0
    total=0; fallos=0
    print(f"{'cap':<5}{'palabras':>9}  {'sector':<16}estado")
    print("-"*78)
    for f in files:
        n, pal, errs, warns = check(f)
        total += pal; fallos += len(errs)
        est = "OK" if not errs else f"{len(errs)} FALLO(S)"
        print(f"{n:<5}{pal:>9}  {SECTOR.get(n,'—'):<16}{est}")
        for e in errs:  print(f"       ✗ {e}")
        for w in warns: print(f"       · {w}")
    print("-"*78)
    cuerpo = total - sum(check(f)[1] for f in files if int(re.match(r'(\d+)', f.stem).group(1)) in MARCO)
    print(f"total: {total:,} palabras · cuerpo (caps. 1–14): {cuerpo:,} · objetivo ~30.800 · "
          f"fallos: {fallos}")
    return 1 if fallos else 0

if __name__ == '__main__':
    sys.exit(main())
