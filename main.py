import time, os, requests, logging, argparse, queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor # Utilitaire de gestion pour le multi thread
from AnimeSamaApi.main import Api
from AnimeSamaApi.src.backend import PATH_DIR, PATH_ANIME # Pour verifier si le fichier AnimeInfo.json est bien la
from function.Yui import *
from function.Cardinal import *

PATH_DOWNLOAD = os.path.join(Yui.PATH, "Anime")
os.makedirs(PATH_DOWNLOAD, exist_ok=True)
VALIDE_LANGUAGE = ["FR", "ENG"]

def launchApi(args, port = 5000, ip="127.0.0.1"):
    Thread(target=Api.launch, kwargs={"port": port, "ip": ip,"debug_state": False, "reload_status": False}, daemon=True).start()
    Utils.debugPrint(args, ID=1, ip=ip, port=port)

def main():
    parser = argparse.ArgumentParser(
        description="Exemple de script avec arguments et options."
    )

    parser.add_argument("--debug", action="store_true", help="Active le mode débogage")
    parser.add_argument("-i","--ip", type=str,  help="Adresse IP souhaitée")
    parser.add_argument("-p", "--port", type=int, help="Port souhaité")
    
    args = parser.parse_args()
    
    port = args.port or 5000 # Si port est = None ou 0 alors il prendra la valeur de 5000
    ip = args.ip or "127.0.0.1" # Si ip est = None ou 0 alors elle prendra la valeur 127.0.0.1 
    
    if not os.path.isfile(Yui.PATH_LANGUAGE):
        Yui.getLanguageFile()
    
    launchApi(args, port=port, ip=ip)
    
    while True: # Boucle pour qu'une fois l'api prete on passe a la suite
        try:
            requests.get(f"http://{ip}:{port}/")  # Endpoint de test
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.25)
    
    if not args.debug:
        Cardinal.clearScreen()

    if not args.debug:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)  # Ne montre que les erreurs de l'api pour évité une polution inutile du prompt
    
    try:
        langue = Cardinal.ask("What is your language", VALIDE_LANGUAGE).lower() # Ancienne ligne # langue = input(f"What is your language {VALIDE_LANGUAGE} : ").lower().strip()
        languages = Cardinal.getLanguages(Yui.PATH_LANGUAGE)
        
        Utils.debugPrint(args, ID=2, langue=langue, languages=languages)
        Utils.gitCheck(languages, langue) # Vérifie l'installation corecte de git sur la machine
        Utils.hashCheck(args, languages, langue) # Vérifie la mise a jour du code
        statChoice = Cardinal.getStatsChoice(args, languages, langue) # Demande l'accord de l'utilisateur

        threadUserChoice = Cardinal.ask(languages[langue]["threadUserChoice"], Cardinal.THREAD_OPTIONS.get(langue))
        Utils.debugPrint(args, ID=9, threadUserChoice=threadUserChoice)

        threadUserChoice = threadUserChoice.lower() in Cardinal.TRUE_VALUES
        Utils.debugPrint(args, ID=10, threadUserChoice=threadUserChoice)

        try:
            thread_count_input = input(languages[langue]["threadCountAsk"])
            if not thread_count_input.strip():
                max_workers = 4
            else:
                max_workers = int(thread_count_input)
                Utils.debugPrint(args, ID=12, thread_count_input=thread_count_input)
                if max_workers < 1:
                    max_workers = 4
        except (ValueError, KeyError):
            max_workers = 4
        Utils.debugPrint(args, ID=13, max_workers=max_workers)

        # Vérification de l'existance du fichier AnimeInfo.json et si il existe pas recuperation de celui ci 
        os.makedirs(PATH_DIR, exist_ok=True)
        if not os.path.isfile(PATH_ANIME):
            print(languages[langue]["fileNotFound"])
            try:
                requests.get(f"http://{ip}:{port}/api/getAllAnime?r=True")
                Utils.debugPrint(args, ID=3, ip=ip, port=port)

            except Exception as e:
                print(languages[langue]["errorRequets"].format(erreur=e))
                exit(1)
        if not args.debug:
            Cardinal.clearScreen()

        choixAnime = input(languages[langue]["animeName"]).replace(" ", "%20") # le .replace Renplace les espace par des %20
        saison = Cardinal.ask(languages[langue]["typeAsk"], Cardinal.SAISON_OPTIONS) # Ancienne ligne # saison = input(languages[langue]["season"]).strip().lower().replace(" ", "") 

        if saison == "saison":
            saison_num = str(input(languages[langue]["season"]))
            if not saison_num:
                saison = saison + "1"
            else:
                saison = saison + saison_num
        if saison == "autre":
                saison = str(input(languages[langue]["otherSaisonChoice"]))

        version = Cardinal.ask(languages[langue]["version"], Cardinal.VERSION_OPTIONS) # Ancienne ligne # version = input(languages[langue]["version"]).strip().lower()

        Utils.debugPrint(args, ID=4, choixAnime=choixAnime, saison=saison, version=version) # Dédier au debug dans le cas ou saison et version n'affiche rien il valent la valeur que l'api leur donne donc saison1 et vostfr 

        while True:
            if not choixAnime:
                choixAnime = input(languages[langue]["forcedNameAnime"])
            else:
                anime_data = requests.get(f"http://{ip}:{port}/api/getSpecificAnime?q={choixAnime}&s={saison}").json()
                if anime_data is None: # Si notre api renvoie none c'est que l'actualisation de domaine a été effectué et donc qu'une actualisation de celle ci a été faite donc on retente juste après
                    anime_data = requests.get(
                        f"http://{ip}:{port}/api/getSpecificAnime?q={choixAnime}&s={saison}"
                    ).json()

                anime_name = anime_data["title"]
                anime_saison = anime_data["Saison"].strip().replace(" ", "").lower()

                all_episodes = requests.get(f"http://{ip}:{port}/api/getAnimeLink?n={choixAnime}&s={saison}&v={version}").json()
                Utils.debugPrint(args, ID=5, anime_data=anime_data, anime_name=anime_name, anime_saison=anime_saison, all_episodes=all_episodes)
                
                if statChoice == True:
                    total_episodes = max(ep["episode"] for ep in all_episodes) + 1
                    requests.get(f"https://animestats.fuyuki.me/api/stats?n={anime_name}&s={anime_saison}&e={total_episodes}") # Requeste l'api uniquement si l'utilisateur est d'accord
                
                break

        if all_episodes:
            # Préparation des data commune au deux boucle
            tasks = []
            for eps in all_episodes:
                current_ep = eps["episode"] + 1
                tasks.append({
                    "url": eps["url"],
                    "ep_id": f"Episode {current_ep}",
                    "current_ep": current_ep
                })
            
            Utils.debugPrint(args, ID=11, tasks=tasks)

            # Si threadUserChoice = true alors dans se cas on lance le téléchargement de 4 épisode en même temps
            if threadUserChoice:

                # Setup des slot pour l'UI spécifique au thread
                download_slots = queue.Queue()
                
                for i in range(max_workers):
                    download_slots.put(i)

                def download_wrapper(task_data):
                    slot = download_slots.get()
                    try:
                        Yui.download(task_data["url"], PATH_DOWNLOAD, anime_name, anime_saison, version, task_data["ep_id"], task_data["current_ep"], languages, langue, slot_index=slot, total_slots=max_workers)
                    finally:
                        download_slots.put(slot)

                print("\n" * max_workers) # Reserve lines
                Cardinal.clearScreen()
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    for download in tasks:
                        Utils.debugPrint(args, ID=6, url=download["url"], current_ep=download["current_ep"], ep_id=download["ep_id"])
                        executor.submit(download_wrapper, download)
                Cardinal.clearScreen()
            
            # Sinon on le fait un par un
            else:
                for download in tasks:
                    Utils.debugPrint(args, ID=6, url=download["url"], current_ep=download["current_ep"], ep_id=download["ep_id"])
                    Yui.download(download["url"], PATH_DOWNLOAD, anime_name, anime_saison, version, download["ep_id"], download["current_ep"], languages, langue)

    except KeyboardInterrupt:
        print("\nShutdown...")
        time.sleep(0.65)
        if not args.debug:
            Cardinal.clearScreen()
            exit(1)

    except TypeError:
        print(languages[langue]["BadInformation"].format(choixAnime=choixAnime.replace("%20", " "), saison=saison, version=version))
        exit(1)

    except Exception as e: # Gestion des erreur tty lier au InquirerPy
        print(languages[langue]["ErrorException"].format(e=e))
        pass

if __name__ == "__main__":
    main()