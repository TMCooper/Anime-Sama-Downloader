#!/bin/bash

# Met un titre a la fenetre du terminal (ne fonctionne pas sur tous les emulateurs de terminal)
echo -e "\033]2;Lanceur d'application Python\007"

# --- VERIFICATIONS ---
# Verifie si le dossier de l'environnement virtuel existe
if [ ! -f "./anime_sama/bin/activate" ]; then
    echo "[ERREUR] Environnement virtuel 'anime_sama' introuvable."
    # Crée l'environnement virtuel s'il n'existe pas
    python3 -m venv anime_sama
fi

# Verifie si le fichier requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "[ERREUR] Le fichier 'requirements.txt' est introuvable."
    exit 1
fi

# Verifie si le fichier main.py existe
if [ ! -f "Anime_Sama_Downloader.py" ]; then
    echo "[ERREUR] Le script principal 'Anime_Sama_Downloader.py' est introuvable."
    exit 1
fi

# --- EXECUTION ---
echo "[1/3] Activation de l'environnement virtuel..."
# source permet d'executer le script d'activation dans le shell actuel
source ./anime_sama/bin/activate

echo ""
echo "[2/3] Installation des dependances depuis requirements.txt..."
pip install -r requirements.txt

# Verifie si l'installation a reussi
if [ $? -ne 0 ]; then
    echo "[ERREUR] L'installation des dependances a echoue."
    exit 1
fi

echo ""
echo "[3/3] Lancement du script Python..."
python Anime_Sama_Downloader.py

echo ""
echo "--------------------------------------------------"
echo ""

echo "Le script est termine. Appuyez sur Entree pour quitter."
# read permet de garder la fenetre ouverte pour voir le resultat ou les erreurs
read