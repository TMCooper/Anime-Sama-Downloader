import platform, json, os, subprocess, sys, shutil
from InquirerPy import inquirer
from datetime import datetime

PATH = os.getcwd()
PATH_STATS_FOLDER = os.path.join(PATH, "ressources", "Utils")
STATS_CHOICE_FILE = os.path.join(PATH_STATS_FOLDER, "statsChoice.json")

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
    
    @staticmethod
    def getStatsChoice(args, languages, langue): # Demande a l'utilisateur si il accèpte de participer ou non
        os.makedirs(PATH_STATS_FOLDER, exist_ok=True)
        if not os.path.isfile(STATS_CHOICE_FILE): # Faire ici aussi un system de log ? j'pense en vrai
            choix = Cardinal.ask(languages[langue]["statsChoice"], languages[langue]["YesNo"])
            if choix.lower() in ["yes", "oui"]:
                with open(STATS_CHOICE_FILE, "w", encoding='utf-8') as f:
                    data = [
                        {"choix": choix.lower()}
                        ]
                    json.dump(data, f, indent=4, ensure_ascii=False)
        
        with open(STATS_CHOICE_FILE, "r", encoding='utf-8') as data:
            data = json.load(data)

        choix = data[0]["choix"]
        if choix in ["yes", "oui"]:
            Utils.debugPrint(args, ID=8, etat="True")
            return True
        else:
            Utils.debugPrint(args, ID=8, etat="False")
            return False

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
                case 7:
                    print(f"[DEBUG] Local  : {kwargs.get('local_hash')} \n[DEBUG] Remote : {kwargs.get('remote_hash')}")
                case 8:
                    print(f"[DEBUG] choix : {kwargs.get('etat')}")
                case _:
                    print("Erreur, ID hors de l'index")

    def get_hash(ref):
        return subprocess.check_output(['git', 'rev-parse', ref]).decode().strip()

    def hashCheck(args, languages, langue):
        CHOIX_OPTIONS = languages[langue]["YesNo"]

        # Hash local
        local_hash = Utils.get_hash('HEAD')

        # Récupérer les infos du remote
        subprocess.run(['git', 'fetch'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Détecte la branche courante
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()

        # Hash distant
        remote_hash = Utils.get_hash(f'origin/{branch}')

        Utils.debugPrint(args, ID=7, local_hash=local_hash, remote_hash=remote_hash)

        if local_hash != remote_hash:
            reponse = Cardinal.ask(languages[langue]["checkUpdate"], CHOIX_OPTIONS)
            if reponse.lower() in ["yes", "oui"]:
                subprocess.run(["git", "reset", "--hard"], shell=True) # Prevoie le cas ou les utilisateur aurais fait des modification au code
                subprocess.run(["git", "pull", "origin", "main"], shell=True) # Rapatrie la dernière version du code
                os.execv(sys.executable, [sys.executable] + sys.argv) # Reboot le code une fois la mise a jour faite
            else:
                exit(1)

    def gitCheck(languages, langue):
        if shutil.which("git") is None:
            print(languages[langue]["gitCheck"])
            exit(1)
