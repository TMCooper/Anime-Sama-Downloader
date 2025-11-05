import os, yt_dlp, random, time, requests
from yt_dlp.utils import DownloadError
from function.Cardinal import *

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

    def download(url, PATH_DOWNLOAD, anime_name, anime_saison, version, ep_id, current_ep, languages, langue):
        
        FINAL_PATH = os.path.join(PATH_DOWNLOAD, anime_name, version, anime_saison)

        try:
            os.makedirs(FINAL_PATH, exist_ok=True)

            ydl_opts = {
                "format": "best",                                                   # Qualité vidéo maximale
                "outtmpl": os.path.join(FINAL_PATH, f"{ep_id}.mp4"),                # Nom du fichier de sortie
                "quiet": False,                                                     # Affiche les logs
                "http_headers": Yui.HEADERS,                                        # Header pour effectuer la requets
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            time.sleep(random.randint(3, 7)) # Rallentissement du code aleatoire pour evité un ban ip
            Cardinal.clearScreen()

        except DownloadError and KeyboardInterrupt as e:
            Cardinal.log_error(anime_name, anime_saison, current_ep, e, languages, langue)
            exit()

    def getLanguageFile():
        URL = "https://raw.githubusercontent.com/TMCooper/Anime-Sama-Downloader/refs/heads/main/ressources/languages/languages.json"

        reponse = requests.get(URL).json()
        # print(reponse)

        os.makedirs(Yui.PATH_LANGUAGE_FOLDER, exist_ok=True)
        time.sleep(0.003)
        with open(Yui.PATH_LANGUAGE, "w", encoding="utf-8") as f:
            json.dump(reponse, f, indent=4, ensure_ascii=False)