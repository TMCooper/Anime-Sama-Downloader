from os import stat
import subprocess
import ctypes

EPISODE = "episodes.js?"

class Yui:
    @staticmethod
    def set_proxy(proxy_url):
        command = f'netsh winhttp set proxy proxy-server="{proxy_url}"'
        subprocess.run(command, shell=True)


    @staticmethod
    def reset_proxy():
        subprocess.run('netsh winhttp reset proxy', shell=True)

    @staticmethod
    def is_admin():
        # Vérifie si le script est exécuté avec les droits administratifs
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def construct(url, serv_file):
        url = url+EPISODE+serv_file
        return url
    

    @staticmethod
    def final_construct(video_id, ID):        
        return f'https://video.sibnet.ru/v/{video_id}/{ID}.mp4'
    

    @staticmethod
    def animes_search(url_anime_orrigin):
        return url_anime_orrigin.split("/")[-4]

    @staticmethod
    def saisons_search(url_saisons_orrigin):
        return url_saisons_orrigin.split("/")[-3]
