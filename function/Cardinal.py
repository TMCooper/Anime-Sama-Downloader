import os
import subprocess
import platform


class Cardinal:
    def last_requets(url, id, anime_name, anime_saison):

        # Commande curl à exécuter

        if not os.path.exists(f'dist/{anime_name}/{anime_saison}'):
                os.makedirs(f'dist/{anime_name}/{anime_saison}')
        
        # Chemin du fichier de sortie
        output_file = f'dist/{anime_name}/{anime_saison}/EP{id}.mp4'

        # Commande curl à exécuter
        command = [
            "curl", "--location", f'{url}',
            "--header", "Accept: */*",
            "--header", "Accept-Encoding: identity;q=1, *;q=0",
            "--header", "Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "--header", "Connection: keep-alive",
            "--header", "Cookie: sib_userid=1c11abe8766de830c84b3db0d7042769; OAID=745248aa553ce5209d4d5e908a9a5fda",
            "--header", "Host: video.sibnet.ru",
            "--header", "Range: bytes=0-",
            "--header", f"Referer: https://video.sibnet.ru/shell.php?videoid={id}",
            "--header", "Sec-Fetch-Dest: video",
            "--header", "Sec-Fetch-Mode: no-cors",
            "--header", "Sec-Fetch-Site: same-origin",
            "--header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0",
            "--header", 'sec-ch-ua: "Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            "--header", "sec-ch-ua-mobile: ?0",
            "--header", 'sec-ch-ua-platform: "Windows"',
            "--output", output_file  # Enregistrer vers le fichier de sortie
        ]

        # Exécuter la commande avec subprocess
        subprocess.run(command)

        os_name = platform.system()

        if os_name == "Windows":
            subprocess.run("cls", shell=True)
        elif os_name == "Linux" or "Darwin":
            subprocess.run("clear", shell=True)