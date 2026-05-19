@echo off

@REM Baut UniversalPromptManager.py zu UniversalPromptManager.exe

if not exist ".venv\Scripts\python.exe" (
	echo .venv wurde nicht gefunden. Starte setup-venv.bat ...
	call setup-venv.bat
	if errorlevel 1 (
		echo Fehler beim Erstellen der .venv.
		exit /b 1
	)
)

call .venv\Scripts\python.exe -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
	echo PyInstaller wird installiert...
	call .venv\Scripts\python.exe -m pip install pyinstaller
)
echo Baue UniversalPromptManager.exe ...
call .venv\Scripts\python.exe -m PyInstaller --onefile --icon=icon.ico --add-data "icon.png;." --add-data "icon.ico;." UniversalPromptManager.py
echo Fertig! Die EXE befindet sich im dist-Ordner.

:: languages.json kopieren
copy upmlanguages.json dist\upmlanguages.json

:: Verzeichnis categories kopieren
xcopy categories dist\categories /E /I /Y

:: Verzeichnis strategies kopieren
xcopy strategies dist\strategies /E /I /Y

:: todo: icon.ico und icon.png kopieren
copy icon.ico dist\icon.ico
copy icon.png dist\icon.png
