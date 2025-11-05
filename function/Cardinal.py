import platform, json, os
from datetime import datetime

class Cardinal:
   
    OUTPUT_DIRECTORY = "Anime"
    
    @staticmethod # Normalement fonctionelle dans mais peut être voir si dans le cas ou on ne trouve rien pour savoir au moins a quel espisode on est ?
    def log_error(anime_title, season_number, episode_number, error, languages, langue):
        """Enregistre les erreurs dans un fichier de log"""
        os.makedirs(Cardinal.OUTPUT_DIRECTORY, exist_ok=True)
        log_file = os.path.join(Cardinal.OUTPUT_DIRECTORY, "error_log.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(languages[langue]["cardinalLogs"].format(timestamp=timestamp, anime_title=anime_title, season_number=f"{season_number:02d}", episode_number=f"{episode_number:02d}", error=error))

    @staticmethod  # <-- Ajouté ici
    def clearScreen():
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() in ["Linux", "Darwin"]:
            os.system("clear")

    @staticmethod
    def getLanguages(PATH_LANGUAGE):
        with open(PATH_LANGUAGE, "r", encoding='utf-8') as data:
            languages = json.load(data)

        return languages
