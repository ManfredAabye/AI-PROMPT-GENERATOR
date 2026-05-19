@echo off

if not exist ".venv\Scripts\python.exe" (
	echo .venv wurde nicht gefunden. Starte setup-venv.bat ...
	call setup-venv.bat
	if errorlevel 1 (
		echo Fehler beim Erstellen der .venv.
		exit /b 1
	)
)

call .venv\Scripts\python.exe UniversalPromptManager.py