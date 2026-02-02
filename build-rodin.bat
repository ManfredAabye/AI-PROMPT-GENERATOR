@echo off

:: todo: RodinPromptGenerator.py to RodinPromptGenerator.exe

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
	echo PyInstaller wird installiert...
	pip install pyinstaller
)
echo Baue RodinPromptGenerator.exe ...
pyinstaller --onefile RodinPromptGenerator.py
echo Fertig! Die EXE befindet sich im dist-Ordner.
