# LocalWhisper Transcriber

**LocalWhisper Transcriber** ist eine vollständig lokal laufende Web-Applikation zur Transkription von Audio- und Videodateien. Sie nutzt das leistungsstarke `faster-whisper` (eine optimierte Version von OpenAIs Whisper-Modell), um Transkripte direkt auf deinem Rechner zu erstellen – völlig lokal, ohne Cloud-Abhängigkeit, ohne API-Kosten, datenschutzfreundlich.

## 🚀 Features

- **Lokale Verarbeitung:** Keine Daten verlassen deinen Rechner. Ideal für vertrauliche Inhalte.
- **Breite Formatunterstützung:** Verarbeitet `mp4`, `mkv`, `mov`, `mp3`, `wav`, `m4a`, `flac` und mehr.
- **Modell-Management:** Wähle zwischen verschiedenen Whisper-Modellen (`tiny`, `base`, `small`, `medium`, `large-v3`) je nach Hardware-Leistung.
- **Automatischer Download:** Fehlende Modelle werden beim ersten Start automatisch heruntergeladen.
- **Markdown-Export:** Speichere deine Transkripte als strukturierte `.md`-Dateien inklusive YAML-Frontmatter.
- **Dark & Light Mode:** Modernes UI, das sich deinen Systemeinstellungen anpasst.
- **Plattformübergreifend:** Läuft auf Windows, Linux und macOS.

## 🛠 Installation & Start

### Voraussetzungen
- **Python 3.10 oder neuer** muss auf dem System installiert sein. Herunterladen und installieren unter https://www.python.org/downloads/
- Eine Internetverbindung wird **nur für den ersten Start** benötigt, um die Whisper-Modelle herunterzuladen.

### Windows
1. Lade das Repository herunter oder klone Sie es.
2. Führe die Datei `start.bat` per Doppelklick aus.
3. Die Anwendung öffnet sich automatisch in deinem Standard-Browser unter `http://localhost:8000`. Die Meldung zur Firewall bitte zulassen.

### Linux / macOS
1. Öffne ein Terminal im Projektordner.
2. Mach das Startskript ausführbar (einmalig):
   ```bash
   chmod +x start.sh
   ```
3. Starte die Anwendung:
   ```bash
   ./start.sh
   ```

## 📂 Projektstruktur

```text
localwhisper/
├── backend/             # Python FastAPI Logik & Transkription
├── frontend/            # HTML, CSS (Variables_LB.css) & Vanilla JS
├── models/              # Speicherort für heruntergeladene Whisper-Modelle
├── exports/             # Standard-Verzeichnis für exportierte Transkripte
├── start.bat / .sh      # Plattformspezifische Startskripte
└── requirements.txt     # Python-Abhängigkeiten
```

## ⚙️ Technische Details

- **Backend:** FastAPI (Python)
- **Transkription:** `faster-whisper` (CTranslate2)
- **Frontend:** HTML5, Vanilla JavaScript, CSS3 (mit `light-dark()` Support)
- **Hardware-Beschleunigung:** Nutzt automatisch NVIDIA GPUs (CUDA), falls vorhanden und konfiguriert, andernfalls CPU-Betrieb mit 8-Bit Quantisierung (`int8`).

## 📝 Lizenz

Keine – gerne forken, teilen etc ... aber ein Quellenverweis auf mich wäre freundlich, wer schmückt sich schon gerne mit fremden Federn ...? 😉
