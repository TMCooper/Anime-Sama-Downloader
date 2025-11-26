import subprocess, sys, time, os

def main():
    # Petite pause pour s'assurer que le script original est terminé
    time.sleep(1)

    subprocess.run(["git", "fetch", "origin"]) # Prevoie le cas ou les utilisateur aurais fait des modification au code
    subprocess.run(["git", "reset", "--hard", "origin/main"]) # Rapatrie la dernière version du code

    script_principal = os.path.join(os.path.dirname(__file__), "..", "main.py")  # chemin relatif
    subprocess.Popen([sys.executable, script_principal])

if __name__ == "__main__":
    main()