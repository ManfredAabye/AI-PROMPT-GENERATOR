@echo off

@REM Baut UniversalPromptManager.py zu UniversalPromptManager.exe

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
	echo PyInstaller wird installiert...
	pip install pyinstaller
)
echo Baue UniversalPromptManager.exe ...
pyinstaller --onefile UniversalPromptManager.py
echo Fertig! Die EXE befindet sich im dist-Ordner.

