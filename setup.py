import os, subprocess, sys, platform

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_DOWNLOADER_REQUIREMENTS = os.path.join(PATH, "requirements.txt") # Pointe vers les dependence de l'api
PATH_API_REQUIREMENTS = os.path.join(PATH, r"AnimeSamaApi\requirements.txt") # Dependence du downloader

def setup_env(env_name="AnimeSamaEnv", requirements_file=PATH_API_REQUIREMENTS):
    # 1. Vérifier si le dossier d'environnement existe
    if not os.path.exists(env_name):
        print(f"Création de l'environnement virtuel '{env_name}'...")
        subprocess.run([sys.executable, "-m", "venv", env_name], check=True)
    else:
        print(f"L'environnement '{env_name}' existe déjà.")

    # 2. Déterminer le chemin vers le pip de l'environnement
    if platform.system() == "Windows":  # Windows
        pip_path = os.path.join(env_name, "Scripts", "pip.exe")
        python_path = os.path.join(env_name, "Scripts", "python.exe")
    elif platform.system() == ["Linux", "Darwin"]:  # Linux / macOS
        pip_path = os.path.join(env_name, "bin", "pip")
        python_path = os.path.join(env_name, "bin", "python3")

    # 3. Installer les dépendances
    if os.path.exists(requirements_file):
        print(f"Installation des dépendances depuis {requirements_file}...")
        # subprocess.run([pip_path, "install", "-r", PATH_DOWNLOADER_REQUIREMENTS], check=True)
        subprocess.run([pip_path, "install", "-r", PATH_API_REQUIREMENTS], check=True)
    else:
        print("Aucun fichier requirements.txt trouvé, installation ignorée.")

    print("Environnement prêt")
    return python_path


if __name__ == "__main__":
    python_env = setup_env()
    if os.name == "nt":
        print(r"Commande pour lancer votre env sous windows : .\AnimeSamaEnv\Scripts\activate")
    else:  # Linux / macOS
        print(r"Commande pour lancer votre env sous windows : .\AnimeSamaEnv\bin\activate")