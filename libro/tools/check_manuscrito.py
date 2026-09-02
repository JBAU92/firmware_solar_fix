#!/usr/bin/env python3
"""Verificador del manuscrito. Comprueba las nueve trampas del archivo 00-reglas."""
import re, sys, pathlib, collections, unicodedata
from itertools import combinations

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

# El libro tiene dos tríadas distintas y es fácil mezclarlas, porque «capacidad»
# está en las dos. Ya pasó una vez: el capítulo 12 remitía a «los tres criterios»
# del 1 y los glosaba como «que puedas, que haya sitio y que quieras», que es un
# híbrido de las dos y no existe en ninguna parte.
#   · cap. 1 · los tres CRITERIOS  → la persona:  capacidad · aspiración · compromiso
#   · cap. 4 · las tres PUERTAS    → la situación: capacidad demostrada · oportunidad · patrocinio
# Porcentajes redondos escritos con letra: la forma clásica de la estadística
# inventada. Se colaron dos —«el noventa y nueve por ciento de los casos»— pese
# a la regla 1, porque la regla solo miraba dígitos.
PORCENTAJES_FALSOS = ['noventa y nueve por ciento', 'noventa por ciento',
                      'ochenta por ciento', 'setenta por ciento',
                      'nueve de cada diez', 'ocho de cada diez']
# Universales que suenan a dato y no lo son. Aviso, no error: alguno es voz.
# Se escriben como expresión regular para poder excluir la versión ya matizada:
# «casi nadie lo hace» está bien, «nadie lo hace» no.
ABSOLUTOS = [r'(?<!casi )nadie dice que no', r'nadie ha perdido nunca', r'nunca falla',
             r'(?<!casi )cualquier jefe tiene', r'en todas las empresas',
             r'siempre funciona', r'(?<!casi )todo el mundo lo hace',
             r'(?<!casi )nadie lo hace']

# Densidad de cantidades en la apertura de un capítulo. La primera página del
# libro llegó a tener trece: «ocho nombres y una hora, lo que sale a poco más de
# cinco minutos por persona» le pedía al lector hacer una división en la página
# que tiene que engancharlo. «un/una/uno» se excluyen: en español son artículos.
CANTIDAD = (r'\b(dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|'
            r'catorce|veinte|treinta|cuarenta|cincuenta|cien|mitad|\d+)\b')
ARITMETICA = ['lo que sale a', 'lo que da un', 'es decir, un ', 'lo que supone']

# El recuento de las siete cosas. Los capítulos 6 a 12 ponen una cada uno y
# llevan la cuenta: hay que comprobar que el ordinal y las que quedan cuadran.
# Se rompió una vez —el cap. 6 contaba la base más la primera («tiene tres»)
# y el 12 contaba solo las siete— y nadie lo vio hasta que un lector sumó.
CUENTA = {6: ('primera', 'seis'), 7: ('segunda', 'cinco'), 8: ('tercera', 'cuatro'),
          9: ('cuarta', 'tres'), 10: ('quinta', 'dos'), 11: ('sexta', 'una')}
# Javier puso cinco de las siete; Marta, ninguna. En todo el libro.
REPARTO = [(r'Javier\s+(?:puso|hizo)\s+(\w+)', 'Javier', {'cinco'}),
           (r'Marta\s+(?:puso|hizo)\s+(\w+)',  'Marta',  {'cero', 'ninguna'})]

TRIADAS = [
    ('tres criterios', ['aspiración', 'compromiso'],
                       ['haya sitio', 'oportunidad organizativa', 'patrocinio', 'vacante']),
    ('tres puertas',   ['capacidad demostrada', 'oportunidad', 'patrocinio'],
                       ['aspiración', 'compromiso']),
]

# Dos armazones distintos con el mismo nombre: las cinco rutas del capítulo 2
# eran «puertas» en el cuerpo y «escaleras» en el título, y el capítulo 4 tiene
# sus tres puertas. Una ruta es una escalera; una condición del ascenso, una
# puerta. Nunca al revés.
METAFORA = [(2, r'\bpuertas?\b',        'una ruta del capítulo 2 es una escalera, no una puerta'),
            (None, r'\bcinco puertas\b', 'las cinco del capítulo 2 son escaleras'),
            (None, r'\btres escaleras\b','las tres del capítulo 4 son puertas')]

# Fórmulas de franqueza. En el capítulo 3 llegaron a apilarse tres en tres
# párrafos seguidos —«no te voy a engañar», «no te voy a vender humo»,
# «seamos sinceros»— y encima los dos primeros párrafos decían lo mismo.
# Una es un recurso; dos juntas es un tic, y el lector deja de creérselas.
FRANQUEZA = [r'no te voy a (?:engañar|mentir|vender (?:humo|esa moto|la moto))', r'no te engaño',
             r'seamos (?:sinceros|honestos|claros)', r'para ser (?:sincero|honesto)',
             r'te lo digo claro', r'sin engañarte', r'te seré sincero',
             r'con toda (?:sinceridad|honestidad)', r'hablando claro', r'sinceramente']

# Historias y frases contadas dos veces. Se comparan todos los párrafos del
# libro entre sí por 7-gramas. Así se destapó que la historia de la hamburguesa
# estaba en el capítulo 2 y otra vez en el 3, que el 14 volvía a argumentar el
# paracaídas en vez de entregar la lista que había prometido, y que el aforismo
# de las prisas salía en el 5 y en el 10. El detector no sabe distinguir la
# repetición deliberada de la accidental, así que los estribillos del libro van
# exentos y lo demás sale como aviso para mirarlo a ojo.
# Un estribillo se declara con el tramo entero que se repite a propósito, no
# con una etiqueta corta: _gramas tapa ese tramo y con él todos los gramas
# solapados. Y se comprueba que siga existiendo —una entrada obsoleta filtraría
# en vacío sin decir nada, que es el fallo que una red no se puede permitir.
ESTRIBILLOS = [
    # la pregunta central del libro, en negrita al cierre del 1 y del 4
    'si manana se sentaran a hablar de ti que tendrian encima de esa mesa aparte de tus numeros y',
    'numeros y lo que opine',
    'la respuesta honesta',
    # la tríada del capítulo 1, recuperada en el 12
    'tres criterios con los que se mira a una persona capacidad aspiracion y compromiso',
    'intentando contestar a una pregunta',
    # las siete cosas y el recuento con que cierra cada capítulo
    'objetivo medida autoridad padrino',
    'te han dado la responsabilidad',
    'encima de la mesa y la',
    'la apertura de sagunto',
    'con diferencia es que se arregle',
]

def _pal(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.findall(r'[a-z]+', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))

# El capítulo 5 llegó a afirmar que las opciones son el único depósito que se
# vacía sin que hagas nada, cuando sus propias definiciones dicen que la
# capacidad «se vacía sola con los años», la evidencia «cuando pasa el tiempo»
# y la confianza «con el silencio». Se cuenta cuántos se vacían en pasivo y se
# comprueba que el capítulo no le reclame la exclusiva a ninguno.
PASIVO = r'\bsol[oa]\b|por defecto|sin que hagas nada|pasa el tiempo|el silencio|con los años'
EXCLUSIVA = r'(?:el único depósito|los otros cuatro se vacían|se vacía por nada|'\
            r'única con una fuga|el único con una fuga)'

def depositos_pasivos(cuerpo):
    """Depósitos cuya propia definición dice que se vacían sin que hagas nada."""
    out = []
    for m in re.finditer(r'\*\*(\w+)\.\*\*(.+?)(?=\n\n|\Z)', cuerpo, re.S):
        v = m.group(2).split('se vacía', 1)
        if len(v) == 2 and re.search(PASIVO, v[1]): out.append(m.group(1))
    return out

def _gramas(par, n):
    """n-gramas del párrafo, tapando los tramos ocupados por un estribillo:
    una frase repetida a propósito genera decenas de gramas solapados y hay
    que quitarlos todos, no solo el que contiene la etiqueta."""
    ws = _pal(par)
    fijo = [False] * len(ws)
    for e in ESTRIBILLOS:
        pe = e.split()
        for i in range(len(ws) - len(pe) + 1):
            if ws[i:i + len(pe)] == pe:
                for k in range(i, i + len(pe)): fijo[k] = True
    return {' '.join(ws[i:i + n]) for i in range(len(ws) - n + 1)
            if not any(fijo[i:i + n])}

def revisa_estribillos(files):
    todo = ' || '.join(' '.join(_pal(f.read_text())) for f in files)
    return [f"ESTRIBILLO obsoleto, ya no filtra nada: «{e[:46]}…»"
            for e in ESTRIBILLOS if todo.count(e) < 2]

def ecos(files, n=7, umbral=3):
    """Pares de párrafos que comparten >= umbral n-gramas fuera de estribillos."""
    idx = {}
    for f in files:
        cap = int(re.match(r'(\d+)', f.stem).group(1))
        if cap == 16: continue          # la bibliografía repite títulos, es su oficio
        for k, par in enumerate(f.read_text().split('\n\n')):
            if not par.strip() or par.lstrip()[0] in '#|-': continue
            for g in _gramas(par, n): idx.setdefault(g, set()).add((cap, k))
    pares = {}
    for g, locs in idx.items():
        if len(locs) > 1:
            for a, b in combinations(sorted(locs), 2):
                pares.setdefault((a, b), []).append(g)
    return sorted(((len(gs), a, b, max(gs, key=len)) for (a, b), gs in pares.items()
                   if len(gs) >= umbral), reverse=True)

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

    # 3 bis · estadísticas inventadas y universales falsos
    # sobre el texto sin saltos de línea: «noventa y nueve por\nciento» tiene
    # que casar igual que si estuviera en una sola línea
    plano = ' '.join(cuerpo.split())
    for pf in PORCENTAJES_FALSOS:
        if re.search(re.escape(pf), plano, re.I):
            errs.append(f"CIFRA FALSA: «{pf}» — porcentaje redondo sin fuente")
    for ab in ABSOLUTOS:
        m = re.search(ab, plano, re.I)
        if m: warns.append(f"absoluto: «{m.group(0)}» — ¿es defendible o es voz?")
    for m in re.finditer(r'((?:\w+\s+){0,3})por ciento', cuerpo, re.I):
        frag = ' '.join(m.group(0).split())
        if not re.search(r'\d', frag):
            warns.append(f"porcentaje con letra: «{frag}» — comprobar que tiene fuente")

    # 3 ter · aritmética en la apertura
    if n and n != 16:
        apertura = ' '.join(re.sub(r'^#.*$', '', cuerpo, flags=re.M).split()[:350])
        cants = re.findall(CANTIDAD, apertura, re.I)
        if len(cants) >= 10:
            warns.append(f"apertura cargada: {len(cants)} cantidades en las primeras "
                         f"350 palabras ({', '.join(cants[:6])}…)")
        for a in ARITMETICA:
            if a in plano.lower():
                errs.append(f"ARITMÉTICA: «{a}» — el lector no debería tener que calcular")

    # 3 quater · el recuento de las siete cosas
    if n in CUENTA:
        ordinal, quedan = CUENTA[n]
        if not re.search(rf'\b{ordinal}\b.{{0,140}}encima de la mesa|'
                         rf'\b{ordinal}\b de las siete', plano, re.I):
            errs.append(f"RECUENTO: el capítulo debería poner la «{ordinal}» de las siete")
        # solo «Quedan» seguido de un numeral, y el último del capítulo: es el
        # del cierre. Si no se acota, casa con «se quedan en», «queda otro»…
        # dos formas: «Quedan cuatro» y «las cuatro que quedan». Variar la
        # redacción del recuento es deliberado; el verificador se adapta.
        N = r'(uno|una|dos|tres|cuatro|cinco|seis|siete)'
        ms = [a or b for a, b in re.findall(
            rf'\bqueda[n]?\s+{N}\b|\b{N}\s+que\s+queda[n]?\b', plano, re.I)]
        if not ms:
            errs.append(f"RECUENTO: falta el «quedan {quedan}» del cierre")
        elif ms[-1].lower() != quedan:
            errs.append(f"RECUENTO: dice «quedan {ms[-1]}» y deberían quedar {quedan}")
    for pat, quien, validos in REPARTO:
        for m in re.finditer(pat, plano):
            if m.group(1).lower() not in validos:
                errs.append(f"RECUENTO: «{quien} puso {m.group(1)}» — debería ser "
                            f"{' o '.join(sorted(validos))}")

    # 3 quinquies · cadenas de «y» dentro de una misma frase
    # El español enlaza con «y» de forma natural y el libro promedia 34 por mil
    # palabras, que está bien. Lo que cansa es la frase que se sostiene sobre
    # tres: «se acepta y se vuelve a poner y se cumple la fecha».
    for frase in re.split(r'(?<=[.?!])\s+', ' '.join(cuerpo.split())):
        # Calibrado sobre el libro: a partir de tres marca diecinueve frases y
        # casi todas son legítimas —enumeraciones, anáfora deliberada—. A partir
        # de cuatro marca una, y esa sí lo era.
        if len(re.findall(r'\by\b', frase, re.I)) >= 4 and len(frase.split()) > 12:
            warns.append(f'cadena de «y»: …{frase[:66]}…')

    # 3 sexies · columnas y filas que no existen
    # «puedes optimizar tu vida entera para la columna de la izquierda» remitía
    # a una tabla que no está dibujada en ninguna parte. Y la energía, que en la
    # cuadrícula del capítulo 2 es una fila, se citaba como columna.
    cabeceras, primeras = set(), set()
    for m in re.finditer(r'^\|(.+)\|\s*$', cuerpo, re.M):
        celdas = [c.strip().strip('*').lower() for c in m.group(1).split('|')]
        if not celdas: continue
        if re.match(r'^[\s:\-|]+$', m.group(1)):
            continue
        primeras.add(celdas[0])
        cabeceras |= set(celdas[1:])
    for tipo, valido in (('columna', cabeceras), ('fila', primeras)):
        for m in re.finditer(rf'\b{tipo} de (?:la |el |los |las )?([\wáéíóúñ]+)', plano, re.I):
            ref = m.group(1).lower()
            if ref in ('energía', 'ingreso', 'riesgo') and tipo == 'columna' and ref in primeras:
                errs.append(f"COLUMNA/FILA: «{tipo} de {ref}» — en la tabla es una fila")
            elif not any(ref in c for c in valido):
                errs.append(f"COLUMNA/FILA: «{tipo} de {ref}» — no existe esa {tipo} "
                            f"en ninguna tabla del capítulo")

    # 4 bis · no mezclar las dos tríadas
    # Solo se mira la glosa inmediata —hasta el final de la frase—, porque más
    # allá el capítulo puede hablar legítimamente de la otra tríada.
    for etiqueta, _propios, ajenos in TRIADAS:
        for m in re.finditer(re.escape(etiqueta), cuerpo, re.I):
            resto = cuerpo[m.end():m.end() + 200]
            # el markdown va con saltos de línea: hay que normalizarlos o
            # «haya\nsitio» no casa con «haya sitio»
            glosa = ' '.join(re.split(r'(?<=[.?!])\s', resto)[0].lower().split())
            intrusos = [a for a in ajenos if a in glosa]
            if intrusos:
                errs.append(f"TRÍADAS: «{etiqueta}» glosado con «{intrusos[0]}», "
                            f"que pertenece a la otra tríada")

    # 4 quinquies · nadie tiene la exclusiva de vaciarse solo
    if n == 5:
        pas = depositos_pasivos(cuerpo)
        m = re.search(EXCLUSIVA, cuerpo, re.I)
        if m and len(pas) > 1:
            errs.append(f"DEPÓSITOS: «{m.group(0)}» reclama una exclusiva, pero se "
                        f"vacían en pasivo {len(pas)}: {', '.join(pas)}")

    # 4 quater · las fórmulas de franqueza no se apilan
    marcas = sorted((len(cuerpo[:m.start()].split()), m.group(0))
                    for pat in FRANQUEZA for m in re.finditer(pat, cuerpo, re.I))
    for (p1, x), (p2, y) in zip(marcas, marcas[1:]):
        if p2 - p1 < 300:
            errs.append(f"FRANQUEZA: «{x}» y «{y}» a {p2 - p1} palabras — "
                        f"una es un recurso, dos juntas es un tic")

    # 4 bis bis · escalera = ruta (cap. 2), puerta = condición (cap. 4)
    for cap, patron, motivo in METAFORA:
        if cap is not None and cap != n: continue
        for m in re.finditer(patron, cuerpo, re.I):
            errs.append(f"METÁFORA: «{m.group(0)}» — {motivo}")

    # 4 ter · la raya de apertura va pegada al texto que introduce
    # «lo mismo —pero se nota», no «lo mismo — pero se nota». Las marcas de
    # trabajo «> GANCHO — …» no cuentan: el compositor las quita.
    for ln in cuerpo.split('\n'):
        if ln.lstrip().startswith('> GANCHO'): continue
        for m in re.finditer(r'\S — \S', ln):
            errs.append(f"RAYA: «{m.group(0)}» — la raya va pegada al texto que abre")

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
    for aviso in revisa_estribillos(files): print(f"       ✗ {aviso}")
    for cuantos, (c1, k1), (c2, k2), g in ecos(files):
        print(f"       · ECO: cap. {c1} y cap. {c2} comparten {cuantos} giros "
              f"de siete palabras — «{g[:52]}…»")
    print("-"*78)
    cuerpo = total - sum(check(f)[1] for f in files if int(re.match(r'(\d+)', f.stem).group(1)) in MARCO)
    print(f"total: {total:,} palabras · cuerpo (caps. 1–14): {cuerpo:,} · objetivo ~30.800 · "
          f"fallos: {fallos}")
    return 1 if fallos else 0

if __name__ == '__main__':
    sys.exit(main())
