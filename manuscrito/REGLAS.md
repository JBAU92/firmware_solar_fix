# Reglas de escritura — la red

**Esto no es un documento de intenciones. Es una lista de fallos concretos que ya he cometido en
este proyecto, con su antídoto y, donde se puede, con una comprobación automática.**

---

## Las nueve trampas

### 1. Inventar cifras que suenan a dato
**Ya lo hice.** Escribí «su equipo vendía un doce por ciento menos» y «la errata de la página
nueve» como si fueran hechos. En un libro que se vende como basado en evidencia, una sola cifra
fabricada contamina también los estudios de verdad.

> **Regla:** en una escena **no aparece ningún número** salvo que venga de una fuente citada. La
> concreción se consigue con objetos y acciones, no con estadísticas falsas. «Vendía menos que el
> año anterior» en vez de «un 12% menos». «Una errata» en vez de «una errata en la página nueve».

**Excepción:** los datos de estudios verificados en el archivo 04, con su cifra exacta.
**Comprobación automática:** el verificador marca todo dígito en bloques de escena.

### 2. Que todo pase en una oficina
**Ya lo hice.** Escribí una regla de sectores y luego escribí escenas de oficina igualmente.

> **Regla:** máximo cuatro escenas de oficina en catorce capítulos, y nunca dos seguidas del mismo
> sector. Reparto fijado en la biblia.

**Comprobación automática:** el verificador cuenta sectores por capítulo contra el reparto.

### 3. Sobrematizar hasta dejar la prosa coja
Tengo tirón natural a cubrirme. «Podría ser», «en cierto modo», «no siempre». Tres seguidos y la
frase deja de afirmar nada.

> **Regla:** una afirmación se hace **entera** y el matiz va **después**, en su sitio —el
> contrapeso—, no incrustado en la frase. Si la frase necesita tres muletas, es que no la creo, y
> entonces no va.

**Comprobación automática:** densidad de muletillas por capítulo, con umbral.

### 4. Sermonear
El lector no ha comprado un cura. La ética se cuenta en consecuencias: qué explota y por qué.

> **Regla:** cero frases que empiecen por «es importante recordar que», «debemos», «hay que ser
> consciente de». La moral se dice **una vez** por capítulo como máximo y en forma de consecuencia.

### 5. Perder el hilo de Marta y Javier bajo el método
El contenido empuja y la historia se queda fuera. Es el fallo que más caro sale, porque el hilo es
el motor de lectura.

> **Regla:** cada capítulo con revelación asignada (1, 6, 8, 10, 11, 12, 14) **empieza o termina**
> con ella. No se menciona de pasada en mitad.

**Comprobación automática:** presencia de «Marta» o «Javier» en los capítulos asignados.

### 6. Engordar
Escribo largo. Catorce por 2.200 son 30.800 palabras y el presupuesto no es negociable.

> **Regla:** 2.000–2.500 por capítulo. Un capítulo de 2.900 no se recorta al final: se recorta al
> terminarlo, en caliente.

**Comprobación automática:** recuento por capítulo con aviso.

### 7. Repetir el mejor ejemplo
Cuando un ejemplo funciona, tiendo a volver a él. El lector lo nota como relleno.

> **Regla:** un registro de ejemplos y pepitas ya usados. Nada se usa dos veces salvo el *callback*
> deliberado, que se anota como tal.

### 8. La cadencia de máquina
Tríos por todas partes. «No es X, es Y» en cada página. Todos los párrafos de cuatro líneas. Rayas
por doquier.

> **Regla:** «No es X, es Y» **una vez por capítulo como máximo**. Variedad obligatoria de longitud
> de párrafo: al menos uno de una sola línea y al menos uno de más de seis por capítulo. Y la
> apertura de cada capítulo cambia de forma —escena, pregunta directa, diálogo, dato, objeto— según
> el reparto de la biblia, para que no suenen los catorce igual.

**Comprobación automática:** frecuencia de «no es… es», rayas por mil palabras, varianza de párrafo.

### 9. Cerrar el capítulo sin abrir el siguiente
Es la regla que más sostiene la lectura y la más fácil de olvidar cuando llevas 2.400 palabras.

> **Regla:** la última frase de cada capítulo apunta al siguiente. Sin excepción.

**Comprobación automática:** el verificador exige un bloque `> GANCHO` al final.

---

## Cómo escribo, en concreto

1. **En orden.** El capítulo N se escribe habiendo leído el N‑1 terminado, no su ficha. Así la
   revelación de Javier escala de verdad y los ganchos encajan.
2. **Un estudio por capítulo**, contado como historia, con su cifra exacta del archivo 04. El resto
   a las notas.
3. **La escena primero**, antes de saber cómo sigue el capítulo. Si la escena no se sostiene sola,
   el capítulo no arranca.
4. **Recorte en caliente.** Al terminar cada capítulo, quitar el 10%. Siempre sobra.
5. **Verificador después de cada capítulo**, no al final.

## Marcas en el texto

- `⟦AUTOR: …⟧` — pasaje que depende de un hecho de su vida y que **tiene que reescribir él**.
- `⟦VERIFICAR: …⟧` — dato pendiente de confirmar contra fuente.
- `> GANCHO` — última línea, la que abre el capítulo siguiente.
