#!/bin/bash

# LocalWhisper Transcriber Startskript für Linux und macOS
# Wechsel in das Verzeichnis des Skripts
cd "$(dirname "$0")"

echo "Starte LocalWhisper Transcriber..."

# Prüfe auf Python 3
if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python 3 wurde nicht gefunden. Bitte installieren Sie Python 3.10+."
    exit 1
fi

# Prüfe auf virtuelle Umgebung
if [ ! -d "venv" ]; then
    echo "Erstelle virtuelle Umgebung..."
    python3 -m venv venv
fi

# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Installiere Abhängigkeiten
echo "Prüfe Abhängigkeiten..."
pip install -r requirements.txt

# Starte den Server
echo "Starte Server auf http://localhost:8000"

# Browser-Befehl basierend auf Betriebssystem
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    (sleep 2 && open http://localhost:8000) &
else
    # Linux (und andere)
    (sleep 2 && xdg-open http://localhost:8000) &
fi

# Setze PYTHONPATH damit backend gefunden wird
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m backend.main
