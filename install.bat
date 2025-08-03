@echo off
REM Met un titre a la fenetre de la console
title Lanceur d'application Python

REM --- VERIFICATIONS ---
REM Verifie si le dossier de l'environnement virtuel existe
IF NOT EXIST ".\anime_sama\Scripts\activate.bat" (
    echo [ERREUR] Environnement virtuel 'anime_sama' introuvable.
    python -m venv anime_sama
)

REM Verifie si le fichier requirements.txt existe
IF NOT EXIST "requirements.txt" (
    echo [ERREUR] Le fichier 'requirements.txt' est introuvable.
    goto End
)

REM Verifie si le fichier main.py existe
IF NOT EXIST "Anime_Sama_Downloader.py" (
    echo [ERREUR] Le script principal 'Anime_Sama_Downloader.py' est introuvable.
    goto End
)

REM --- EXECUTION ---
echo [1/3] Activation de l'environnement virtuel...
REM L'appel a CALL permet d'executer le script d'activation dans la console actuelle
CALL .\anime_sama\Scripts\activate.bat

echo.
echo [2/3] Installation des dependances depuis requirements.txt...
pip install -r requirements.txt

REM Verifie si l'installation a reussi
IF %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] L'installation des dependances a echoue.
    goto End
)

echo.
echo --------------------------------------------------
echo.

:End
echo Le script est termine. Appuyez sur une touche pour quitter.
REM pause permet de garder la fenetre ouverte pour voir le resultat ou les erreurs
pause >nul