import subprocess
import ctypes

EPISODE = "episodes.js?"

class Yui:
    def set_proxy(proxy_url):
        command = f'netsh winhttp set proxy proxy-server="{proxy_url}"'
        subprocess.run(command, shell=True)

    def reset_proxy():
        subprocess.run('netsh winhttp reset proxy', shell=True)

    def is_admin():
        # Vérifie si le script est exécuté avec les droits administratifs
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def construct(url, serv_file):
        url = url+EPISODE+serv_file
        return url
    
    def final_construct(video_id, ID):        
        return f'https://video.sibnet.ru/v/{video_id}/{ID}.mp4'
    
    def animes_search(url_anime_orrigin):
        return url_anime_orrigin.split("/")[-4]

    def saisons_search(url_saisons_orrigin):
        return url_saisons_orrigin.split("/")[-3]