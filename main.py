# TODO
# Intégration du system de langue et peut être gerer plus d'erreur typiquement quand on tape mal le nom y a une erreur

import time, os, requests, logging
from threading import Thread
from AnimeSamaApi.main import Api
from AnimeSamaApi.src.backend import PATH_DIR, PATH_ANIME # Pour verifier si le fichier AnimeInfo.json est bien la
from function.Yui import *
from function.Cardinal import *

PATH_DOWNLOAD = os.path.join(Yui.PATH, "Anime")
os.makedirs(PATH_DOWNLOAD, exist_ok=True)
VALIDE_LANGUAGE = "[FR, ENG]"

def launchApi():
    Thread(target=Api.launch, kwargs={"port": 5000,"debug_state": False, "reload_status": False}, daemon=True).start()
    # print("API launched successfully (running in background)")

def main():
    launchApi()
    time.sleep(0.003)
    Cardinal.clearScreen()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Ne montre que les erreurs de l'api pour évité une polution inutile du prompt
    
    try:
        if not os.path.isfile(Yui.PATH_LANGUAGE):
            Yui.getLanguageFile()

        langue = input(f"What is your language {VALIDE_LANGUAGE} : ").lower().strip()
        while True:
            if langue in ["fr", "eng"]:
                languages = Cardinal.getLanguages(Yui.PATH_LANGUAGE)
                break
            else:
                langue = input(f"Please select one of the actual list {VALIDE_LANGUAGE} : ")

        # Ne pas oublier d'implementé la fonction de lecture du fichier languages.json
        # Vérification de l'existance du fichier AnimeInfo.json et si il existe pas creation de celui ci 
        os.makedirs(PATH_DIR, exist_ok=True)
        if not os.path.isfile(PATH_ANIME):
            print(languages[langue]["fileNotFound"])
            try:
                requests.get("http://127.0.0.1:5000/api/getAllAnime?r=True")
            except Exception as e:
                print(languages[langue]["errorRequets"].format(erreur=e))
                exit()
        Cardinal.clearScreen()


        choixAnime = input(languages[langue]["animeName"]).replace(" ", "%20") # le .replace Renplace les espace par des %20
        saison = input(languages[langue]["season"]).strip().lower().replace(" ", "")
        version = input(languages[langue]["version"]).strip().lower()

        # print(f"Anime request : {choixAnime}, saison : {saison}, version : {version}") # Dédier au debug dans le cas ou saison et version n'affiche rien il valent la valeur que l'api leur donne donc saison1 et vostfr 

        while True:
            if not choixAnime:
                choixAnime = input(languages[langue]["forcedNameAnime"])
            else:
                anime_data = requests.get(f"http://127.0.0.1:5000/api/getSpecificAnime?q={choixAnime}&s={saison}").json()
                anime_name = anime_data["title"]
                anime_saison = anime_data["Saison"].strip().replace(" ", "").lower()

                all_episodes = requests.get(f"http://127.0.0.1:5000/api/getAnimeLink?n={choixAnime}&s={saison}&v={version}").json()
                # print(all_episodes)
                break

        if not version:
            version = "vostfr"
            # print(version)
        else:
            version = version.replace(" ", "").strip().lower()

        if all_episodes:

            # print(anime_name)
            # print(anime_saison)
            
            for eps in all_episodes:
                ep_num = eps["episode"]
                url = eps["url"]
                current_ep = ep_num + 1 # current_ep numero de l'épisode le plus 1 c'est pour tous décaler correctement et eviter les episode 0
                ep_id = f"Episode {current_ep}" # Creation du nom de fichier
                

                Yui.download(url, PATH_DOWNLOAD, anime_name, anime_saison, version, ep_id, current_ep, languages, langue)
                # print(ep_id, url)
                # print(FINAL_PATH)

    except KeyboardInterrupt:
        print("\nShutdown...")
        time.sleep(0.5)
        # Cardinal.clearScreen() # A rajouté plus tard ?

if __name__ == "__main__":
    main()