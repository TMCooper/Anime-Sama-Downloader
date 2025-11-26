import subprocess, sys, time

# Petite pause pour s'assurer que le script original est terminé
time.sleep(1)

subprocess.run(["git", "fetch", "origin"]) # Prevoie le cas ou les utilisateur aurais fait des modification au code
subprocess.run(["git", "reset", "--hard", "origin/main"]) # Rapatrie la dernière version du code

subprocess.Popen([sys.executable] + sys.argv) # Reboot le code une fois la mise a jour faite