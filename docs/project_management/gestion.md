# Gestión del proyecto

Proyecto solo. Tablero Kanban personal (Todo / Doing / Done).

## Planificación

| Fase                                      | Estimado | Real  |
| ----------------------------------------- | -------- | ----- |
| Setup + integración A-Maze-ing            | 0,5 d    | 0,5 d |
| Config + parser + validación              | 0,5 d    | 0,5 d |
| Render del laberinto + jugador            | 1,5 d    | 2,0 d |
| IA de los fantasmas + estados             | 1,0 d    | 1,5 d |
| Escenas (menú, pausa, fin, highscores)    | 1,0 d    | 1,0 d |
| HUD + cheat + pulido                      | 0,5 d    | 1,0 d |
| Packaging + README + lint                 | 1,0 d    | 0,5 d |

## Decisiones clave

- **Tamaño de tile centralizado** en `EntitiesMannager`, redondeado a múltiplo de 6 para que los pasos de movimiento (3 px jugador, 1 o 2 px fantasmas) caigan exactos en los centros.
- **Update lógico a 40 Hz** desacoplado del render a 60 fps (acumulador de tiempo).
- **Timeout = perder 1 vida + reiniciar nivel**, game over solo a 0 vidas.
- **Width/height limitados a [8, 40]** porque el generador de laberinto es recursivo.
- **Fantasmas con máquina de estados** CHASE / ESCAPE / EATEN (respawn tras 5 s).

## Riesgos y mitigaciones

- Recursión del generador → clamp en el config.
- Highscore corrupto → try/except + Pydantic, top-10 vacío en caso de error.
- Excepción no controlada → `try/except` global en `pac_man.py`.

## Puntos de bloqueo encontrados

- Desincronización entre mapa y entidades al añadir HUD → una sola fuente de verdad para `t_size` y offsets.
- `is_centered()` siempre falso porque el paso no dividía el tile → snap a múltiplo de 6.
- Fantasmas comibles varias veces seguidas → estado EATEN excluido de las colisiones durante 5 s.
