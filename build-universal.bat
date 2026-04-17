@echo off

@REM Baut UniversalPromptManager.py zu UniversalPromptManager.exe

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
	echo PyInstaller wird installiert...
	pip install pyinstaller
)
echo Baue UniversalPromptManager.exe ...
pyinstaller --onefile --icon=icon.ico --add-data "icon.png;." --add-data "icon.ico;." UniversalPromptManager.py
echo Fertig! Die EXE befindet sich im dist-Ordner.

:: languages.json kopieren
copy upmlanguages.json dist\upmlanguages.json

:: Verzeichnis categories kopieren
xcopy categories dist\categories /E /I /Y

:: todo: icon.ico und icon.png kopieren
copy icon.ico dist\icon.ico
copy icon.png dist\icon.png
