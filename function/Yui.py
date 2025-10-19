import os
import re
import shutil
import tempfile
from playwright.async_api import async_playwright


class Yui:
    """Classe pour la gestion du navigateur et de l'interception des flux M3U8"""
    
    @staticmethod
    def find_browser_profile():
        """Détecte et retourne le profil navigateur disponible (Edge ou Chrome)"""
        home_dir = os.path.expanduser('~')
        edge_path = os.path.join(home_dir, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data')
        chrome_path = os.path.join(home_dir, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
        
        if os.path.exists(edge_path):
            print(f"Profil Microsoft Edge détecté.")
            return edge_path, "msedge"
        elif os.path.exists(chrome_path):
            print(f"Profil Google Chrome détecté.")
            return chrome_path, "chrome"
        else:
            return None, None
    
    @staticmethod
    def extract_season_from_url(url):
        """Extrait le numéro de saison depuis l'URL"""
        match = re.search(r'saison(\d+)', url, re.IGNORECASE)
        if match:
            return int(match.group(1))
        else:
            print("Saison non détectée, utilisation de 'Saison 01' par défaut.")
            return 1
    
    @staticmethod
    def sanitize_filename(name):
        """Nettoie un nom de fichier des caractères interdits"""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()
    
    @staticmethod
    async def create_browser_context(user_data_path, channel):
        """Crée et retourne un contexte de navigateur avec profil temporaire"""
        p = async_playwright()
        playwright_instance = await p.start()
        
        # Créer un dossier temporaire pour le profil
        temp_profile = tempfile.mkdtemp(prefix="playwright_profile_")
        
        try:
            # Copier seulement les fichiers essentiels (cookies, etc.)
            default_profile = os.path.join(user_data_path, 'Default')
            temp_default = os.path.join(temp_profile, 'Default')
            os.makedirs(temp_default, exist_ok=True)
            
            # Copier les cookies si le fichier existe
            cookies_file = os.path.join(default_profile, 'Cookies')
            if os.path.exists(cookies_file):
                try:
                    shutil.copy2(cookies_file, os.path.join(temp_default, 'Cookies'))
                    print("Cookies copiés avec succès")
                except Exception as e:
                    print(f"Impossible de copier les cookies: {e}")
            
            # Lancer avec le profil temporaire
            context = await playwright_instance.chromium.launch_persistent_context(
                user_data_dir=temp_profile,
                headless=True,
                channel=channel,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            return playwright_instance, context
            
        except Exception as e:
            # Nettoyer en cas d'erreur
            shutil.rmtree(temp_profile, ignore_errors=True)
            raise e
    
    @staticmethod
    async def get_anime_info(page, url):
        """Récupère les informations de l'anime et la liste des épisodes"""
        print(f"Navigation vers la page : {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Récupération du titre
        anime_title_raw = await page.locator("#titreOeuvre").inner_text()
        anime_title = Yui.sanitize_filename(anime_title_raw).lower()
        
        # Récupération de la saison
        season_number = Yui.extract_season_from_url(url)
        
        print(f"Anime détecté : {anime_title} | Saison {season_number:02d}")
        
        # Récupération des épisodes
        episode_options = await page.locator("#selectEpisodes > option").all()
        episodes_to_download = []
        
        for option in episode_options:
            text = await option.inner_text()
            value = await option.get_attribute("value")
            match = re.search(r'\d+', text)
            if match:
                episodes_to_download.append({
                    "number": int(match.group(0)),
                    "text": text,
                    "value": value
                })
        
        print(f"{len(episodes_to_download)} épisodes trouvés.")
        
        return anime_title, season_number, episodes_to_download