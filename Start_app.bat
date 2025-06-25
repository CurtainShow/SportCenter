@echo off
REM ————————————————————————————
REM 1) Se placer dans le répertoire de l'application
REM ————————————————————————————
cd /d "%USERPROFILE%\Desktop\CentreSportif-main"

REM ————————————————————————————
REM 2) Lancer Streamlit dans une nouvelle console
REM ————————————————————————————
start "Streamlit" cmd /c "streamlit run webserver.py"

REM ————————————————————————————
REM 3) Attendre le démarrage du serveur (~5 s)
REM    Ajustez la valeur si besoin
REM ————————————————————————————
timeout /t 5 /nobreak >nul

REM ————————————————————————————
REM 4) Ouvrir Chrome en plein écran sur localhost:8501
REM    Si Chrome n'est pas dans le PATH, spécifiez le chemin complet
REM    Exemple Edge : remplacez chrome par msedge et ajoutez --kiosk
REM ————————————————————————————
REM start "" "msedge" --start-fullscreen http://localhost:8501
REM start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --start-fullscreen http://localhost:8501

start "" "chrome" --start-fullscreen http://localhost:8501
