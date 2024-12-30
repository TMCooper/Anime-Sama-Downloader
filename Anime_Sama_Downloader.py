from function.__init__ import *
import requests
import json
import re

def main():

    try:

        valid_languages = ["en", "fr"]

        with open('languages.json', 'r') as lang_file:
            languages = json.load(lang_file)

        print(f"Available languages: {', '.join(valid_languages).upper()}")
        lang = input("What is your language ? : ").lower()

        while lang not in valid_languages:
            print(f"Available languages: {', '.join(valid_languages).upper()}")
            lang = input("Please select your language: ").lower()

        # URL cible
        print(languages[lang]["Exit_q"])
        url_anime_orrigin = input(languages[lang]["url_question"])

        url_ru = ""

        # Faire une requête GET à l'URL sans headers
        response = requests.get(url_anime_orrigin)

        # Vérifier si la requête a réussi
        if response.status_code == 200:

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }

            content = response.text
            serv_file = content.split("episodes.js?")[1].split("'")[0]

            url_ru = Yui.construct(url_anime_orrigin, serv_file)
            # print(url_ru)
            reponse = requests.get(url_ru)
            # retaper la manière dont les url son récupérer avec pour ojbectif de aire en sorte que cela fonctione a tous les coup peut importe sa position au moment du get sur les lien sib
            
            url_episodes = reponse.text
            # print(url_episodes)
            url_episode = url_episodes
            # print (f'url_episode avant split : {url_episode}')
            url_episodes = re.findall(r"'(https://video\.sibnet\.ru/shell\.php\?videoid=\d+)'", url_episodes)
            # print(f'url_episodes après split : {url_episodes}')
            
            i = 0
            for url_episode in url_episodes:
                if not "videoid=" in url_episode:
                    continue
                print(f'url_episode {i} : {url_episode}')
                i += 1
                ID = url_episode.split("videoid=")[1]
                # print(ID)

                video = requests.get(url_episode, headers=headers, timeout=30)
                # print(video)
                video_html = video.text
                # print(video_html)
                video_id = video_html.split(f'/v/')[1].split('/')[0]
                Cardinal.last_requets(Yui.final_construct(video_id, ID), i, Yui.animes_search(url_anime_orrigin), Yui.saisons_search(url_anime_orrigin), ID)

        else:
            print(f"Erreur lors de la requête : {response.status_code}")
        
    except KeyboardInterrupt:
        print(languages[lang]["keyboard_interupt"])

if __name__ == "__main__":
    main()