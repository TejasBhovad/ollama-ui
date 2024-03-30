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
pyinstaller --name="Ollama UI" --windowed --add-data "index.css:." --icon=icons/ai_icon.png main.py --onefile
```
> Modify to add SVGs

## Adding SVGs
https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html
remove ui tag
https://doc.qt.io/qt-5/resources.html