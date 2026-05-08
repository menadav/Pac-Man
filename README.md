flowchart TD
    A[Pac-man] -->|Config_json|B(GameMannager)
    B --> C{DataProcess}
    C -->|loop_menu| D[Menu]
    D -->|loop_start| E[Start]
    D -->|loop_highscore| H[HighScore]
    D -->|loop_instructions| G[Instructions]
    D --> J[Exit]
    E -->|Game| K[save_score]
    K --> D 
