import platform, json, os
from InquirerPy import inquirer
from datetime import datetime

class Cardinal:
   
    SAISON_OPTIONS = ["saison", "film", "oav"]
    VERSION_OPTIONS = ["vostfr", "vf"]

    OUTPUT_DIRECTORY = "Logs"
    
    @staticmethod # Normalement fonctionelle dans mais peut être voir si dans le cas ou on ne trouve rien pour savoir au moins a quel espisode on est ?
    def log_error(anime_title, anime_saison, episode_number, error, languages, langue):
        """Enregistre les erreurs dans un fichier de log"""
        os.makedirs(Cardinal.OUTPUT_DIRECTORY, exist_ok=True)
        log_file = os.path.join(Cardinal.OUTPUT_DIRECTORY, "error_log.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        season_num = int(''.join(filter(str.isdigit, anime_saison)))

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(languages[langue]["cardinalLogs"].format(timestamp=timestamp, anime_title=anime_title, anime_saison=f"{season_num:02d}", episode_number=f"{episode_number:02d}", error=error))

    @staticmethod
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
    
    @staticmethod
    def ask(question, options):
        choix = inquirer.select(
            message=question,
            choices=options
            ).execute()
        return choix
