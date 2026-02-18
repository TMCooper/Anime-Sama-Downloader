import os, yt_dlp, random, time, requests, sys, shutil, threading
import colorama
from colorama import Cursor
from yt_dlp.utils import DownloadError
from function.Cardinal import *

colorama.init()
print_lock = threading.Lock()

class Yui:

    PATH = os.getcwd()
    PATH_LANGUAGE_FOLDER = os.path.join(PATH, "ressources", "languages")
    PATH_LANGUAGE = os.path.join(PATH_LANGUAGE_FOLDER, "languages.json")

    HEADERS = {
        'authority': 'p16-ad-sg.tiktokcdn.com',
        'method': 'GET',
        'path': '/obj/ad-site-i18n-sg/202508125d0d6bceedbe1123419c9459',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,de;q=0.5,zh-CN;q=0.4,zh;q=0.3,ru;q=0.2,es;q=0.1,ko;q=0.1,vi;q=0.1,pl;q=0.1',
        'cache-control': 'no-cache',
        'origin': 'https://smoothpre.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://smoothpre.com/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Opera GX";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0',
        }

    def download(url, PATH_DOWNLOAD, anime_name, anime_saison, version, ep_id, current_ep, languages, langue, slot_index=None, total_slots=4):
        
        FINAL_PATH = os.path.join(PATH_DOWNLOAD, anime_name, version, anime_saison)

        try:
            cleanLogger = YuiCleanLogger(languages, langue, slot_index, total_slots)

            os.makedirs(FINAL_PATH, exist_ok=True)

            ydl_opts = {
                "format": "best",                                                                           # Qualité vidéo maximale
                "outtmpl": os.path.join(FINAL_PATH, f"{ep_id}.mp4"),                                        # Nom du fichier de sortie
                "quiet": False,                                                                             # N'affiche pas les logs
                "no_warning": True,                                                                         # Supprime les warnings
                "logger": cleanLogger,                                                                      # Logger personalisé
                "progress_hooks": [cleanLogger.hook],                                                       # Pour un affichage personnalisé de la progression
                "http_headers": Yui.HEADERS,                                                                # Header pour effectuer la requets
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            time.sleep(random.randint(3, 7)) # Rallentissement du code aleatoire pour evité un ban ip
            
            if slot_index is None:
                Cardinal.clearScreen()

        except (DownloadError, KeyboardInterrupt) as e:
            Cardinal.log_error(anime_name, anime_saison, current_ep, e, languages, langue)
            exit()

    def getLanguageFile():
        URL = "https://raw.githubusercontent.com/TMCooper/Anime-Sama-Downloader/refs/heads/main/ressources/languages/languages.json"

        reponse = requests.get(URL).json()

        os.makedirs(Yui.PATH_LANGUAGE_FOLDER, exist_ok=True)
        time.sleep(0.003)
        with open(Yui.PATH_LANGUAGE, "w", encoding="utf-8") as f:
            json.dump(reponse, f, indent=4, ensure_ascii=False)


class YuiCleanLogger:
    def __init__(self, languages, langue, slot_index=None, total_slots=4):
        self.path_printed = False
        self.languages = languages
        self.langue = langue
        self.slot_index = slot_index
        self.total_slots = total_slots

    def debug(self, msg):
        # print(msg) # A décommentez pour le débug
        pass # Ignore les messages de type '[info]', '[generic]', etc.

    def warning(self, msg):
        # print(msg) # A  décommentez pour voir les avertissements
        pass # Ignore les avertissements

    def error(self, msg):
        if self.slot_index is not None:
            with print_lock:
                 # Best effort error printing in threaded mode
                sys.stdout.write(f"\nError in thread {self.slot_index}: {msg}\n")
        else:
            print(msg)

    def hook(self, d):
        try:
            # Récupère la largeur actuelle du terminal
            terminal_width = shutil.get_terminal_size().columns
        except OSError:
                # Largeur par défaut pour éviter les crashes    
            terminal_width = 80

        if d['status'] == 'downloading':
            # La ligne de progression qui se met à jour
            progress_line = (
                f"[download] {d['_percent_str']} of {d.get('total_bytes_str', 'N/A')}"
                f" at {d['_speed_str']} ETA {d['_eta_str']}"
            )
            
            if self.slot_index is not None:
                # In threaded mode, prepend filename short version to know what is downloading
                filename = os.path.basename(d['filename'])
                if len(filename) > 15:
                    filename = filename[:12] + "..."
                progress_line = f"{filename}: {progress_line}"
                
                # Truncate to fit terminal
                line_to_write = f"\r{progress_line:<{terminal_width - 1}}"
                
                with print_lock:
                    sys.stdout.write(Cursor.UP(self.total_slots - self.slot_index))
                    sys.stdout.write(line_to_write)
                    sys.stdout.write(Cursor.DOWN(self.total_slots - self.slot_index))
                    sys.stdout.flush()
            else:
                if not self.path_printed:
                    print(f"Destination: {d['filename']}")
                    self.path_printed = True
            
                line_to_write = f"\r{progress_line:<{terminal_width - 1}}"
                sys.stdout.write(line_to_write) 
                sys.stdout.flush()

        if d['status'] == 'finished':
            if self.slot_index is not None:
                filename = os.path.basename(d['filename'])
            else:
                # Réinitialise la variable pour le prochain fichier à télécharger
                self.path_printed = False