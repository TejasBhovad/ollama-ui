# Ollama UI App
Desktop app created to communicate with ollama model locally

## Tech Stack

- PyQT
- CSS

## Packages

- PyQt6

## Progress

MVP done
Styling remaining
Exporting to be done

## Build Command
    
```bash
pyinstaller --onefile main.py --add-data "frontend/logos:frontend/logos" --add-data "frontend/components:frontend/components" --add-data "index.css:."
```
> Modify to add SVGs