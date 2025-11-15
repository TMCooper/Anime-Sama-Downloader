import platform, json, os
from InquirerPy import inquirer
from datetime import datetime

class Cardinal:
   
    SAISON_OPTIONS = ["saison", "film", "oav", "autre"]
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

class Utils:
    def debugPrint(args, ID=None, **kwargs):
        if args.debug:
            match ID:
                case 1:
                    print(f"[DEBUG] API : OK \n[DEBUG] IP : {kwargs.get('ip')} \n[DEBUG] Port : {kwargs.get('port')}")
                case 2:
                    print(f"[DEBUG] Langue : {kwargs.get('langue')} \n[DEBUG] Languages : {kwargs.get('languages')}")
                case 3:
                    print(f"[DEBUG] request http://{kwargs.get('ip')}:{kwargs.get('port')}/api/getAllAnime?r=True : OK")
                case 4:
                    print(f"[DEBUG] choixAnime : {kwargs.get('choixAnime')} \n[DEBUG] saison : {kwargs.get('saison')} \n[DEBUG] version : {kwargs.get('version')}")
                case 5:
                    print(f"[DEBUG] anime_data : {kwargs.get('anime_data')} \n[DEBUG] anime_name : {kwargs.get('anime_name')} \n[DEBUG] anime_saison : {kwargs.get('anime_saison')} \n[DEBUG] all_episodes : {kwargs.get('all_episodes')}")
                case 6:
                    print(f"[DEBUG] ep_num : {kwargs.get('ep_num')} \n[DEBUG] url : {kwargs.get('url')} \n[DEBUG] current_ep : {kwargs.get('current_ep')}, \n[DEBUG] ep_id : {kwargs.get('ep_id')}")
                case _:
                    print("Erreur, ID hors de l'index")