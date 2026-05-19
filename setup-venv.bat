@echo off
setlocal

@REM Erstellt die Projekt-Umgebung .venv und installiert requirements.txt

set "PYTHON_CMD="

where python >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
)

if "%PYTHON_CMD%"=="" (
    where py >nul 2>&1
    if %errorlevel%==0 (
        set "PYTHON_CMD=py -3.13"
    )
)

if "%PYTHON_CMD%"=="" (
    echo Fehler: Kein Python-Interpreter gefunden.
    echo Bitte installiere Python 3.13+ und versuche es erneut.
    exit /b 1
)

echo Verwende Interpreter: %PYTHON_CMD%

if not exist ".venv" (
    echo Erstelle virtuelle Umgebung .venv ...
    call %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo Fehler beim Erstellen von .venv.
        exit /b 1
    )
) else (
    echo .venv existiert bereits.
)

echo Aktualisiere pip ...
call .venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo Fehler beim Aktualisieren von pip.
    exit /b 1
)

if exist "requirements.txt" (
    echo Installiere Abhaengigkeiten aus requirements.txt ...
    call .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Fehler bei der Installation aus requirements.txt.
        exit /b 1
    )
) else (
    echo Hinweis: requirements.txt nicht gefunden. Ueberspringe Paketinstallation.
)

echo.
echo Fertig. Umgebung erstellt unter .venv

echo Aktivieren mit:
echo .venv\Scripts\Activate.ps1

endlocal
