# myTinyDesk

Ein leichtgewichtiger, ressourcenschonender PDF-Viewer mit GUI, entwickelt in Python mit Tkinter. Ideal für Terminalserver und Desktop-Umgebungen.

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## ✨ Features

- 📂 **PDF direkt in der App anzeigen** - Keine externen Programme nötig
- 🔍 **Zoom-Funktionen** - Stufenlos zwischen 40% und 300%
- ⚡ **Schnelle Navigation** - Vor/Zurück durch Seiten mit Buttons oder Tastatur
- 🎨 **Moderne UI** - Dunkle Toolbar mit intuitiver Bedienung
- ⌨️ **Keyboard-Shortcuts** - Pfeiltasten, Page Up/Down, +/- für Zoom
- 💾 **Ressourcenschonend** - Rendert nur die aktuelle Seite
- 🖥️ **Terminalserver-tauglich** - Minimaler Speicher- und CPU-Verbrauch

## 🎯 Anwendungsfälle

- Schnelles Betrachten von PDFs ohne schwere Desktop-Anwendungen
- Deployment auf Terminalservern mit vielen gleichzeitigen Benutzern
- Eingebetteter PDF-Viewer für eigene Python-Anwendungen
- Ressourcenschonende Alternative zu Adobe Reader, Evince, etc.

## 📋 Voraussetzungen

- **Python 3.12+** (funktioniert auch mit 3.8+)
- **Tkinter** (meist vorinstalliert, sonst siehe Installation)
- **Linux** (Ubuntu, Debian, etc.) - Windows/macOS mit kleinen Anpassungen möglich

## 🚀 Installation

### 1. Repository klonen

```bash
git clone https://github.com/retoro-sen/mytinydesk_pdfreader.git
cd mytinydesk_pdfreader
```

### 2. Tkinter installieren (falls nicht vorhanden)

```bash
sudo apt-get update
sudo apt-get install -y python3-tk
```

### 3. Virtuelle Umgebung erstellen (empfohlen)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## 🎮 Verwendung

### Starten der Anwendung

```bash
python3 main.py
```

Oder mit aktivierter virtueller Umgebung:

```bash
.venv/bin/python main.py
```

### Bedienung

#### Buttons
- **📂 Öffnen** - PDF-Datei auswählen
- **◀ Zurück** - Vorherige Seite
- **Vor ▶** - Nächste Seite
- **🔍+** - Hineinzoomen
- **🔍-** - Herauszoomen

#### Keyboard-Shortcuts
- `←` / `→` - Seite zurück/vor
- `Page Up` / `Page Down` - Seite zurück/vor
- `+` / `-` - Zoom in/out

## 🏗️ Projektstruktur

```
pythongui/
├── main.py              # Hauptanwendung (myTinyDesk)
├── requirements.txt     # Python-Abhängigkeiten
├── README.md           # Diese Datei
└── .venv/              # Virtuelle Umgebung (nach Installation)
```

## 🔧 Technische Details

### Verwendete Bibliotheken

- **Tkinter** - GUI-Framework (Standard-Python-Bibliothek)
- **PyMuPDF (fitz)** - PDF-Rendering-Engine
- **Pillow (PIL)** - Bildverarbeitung für Display-Konvertierung

### Ressourcenverbrauch

- **RAM**: ~20-50 MB (abhängig von PDF-Größe)
- **CPU**: Minimal (nur beim Seitenwechsel/Zoom)
- **Festplatte**: ~15 MB (inkl. Abhängigkeiten)

### Architektur

myTinyDesk nutzt eine ereignisgesteuerte Architektur:
1. PDF wird mit PyMuPDF geladen
2. Aktuelle Seite wird als Pixmap gerendert
3. Pixmap wird in PIL Image konvertiert
4. Image wird als Tkinter PhotoImage im Canvas angezeigt
5. Nur die aktuelle Seite wird im Speicher gehalten

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"

Tkinter ist nicht installiert. Lösung:
```bash
sudo apt-get install python3-tk
```

### "ModuleNotFoundError: No module named 'fitz'"

PyMuPDF ist nicht installiert. Lösung:
```bash
pip install PyMuPDF
```

### PDF wird nicht angezeigt

- Stelle sicher, dass die PDF-Datei nicht beschädigt ist
- Prüfe, ob genügend RAM verfügbar ist
- Bei sehr großen PDFs (>100 MB) kann das Rendern länger dauern

### GUI startet nicht auf Terminalserver

Stelle sicher, dass:
- X11-Forwarding aktiviert ist (bei SSH: `ssh -X`)
- DISPLAY-Variable korrekt gesetzt ist: `echo $DISPLAY`
- Ein X-Server läuft

## 🔮 Geplante Features

- [ ] Vollbildmodus
- [ ] Lesezeichen/Favoriten
- [ ] Suchfunktion im PDF
- [ ] Thumbnail-Ansicht aller Seiten
- [ ] Druckfunktion
- [ ] Dunkler Modus für die gesamte UI
- [ ] PDF-Rotation
- [ ] Mehrere PDFs in Tabs öffnen

## 🤝 Mitwirken

Contributions sind willkommen! 

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

## 👤 Autor

**retoro-sen**

- GitHub: [@retoro-sen](https://github.com/retoro-sen)
- E-Mail: [retoro-sen@protonmail.ch](mailto:retoro-sen@protonmail.ch)

## ☕ Unterstütze das Projekt

Wenn dir myTinyDesk gefällt und du das Projekt unterstützen möchtest:

**Bitcoin (BTC):**
```
bc1q40tcmyk8rtp5vyg4ykgexa0upcvd08l99dq4z0
```

**Kontakt:** [retoro-sen@protonmail.ch](mailto:retoro-sen@protonmail.ch)

## 🙏 Danksagungen

- [PyMuPDF](https://pymupdf.readthedocs.io/) für die exzellente PDF-Rendering-Library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) für das robuste GUI-Framework
- Die Python-Community für kontinuierliche Unterstützung

---

⭐ Wenn dir dieses Projekt gefällt, gib ihm einen Stern auf GitHub!
