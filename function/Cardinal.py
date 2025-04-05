import os
import subprocess
import platform


class Cardinal:
    def last_requets(url, id, anime_name, anime_saison, ID):

        # Commande curl à exécuter

        if not os.path.exists(f'dist/{anime_name}/{anime_saison}'):
                os.makedirs(f'dist/{anime_name}/{anime_saison}')
        
        # Chemin du fichier de sortie
        output_file = f'dist/{anime_name}/{anime_saison}/EP{id}.mp4'

        # print(url)

        # Commande curl à exécuter
        command = [
            "curl", "--location", f'{url}',
            "--header", "Accept: */*",
            "--header", "Accept-Encoding: identity;q=1, *;q=0",
            "--header", "Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "--header", "Cache-Control: no-cache",
            "--header", "Connection: keep-alive",
            "--header", "Cookie: sib_userid=fd3787da2292a48bc8e39cb536ed1b20",
            "--header", "Host: dv26-2.sibnet.ru",
            "--header", "Pragma: no-cache",
            "--header", "Range: bytes=0-",
            "--header", "Referer: https://video.sibnet.ru/",
            "--header", "Sec-Fetch-Dest: video",
            "--header", "Sec-Fetch-Mode: no-cors",
            "--header", "Sec-Fetch-Site: same-site",
            "--header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0",
            "--header", 'sec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132", "Opera GX";v="117"',
            "--header", "sec-ch-ua-mobile: ?0",
            "--header", 'sec-ch-ua-platform: "Windows"',
            "--output", output_file
        ]

        # Exécuter la commande avec subprocess
        subprocess.run(command, shell=True)

        os_name = platform.system()

        if os_name == "Windows":
            subprocess.run("cls", shell=True)
        elif os_name == "Linux" or "Darwin":
            subprocess.run("clear", shell=True)