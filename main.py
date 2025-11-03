# [
#   {
#     "episode": 0,
#     "url": "https://video.sibnet.ru/shell.php?videoid=4692676"
#   },
# ]

# http://127.0.0.1:5000/api/getAnimeLink?n=youjo%20senki

# TODO
# Intégration du system de langue et peut être gerer plus d'erreur typiquement quand on tape mal le nom y a une erreur
# List a tester avec ou sans variation dans le nom : Youjo Senki, Spice And Wolf (remake 2024 aussi), Frieren, Assassination classroom,  

import time, os, requests, logging
from threading import Thread
from AnimeSamaApi.main import Api
from AnimeSamaApi.src.backend import PATH_DIR, PATH_ANIME # Pour verifier si le fichier AnimeInfo.json est bien la
from function.Yui import *

PATH = os.getcwd()
PATH_DOWNLOAD = os.path.join(PATH, "Anime")
PATH_LANGUAGE = os.path.join(PATH, "ressources", "languages", "languages.json")
os.makedirs(PATH_DOWNLOAD, exist_ok=True)

def launchApi():
    Thread(target=Api.launch, kwargs={"port": 5000,"debug_state": False, "reload_status": False}, daemon=True).start()
    print("API launched successfully (running in background)")

def main():
    launchApi()
    time.sleep(0.003)
    Cardinal.clearScreen()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Ne montre que les erreurs de l'api pour évité une polution inutile du prompte

    # Vérification de l'existance du fichier AnimeInfo.json et si il existe pas creation de celui ci 
    os.makedirs(PATH_DIR, exist_ok=True)
    if not os.path.isfile(PATH_ANIME):
        print("Fichier introuvable, récupération des données... Cela peut prendre un certain temps merci de votre patience...")
        try:
            requests.get("http://127.0.0.1:5000/api/getAllAnime?r=True")
        except Exception as e:
            print("Erreur lors de la requête :", e)

    Cardinal.clearScreen()
    
    try:
        if not os.path.isfile(PATH_LANGUAGE):
            print(f"Le module languages.json est manquant merci de le télécharger et de le ranger ici : {PATH_LANGUAGE}")
            exit()

        langue = input("What is your language [FR, ENG] : ").lower()
        while True:
            if langue in ["fr", "eng"]:
                print(langue)
                break
            else:
                langue = input("Please select one of the actual list [FR, ENG] : ")

        # Ne pas oublier d'implementé la fonction de lecture du fichier languages.json

        choixAnime = input("Quel est le nom de votre animer ? : ").replace(" ", "%20") # le .replace Renplace les espace par des %20
        saison = input("Quel saison voulez vous ? (exemple Saison 1, Film, etc...) (Par défaut c'est la saison 1 qui est prise) : ").strip().lower().replace(" ", "")
        version = input("Quel version voulez vous ? (exemple vostfr) (Par défaut c'est le vostfr qui est pris) : ").strip().lower()
        # anime = re.sub(r"\s+", '%20', choixAnime) 

        # print(f"Anime request : {choixAnime}, saison : {saison}, version : {version}") # Dédier au debug dans le cas ou saison et version n'affiche rien il valent la valeur que l'api leur donne donc saison1 et vostfr 

        while True:
            if not choixAnime:
                choixAnime = input("Velliez écrire le nom de votre anime : ")
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
                

                Yui.download(url, PATH_DOWNLOAD, anime_name, anime_saison, version, ep_id, langue)
                # print(ep_id, url)
                # print(FINAL_PATH)

    except KeyboardInterrupt:
        print("\nShutdown...")

if __name__ == "__main__":
    main()