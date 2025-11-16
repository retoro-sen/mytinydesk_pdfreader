# Icon Integration für myTinyDesk

## Automatische Icon-Erkennung

Das `setup.py` Script sucht automatisch nach Icon-Dateien im Projektverzeichnis:
- `icon.png` (Linux/macOS)
- `icon.ico` (Windows)
- `icon.svg` (Linux)
- `icon.xpm` (Linux)

## Icons erstellen

### Option 1: Automatisch mit create_icon.py

```bash
python3 create_icon.py
```

Erstellt automatisch:
- `icon.png` (256x256) - Universal
- `icon.ico` (Multi-Size) - Windows
- `icon_48x48.png` - Linux
- `icon_64x64.png` - Linux  
- `icon_128x128.png` - Linux

### Option 2: Eigenes Icon verwenden

Platziere deine Icon-Datei als:
- **Linux**: `icon.png` (48x48, 64x64 oder 128x128 empfohlen)
- **Windows**: `icon.ico` (muss .ico Format sein)
- **macOS**: `icon.png` (512x512 empfohlen)

## Plattform-spezifische Details

### Linux (.desktop Datei)
```ini
Icon=/pfad/zu/projekt/icon.png
```
Unterstützte Formate: PNG, SVG, XPM

### Windows (.lnk Verknüpfung)
```python
shortcut.IconLocation = 'C:\\pfad\\zu\\projekt\\icon.ico'
```
**Wichtig**: Muss .ico Format sein!

### macOS (.app Bundle)
Für macOS muss ein .icns Format erstellt werden:
```bash
# PNG zu ICNS konvertieren (auf macOS)
mkdir icon.iconset
sips -z 16 16 icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out icon.iconset/icon_16x16@2x.png
# ... weitere Größen ...
iconutil -c icns icon.iconset
```

## Icon-Anforderungen

### Größen
- **Minimum**: 16x16 px
- **Empfohlen**: 256x256 px oder größer
- **Windows ICO**: Multi-Size (16, 32, 48, 64, 128, 256)

### Formate
- **PNG**: Transparent background empfohlen
- **ICO**: Windows-Standard
- **SVG**: Skalierbar, gut für Linux

### Design-Tipps
- Klare, einfache Formen
- Gut erkennbar auch in kleinen Größen
- Kontrastreiche Farben
- Transparenter Hintergrund (außer bei ICO)

## Verwendung im setup.py

Das Setup-Script prüft automatisch:

```python
# Suche nach Icon
for ext in ['.png', '.ico', '.svg', '.xpm']:
    potential_icon = current_dir / f'icon{ext}'
    if potential_icon.exists():
        icon_path = potential_icon
        break
```

Wenn kein Icon gefunden wird:
- **Linux**: Verwendet System-Icon `application-pdf`
- **Windows**: Verwendet `shell32.dll,1` (Standard PDF-Icon)

## Icon-Generator anpassen

Bearbeite `create_icon.py` um:
- Farben zu ändern: `doc_color`, `text color`
- Text zu ändern: `text = "PDF"`
- Größen hinzuzufügen: `sizes` Liste
- Design zu modifizieren: `ImageDraw` Befehle

## Beispiel: Eigenes Icon einbinden

1. Erstelle oder besorge ein Icon
2. Benenne es um:
   - `icon.png` für Linux/macOS
   - `icon.ico` für Windows
3. Platziere es im Projekt-Root
4. Führe `python3 setup.py` aus
5. Das Icon wird automatisch erkannt und verwendet!

## Troubleshooting

### "Icon wird nicht angezeigt"
- **Linux**: Desktop-Datenbank aktualisieren: `update-desktop-database ~/.local/share/applications/`
- **Windows**: Verknüpfung neu erstellen
- **Alle**: Cache leeren/neu anmelden

### "Icon hat falsche Größe"
- Linux: Verwende 48x48 oder 64x64 px
- Windows: ICO muss Multi-Size sein
- macOS: 512x512 px empfohlen

### "Icon ist verpixelt"
- Verwende größere Basis-Auflösung (512x512)
- Nutze SVG-Format (Linux)
- Erstelle separate Größen statt Skalierung
