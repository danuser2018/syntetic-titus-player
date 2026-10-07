# Synthetic Titus Player 🦊

Un experimento para construir un agente que aprenda a jugar a **Titus the Fox** a base de mirar, probar cosas, equivocarse y volver a intentarlo.

La idea no es programar un bot que sepa de antemano cómo pasarse el juego.

La idea es darle las herramientas básicas para jugar y ver hasta dónde podemos llegar dejando que **aprenda por experiencia**.

---

## ¿Qué queremos conseguir?

Algo parecido a esto:

```text
        ┌──────────────┐
        │    AGENTE    │
        └──────┬───────┘
               │
             acción
               │
               ▼
        ┌──────────────┐
        │    TITUS     │
        │    DOSBox    │
        └──────┬───────┘
               │
          pantalla
               │
               ▼
        ┌──────────────┐
        │  PERCEPCIÓN  │
        └──────┬───────┘
               │
        "Titus está aquí"
        "hay un enemigo"
        "hay un agujero"
               │
               ▼
        ┌──────────────┐
        │    AGENTE    │
        └──────────────┘
```

En resumen:

> **mirar → decidir → actuar → ver qué ha pasado → aprender**

Y repetir.

---

## ¿Por qué Titus?

Porque es un entorno bastante pequeño y controlable, pero tiene suficientes cosas interesantes como para que el experimento tenga chicha.

Titus tiene:

* Plataformas.
* Saltos.
* Enemigos.
* Objetos que se pueden coger y lanzar.
* Obstáculos.
* Trampas.
* Pasadizos secretos.
* Checkpoints.
* Diferentes tipos de enemigos.
* Muchos escenarios que explorar.

Y, sobre todo, **nosotros no conocemos de antemano la solución de los niveles**.

Eso es importante.

El agente tampoco debería conocerla.

---

## Lo que NO queremos hacer

No queremos esto:

```text
Si estás en X:
    pulsa derecha 800 ms

Si estás en Y:
    salta

Si estás en Z:
    pulsa izquierda
```

Eso sería básicamente un walkthrough automatizado.

Funciona, pero no es demasiado interesante.

Tampoco queremos empezar construyendo una IA capaz de jugar a cualquier videojuego del mundo.

Eso nos llevaría bastante más lejos de lo que necesitamos.

---

## Lo que SÍ queremos

Queremos un agente especializado en este tipo de juego, pero que **no conozca el mapa ni las soluciones de antemano**.

Por ejemplo:

```text
Ve un enemigo.

Prueba a acercarse.
    ↓
Mala idea.

Prueba a saltar.
    ↓
Funciona.

Guarda:

"Este tipo de enemigo se puede evitar saltando."
```

Más adelante:

```text
Ve un objeto.

Lo coge.

Lo lanza contra un enemigo.

Funciona.

Guarda:

"Este objeto puede utilizarse contra este enemigo."
```

Y después puede reutilizar ese conocimiento en otra situación.

La gracia está precisamente ahí.

---

# Arquitectura

De momento no necesitamos una arquitectura monstruosa.

La idea es ir creciendo poco a poco:

```text
synthetic-titus-player
│
├── DOSBox
│
├── control
│   └── teclado
│
├── captura
│   └── screenshots
│
├── percepción
│   └── ¿qué está pasando?
│
├── mundo
│   └── representación del estado
│
├── agente
│   └── ¿qué hago ahora?
│
├── aprendizaje
│   └── ¿qué he aprendido?
│
└── memoria
    └── ¿qué recuerdo?
```

No hace falta implementar todo esto desde el principio.

De hecho, **no debemos hacerlo**.

---

# El plan

## Fase 0 — Conseguir que Titus nos haga caso

Primero tenemos que resolver lo más aburrido.

Y probablemente lo más importante.

Queremos poder hacer:

```bash
titus-player start

titus-player press right

titus-player hold right 500

titus-player press up

titus-player screenshot

titus-player stop
```

Y que realmente ocurra.

Nada de IA todavía.

Nada de visión artificial.

Nada de aprendizaje.

Solo:

```text
Python
   ↓
teclado
   ↓
DOSBox
   ↓
Titus
```

Si esto no funciona de forma fiable, todo lo demás da igual.

---

## Fase 1 — Ver el juego

Una vez podamos controlarlo, toca conseguir que el programa pueda **verlo**.

Al principio no necesitamos una IA sofisticada.

Una captura de pantalla ya es suficiente:

```text
┌───────────────────────────────┐
│                               │
│          🦊                   │
│             👾                │
│      █████████████            │
│                               │
└───────────────────────────────┘
```

A partir de ahí intentaremos detectar cosas sencillas:

* Dónde está Titus.
* Dónde hay suelo.
* Dónde hay plataformas.
* Dónde hay enemigos.
* Dónde hay objetos.
* Si Titus se está moviendo.

---

## Fase 2 — De píxeles a mundo

No queremos que el agente razone directamente sobre una imagen.

Queremos convertirla en algo parecido a:

```python
Observation(
    player=Player(...),
    enemies=[...],
    objects=[...],
    terrain=[...],
    hazards=[...]
)
```

Así podremos decir:

```text
Titus está aquí.
Hay un enemigo delante.
Hay suelo debajo.
Hay un objeto a la izquierda.
```

en lugar de:

```text
pixel (143, 82) = ...
```

---

## Fase 3 — Darle manos y pies

El agente tendrá unas pocas acciones básicas:

```text
LEFT
RIGHT
JUMP
DUCK
PICK_UP
DROP
THROW
```

Y algunas acciones podrán tener duración:

```text
RIGHT 300 ms
```

o combinarse:

```text
RIGHT + JUMP
```

La idea es darle **capacidades**, no estrategias.

---

# Fase 4 — Reglas

Aquí empieza a ponerse interesante.

El agente tendrá algunas reglas básicas que podemos considerar parte de la física o del funcionamiento del juego.

Por ejemplo:

```text
No puedes atravesar una pared.

Los saltos duran un tiempo determinado.

Llevar un objeto cambia lo que puedes hacer.

Algunos enemigos son peligrosos.

Algunos objetos pueden lanzarse.
```

Pero habrá otras cosas que tendrá que descubrir.

Por ejemplo:

```text
¿Puedo saltar este enemigo?

¿Puedo matarlo lanzándole esto?

¿Puedo llegar a esa plataforma?

¿Este objeto sirve para pasar ese obstáculo?

¿Hay otro camino?
```

---

# Fase 5 — Aprender

Aquí aparece el verdadero experimento.

Cada interacción puede producir una experiencia:

```text
estado anterior
       ↓
     acción
       ↓
estado nuevo
       ↓
resultado
```

Por ejemplo:

```text
Estado:
    enemigo delante

Acción:
    avanzar

Resultado:
    daño

Aprendizaje:
    mala estrategia
```

Otro intento:

```text
Estado:
    enemigo delante

Acción:
    saltar

Resultado:
    enemigo evitado

Aprendizaje:
    buena estrategia
```

Con suficientes experiencias podremos empezar a construir reglas.

---

# Fase 6 — Explorar

El agente no debería limitarse a repetir siempre lo que ya conoce.

Tiene que experimentar.

Algo parecido a:

```text
        ¿Qué hago?
             │
       ┌─────┴─────┐
       │           │
    conozco      no sé
       │           │
       ▼           ▼
     usar       probar
       │           │
       └─────┬─────┘
             ▼
          observar
             │
             ▼
           aprender
```

Tendrá que encontrar un equilibrio entre:

**Explotar**

> "Esto ya sé que funciona."

y

**Explorar**

> "No sé qué pasará, pero vamos a probar."

---

# Memoria

Con el tiempo necesitaremos guardar diferentes tipos de información.

### Experiencias

```text
En esta situación hice X.
Pasó Y.
```

### Reglas

```text
Este enemigo se puede evitar saltando.
```

### Mundo

```text
Por aquí ya he pasado.

Aquí había un callejón sin salida.

Aquí encontré un checkpoint.
```

La memoria permitirá que el agente no tenga que descubrirlo todo desde cero en cada partida.

---

# ¿Y el aprendizaje automático?

No necesariamente desde el minuto uno.

De hecho, **preferimos empezar sin meter una red neuronal porque sí**.

Primero queremos comprobar hasta dónde podemos llegar con:

* reglas;
* memoria;
* búsqueda;
* exploración;
* puntuaciones;
* experiencia acumulada.

Si llegamos a un punto donde este enfoque se queda corto, entonces introduciremos ML/RL y podremos comparar:

```text
reglas
   vs
reglas + aprendizaje
   vs
reinforcement learning
   vs
otros enfoques
```

Eso es mucho más interesante que meter una red neuronal desde el principio y no saber muy bien qué está haciendo.

---

# Cómo sabremos si funciona

Necesitamos métricas.

Por ejemplo:

```text
⏱ Tiempo sobrevivido
🗺️ Pantallas descubiertas
❤️ Vidas perdidas
👾 Enemigos derrotados
🚧 Obstáculos superados
🔒 Checkpoints alcanzados
📈 Progreso del nivel
🏁 Niveles completados
```

Una señal especialmente interesante será:

> **¿El agente mejora cuando vuelve a intentarlo?**

Si la respuesta es sí, tenemos aprendizaje.

---

# Principios del proyecto

### 1. Empezar pequeño

Nada de construir Skynet para jugar al Titus.

Primero:

```text
arrancar → pulsar tecla → hacer screenshot
```

### 2. Todo medible

Si algo funciona, queremos poder demostrarlo.

### 3. No hacer trampas

No le damos el mapa ni el walkthrough.

### 4. Entender por qué hace las cosas

Siempre que sea posible queremos poder responder:

> "¿Por qué ha saltado?"

### 5. Aprender antes de complicar

Si una tabla de reglas funciona, no necesitamos una red neuronal.

### 6. Construir por capas

Cada fase debe dejar algo funcionando que podamos probar.

---

# El primer MVP

El primer objetivo es extremadamente sencillo:

```text
┌─────────────┐
│   Python    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  DOSBox     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Titus Fox   │
└──────┬──────┘
       │
       ▼
  screenshot
```

Queremos conseguir que el programa sea capaz de:

1. Arrancar DOSBox.
2. Arrancar Titus.
3. Pulsar teclas.
4. Mantener teclas durante un tiempo.
5. Capturar la pantalla.
6. Cerrar el juego.

Cuando esto funcione, tendremos nuestro primer ladrillo.

Y entonces podremos empezar con lo divertido:

> **enseñarle a Titus a aprender.** 🦊

---

## Estado actual

**Fase:** 0 — Control del entorno

**Siguiente objetivo:**

```text
DOSBox
   ↓
Titus
   ↓
control por teclado
   ↓
screenshot
```

A partir de ahí: **ojos → mundo → acciones → reglas → aprendizaje → exploración**.
