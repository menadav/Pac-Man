# Project Management

Solo project. Personal Kanban board (Todo / Doing / Done).

## Planning
| Phase | Estimated | Actual |
|---|---|---|
| Setup + A-Maze-ing integration | 0.5 d | 0.5 d |
| Config + parser + validation | 0.5 d | 0.5 d |
| Maze render + player | 1.5 d | 2.0 d |
| Ghost AI + states | 1.0 d | 1.5 d |
| Scenes (menu, pause, end, highscores) | 1.0 d | 1.0 d |
| HUD + cheat + polish | 0.5 d | 1.0 d |
| Packaging + README + lint | 1.0 d | 0.5 d |

## Key Decisions
- **Tile size centralized** in `EntitiesMannager`, rounded to a multiple of 6 so that movement steps (3 px player, 1 or 2 px ghosts) land exactly on cell centers.
- **Logic update at 40 Hz** decoupled from rendering at 60 fps (time accumulator).
- **Timeout = lose 1 life + reset level**, game over only at 0 lives.
- **Width/height limited to [8, 40]** because the maze generator is recursive.
- **Ghosts with state machine** CHASE / ESCAPE / EATEN (respawn after 5 s).

## Risks and Mitigations
- Generator recursion → clamp in config.
- Corrupted highscore → try/except + Pydantic, empty top-10 on error.
- Unhandled exception → global `try/except` in `pac_man.py`.

## Blockers Found
- Desync between map and entities when adding HUD → single source of truth for `t_size` and offsets.
- `is_centered()` always false because the step didn't divide the tile evenly → snap to multiple of 6.
- Ghosts eatable multiple times in a row → EATEN state excluded from collisions for 5 s.
