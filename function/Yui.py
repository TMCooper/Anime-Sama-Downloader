import subprocess
import ctypes
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

EPISODE = "/episodes.js?"

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
        base_url = 'https://video.sibnet.ru/v/'+video_id+"/"+f'{int(ID)}'+".mp4"
        # print(ID+".mp4")
        # print(base_url)
        return base_url
    
    def animes_search(url_anime_orrigin):
        return url_anime_orrigin.split("/")[-4]

    def saisons_search(url_saisons_orrigin):
        return url_saisons_orrigin.split("/")[-3]
    
    @staticmethod
    async def request(URL):
        async with async_playwright() as p:
            # Lancer le navigateur avec des options pour minimiser la détection
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-popup-blocking",
                    "--disable-web-security",
                    "--log-level=3",
                ]
            )

            # Créer une nouvelle page
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36"
            )
            page = await context.new_page()

            # Désactiver les traces de WebDriver avec du JavaScript
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """)

            # Charger la page
            await page.goto(URL)

            # Attendre que le contenu dynamique soit chargé
            await page.wait_for_selector('body')  # S'assurer que la page est complètement chargée

            # Récupérer le HTML après exécution du JavaScript
            page_source = await page.content()

            # Fermer le navigateur
            await browser.close()

            # Utilisation de BeautifulSoup pour parser le HTML
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup