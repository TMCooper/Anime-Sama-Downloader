import asyncio, os, subprocess, shutil
from playwright.async_api import async_playwright
from function.Yui import Yui
from function.Cardinal import Cardinal

async def main():

    # Vérifie si le navigateur est installé, sinon l'installe
    playwright_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "ms-playwright")
    if not os.path.exists(os.path.join(playwright_dir, "chromium-")):
        subprocess.run(["playwright", "install", "chromium"], check=True)

    print("Démarrage du script de téléchargement de saison...\n")
    
    browser_user_data_path, browser_channel = Yui.find_browser_profile()
    if not browser_user_data_path:
        print("Aucun profil navigateur détecté.")
        return
    
    url = input("Veuillez coller l'URL de la page : ")
    if not url.startswith('http'):
        print("URL invalide.")
        return
    
    print("\n--- IMPORTANT ---")
    print(f"Le script va utiliser votre profil {browser_channel.title()}. Fermez toutes ses fenêtres.")
    input("Appuyez sur Entrée lorsque c'est fait...")
    Cardinal.cleanscreen()

    
    default_profile = os.path.join(browser_user_data_path, "Default")
    custom_profile = os.path.join(playwright_dir, "playwright_profile")

    os.makedirs(custom_profile, exist_ok=True)
    
    async with async_playwright() as p:
        context = None
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=browser_user_data_path,
                headless=True,
                channel=browser_channel,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            )
            page = await context.new_page()
            
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """)
            
            anime_title, season_number, episodes_to_download = await Yui.get_anime_info(page, url)
            
            m3u8_by_episode = {}
            captured_urls = set()
            new_m3u8_event = asyncio.Event()
            pending_m3u8_data = None

            def filter_headers(headers):
                return {k: v for k, v in headers.items() if not k.startswith(':')}

            async def intercept_request(request):
                nonlocal pending_m3u8_data
                if "master.m3u8" in request.url:
                    if request.url not in captured_urls:
                        raw_headers = await request.all_headers()
                        clean_headers = filter_headers(raw_headers)
                        pending_m3u8_data = {"url": request.url, "headers": clean_headers}
                        captured_urls.add(request.url)
                        new_m3u8_event.set()

            page.on("request", intercept_request)
            
            # --- Capture de l'épisode initial ---
            print(f"\nPhase 0 : Capture de l'épisode initialement chargé...")
            try:
                initial_episode_text = await page.evaluate("document.querySelector('#selectEpisodes').value")
                print(f"Page chargée sur : '{initial_episode_text}'. Attente de son M3U8...")
                
                new_m3u8_event.clear()
                await asyncio.wait_for(new_m3u8_event.wait(), timeout=30)
                
                if pending_m3u8_data:
                    m3u8_by_episode[initial_episode_text] = pending_m3u8_data
                    print(f"M3U8 de '{initial_episode_text}' stocké (total: 1)")
                    pending_m3u8_data = None
                else:
                    print(f"M3U8 pour l'épisode initial non détecté à temps.")

            except asyncio.TimeoutError:
                print(f"Timeout : Le M3U8 de l'épisode initial n'a pas été capturé.")
            except Exception as e:
                print(f"Erreur lors de la capture initiale : {e}")

            print(f"\nPhase 1 : Collecte des données M3U8 pour les autres épisodes...\n")
            
            try:
                for episode in episodes_to_download:
                    ep_num, ep_text = episode["number"], episode["text"]
                    
                    if ep_text in m3u8_by_episode:
                        print(f"{ep_text} déjà capturé, passage au suivant")
                        continue
                    
                    print(f"--- Collecte : {ep_text} ---")
                    
                    success = False
                    MAX_RETRIES = 3
                    for attempt in range(1, MAX_RETRIES + 1):
                        if attempt > 1:
                            print(f"Tentative {attempt}/{MAX_RETRIES}...")
                        
                        new_m3u8_event.clear()
                        
                        try:
                            # === CLIC PHYSIQUE AVEC COORDONNÉES ===
                            await page.bring_to_front()
                            
                            # Obtenir la position du select et cliquer physiquement dessus
                            select_box = await page.locator("#selectEpisodes").bounding_box()
                            if select_box:
                                # Cliquer au centre du select (comme un humain)
                                await page.mouse.click(
                                    select_box['x'] + select_box['width'] / 2,
                                    select_box['y'] + select_box['height'] / 2
                                )
                                await asyncio.sleep(0.5)

                            current_text = await page.evaluate("document.querySelector('#selectEpisodes').value")
                            all_texts = [ep["text"] for ep in episodes_to_download]
                            current_index = all_texts.index(current_text) if current_text in all_texts else 0
                            target_index = all_texts.index(ep_text)
                            steps = target_index - current_index

                            # Navigation avec les flèches
                            if steps > 0:
                                for _ in range(steps):
                                    await page.keyboard.press("ArrowDown")
                                    await asyncio.sleep(0.2)
                            elif steps < 0:
                                for _ in range(abs(steps)):
                                    await page.keyboard.press("ArrowUp")
                                    await asyncio.sleep(0.2)

                            await asyncio.sleep(2)

                            # Vérifier qu'on est sur le bon épisode
                            selected_episode = await page.evaluate("document.querySelector('#selectEpisodes').value")
                            if selected_episode != ep_text:
                                # Fallback JavaScript
                                await page.evaluate(f"""
                                    const select = document.querySelector('#selectEpisodes');
                                    select.value = '{ep_text}';
                                    select.dispatchEvent(new Event('change', {{bubbles: true}}));
                                    select.dispatchEvent(new Event('input', {{bubbles: true}}));
                                """)
                                await asyncio.sleep(2)
                                selected_episode = await page.evaluate("document.querySelector('#selectEpisodes').value")

                            if selected_episode == ep_text:
                                print(f"Attente du M3U8...")
                                await asyncio.wait_for(new_m3u8_event.wait(), timeout=30)
                                if pending_m3u8_data:
                                    m3u8_by_episode[ep_text] = pending_m3u8_data
                                    print(f"M3U8 stocké (total: {len(m3u8_by_episode)})")
                                    pending_m3u8_data = None
                                    success = True
                                    break 
                            else:
                                print(f"Impossible de sélectionner {ep_text}")
                        
                        except asyncio.TimeoutError:
                            print(f"Timeout M3U8 pour {ep_text}")
                            if attempt < MAX_RETRIES:
                                await asyncio.sleep(2)

                    if not success:
                        print(f"ÉCHEC après {MAX_RETRIES} tentatives pour {ep_text}")
                        Cardinal.log_error(anime_title, season_number, ep_num, f"Échec M3U8 après {MAX_RETRIES} tentatives")

            except asyncio.TimeoutError:
                print("Timeout général atteint.")
            finally:
                page.remove_listener("request", intercept_request)

            print(f"\nCollecte terminée : {len(m3u8_by_episode)} M3U8 trouvés.\n")
            
            if len(m3u8_by_episode) != len(episodes_to_download):
                print(f"ATTENTION : {len(episodes_to_download)} épisodes vs {len(m3u8_by_episode)} M3U8 !")
                missing = [ep['text'] for ep in episodes_to_download if ep['text'] not in m3u8_by_episode]
                print(f"Épisodes manquants : {missing}")
                if input("Continuer quand même ? (o/n) ").lower() != 'o':
                    return

            # --- TÉLÉCHARGEMENT ---
            print(f"\nPhase 2 : Téléchargement des épisodes...\n")
            for episode in episodes_to_download:
                ep_num, ep_text = episode["number"], episode["text"]
                if ep_text not in m3u8_by_episode:
                    print(f"Pas de M3U8 pour {ep_text}, ignoré.")
                    Cardinal.log_error(anime_title, season_number, ep_num, "Aucune donnée M3U8")
                    continue
                
                print(f"\n--- Téléchargement : {ep_text} ---")
                try:
                    m3u8_info = m3u8_by_episode[ep_text]
                    await Cardinal.download_and_compile_episode(
                        m3u8_info["url"], m3u8_info["headers"], anime_title, season_number, ep_num
                    )
                    Cardinal.cleanscreen()
                except Exception as e:
                    print(f"ERREUR : {e}")
                    Cardinal.log_error(anime_title, season_number, ep_num, str(e))
                    Cardinal.cleanscreen()

        except Exception as e:
            print(f"Erreur critique : {e}")
        
        finally:
            print("\nTravail terminé. Fermeture du navigateur.\n")
            if context:
                await context.close()

if __name__ == "__main__":
    asyncio.run(main())