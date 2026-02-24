@echo off
setlocal
cd /d "%~dp0"

echo Starte LocalWhisper Transcriber...

:: Prüfe auf virtuelle Umgebung
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
)

:: Aktiviere virtuelle Umgebung
call venv\Scripts\activate

:: Installiere Abhängigkeiten
echo Prüfe Abhängigkeiten...
pip install -r requirements.txt

:: Starte den Server
echo Starte Server auf http://localhost:8000
:: Öffne den Standard-Browser
start http://localhost:8000

:: Setze PYTHONPATH damit backend gefunden wird
set PYTHONPATH=%PYTHONPATH%;%CD%
python -m backend.main

pause
