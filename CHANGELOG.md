# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.2.1] - 2025-11-16

### Changed
- README.md aktualisiert

## [0.2.0] - 2025-11-16

### Added
- Seitennummer-Eingabefeld im Toolbar hinzugefügt
  - Benutzer können jetzt direkt eine Seitennummer eingeben und mit Enter zur gewünschten Seite springen
  - Das Eingabefeld zeigt immer die aktuelle Seitennummer an
  - Validierung der Eingabe mit Fehlermeldungen bei ungültigen Seitennummern

### Changed
- Page-Label umstrukturiert: Zeigt jetzt nur noch die Gesamtseitenzahl (z.B. "/ 25")
- Aktuelle Seitennummer wird im Eingabefeld statt im Label angezeigt

### Technical
- `tk.Entry` Widget für Seiteneingabe implementiert
- `goto_page()` Methode zur Navigation zu spezifischen Seiten hinzugefügt
- Enter-Taste Binding für direktes Springen zur eingegebenen Seite
