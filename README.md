# LocalWhisper Transcriber

**LocalWhisper Transcriber** ist eine vollständig lokal laufende Web-Applikation zur Transkription von Audio- und Videodateien. Sie nutzt das leistungsstarke `faster-whisper` (eine optimierte Version von OpenAIs Whisper-Modell), um präzise Transkripte direkt auf Ihrem Rechner zu erstellen – ohne Cloud-Abhängigkeit, ohne API-Kosten und mit maximalem Datenschutz.

## 🚀 Features

- **Lokale Verarbeitung:** Keine Daten verlassen Ihren Rechner. Ideal für vertrauliche Inhalte.
- **Breite Formatunterstützung:** Verarbeitet `mp4`, `mkv`, `mov`, `mp3`, `wav`, `m4a`, `flac` und mehr.
- **Modell-Management:** Wählen Sie zwischen verschiedenen Whisper-Modellen (`tiny`, `base`, `small`, `medium`, `large-v3`) je nach Hardware-Leistung.
- **Automatischer Download:** Fehlende Modelle werden beim ersten Start automatisch heruntergeladen.
- **Markdown-Export:** Speichern Sie Ihre Transkripte als strukturierte `.md`-Dateien inklusive YAML-Frontmatter.
- **Dark & Light Mode:** Modernes UI, das sich Ihren Systemeinstellungen anpasst.
- **Plattformübergreifend:** Läuft auf Windows, Linux und macOS.

## 🛠 Installation & Start

### Voraussetzungen
- **Python 3.10 oder neuer** muss auf Ihrem System installiert sein.
- Eine Internetverbindung wird **nur für den ersten Start** benötigt, um die Whisper-Modelle herunterzuladen.

### Windows
1. Laden Sie das Repository herunter oder klonen Sie es.
2. Führen Sie die Datei `start.bat` per Doppelklick aus.
3. Die Anwendung öffnet sich automatisch in Ihrem Standard-Browser unter `http://localhost:8000`.

### Linux / macOS
1. Öffnen Sie ein Terminal im Projektordner.
2. Machen Sie das Startskript ausführbar (einmalig):
   ```bash
   chmod +x start.sh
   ```
3. Starten Sie die Anwendung:
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

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht. Sie können es frei verwenden, modifizieren und teilen.

---
*Erstellt mit Unterstützung von Manus.*
