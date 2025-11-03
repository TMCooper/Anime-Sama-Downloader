import os
import platform
from datetime import datetime


class Cardinal:
   
    OUTPUT_DIRECTORY = "Anime"
    
    @staticmethod
    def log_error(anime_title, season_number, episode_number, error, langue):
        """Enregistre les erreurs dans un fichier de log"""
        os.makedirs(Cardinal.OUTPUT_DIRECTORY, exist_ok=True)
        log_file = os.path.join(Cardinal.OUTPUT_DIRECTORY, "error_log.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Échec pour {anime_title} - S{season_number:02d}E{episode_number:02d}: {error}\n")

    @staticmethod  # <-- Ajouté ici
    def clearScreen():
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == ["Linux", "Darwin"]:
            os.system("clear")