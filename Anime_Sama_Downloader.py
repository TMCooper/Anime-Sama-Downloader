from function.__init__ import *
import requests
import json


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

        # url_anime_orrigin = "https://anime-sama.fr/catalogue/komi-cant-communicate/saison1/vostfr/"
        url_anime_orrigin = "https://anime-sama.fr/catalogue/konosuba/saison1/vostfr/"
        url_ru = ""

        # Faire une requête GET à l'URL sans headers
        response = requests.get(url_anime_orrigin)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            content = response.text
            serv_file = content.split("episodes.js?")[1].split("'")[0]

            url_ru = Yui.construct(url_anime_orrigin, serv_file)
            # print(url_ru)
            reponse = requests.get(url_ru)
            url_episodes = reponse.text
            # print(url_episodes)
            url_episode = url_episodes
            url_episodes = url_episodes.replace("'", "").replace(",", "").split('var')[1].split('\n')[1:-4]
            # print(url_episodes)
            
            i = 0
            for url_episode in url_episodes:
                # print(f'url_episode {i} : {url_episode}')
                i += 1
                ID = url_episode.split("videoid=")[1]

                video = requests.get(url_episode)
                video_html = video.text
                video_id = video_html.split(f'/{ID}')[0].split('/')[-1]
                # print(video_id)
                Cardinal.last_requets(Yui.final_construct(video_id, ID), i, Yui.animes_search(url_anime_orrigin), Yui.saisons_search(url_anime_orrigin), languages, lang)

        else:
            print(f"Erreur lors de la requête : {response.status_code}")
        
    except KeyboardInterrupt:
        print(languages[lang]["keyboard_interupt"])

if __name__ == "__main__":
    main()