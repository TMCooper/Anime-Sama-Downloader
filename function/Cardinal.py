import requests
import os

class Cardinal:
    def last_requets(url, id, anime_name, anime_saison, languages, lang):

        headers = {
            "Host": "video.sibnet.ru",
            "Accept": "*/*",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Cookie": "sib_userid=1c11abe8766de830c84b3db0d7042769; OAID=745248aa553ce5209d4d5e908a9a5fda",
            "Range": "bytes=0-",
            "Referer": "https://video.sibnet.ru/shell.php?videoid=4673377",
            "Sec-Fetch-Dest": "video",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        response = requests.get(url, headers=headers)

        if not os.path.exists(f'dist/{anime_name}/{anime_saison}'):
                os.makedirs(f'dist/{anime_name}/{anime_saison}')

        with open(f'dist/{anime_name}/{anime_saison}/EP{id}.mp4', "wb") as f:
            f.write(response.content)
        
        print(languages[lang]["success_download"].format(title=anime_name, path=f'dist/{anime_name}/{anime_saison}/EP{id}.mp4'))