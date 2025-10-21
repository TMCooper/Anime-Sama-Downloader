import asyncio, os, subprocess
from playwright.async_api import async_playwright
from function.Yui import Yui
from function.Cardinal import Cardinal

async def main():

    # Vérifie si le navigateur est installé, sinon l'installe
    playwright_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "ms-playwright")
    if not os.path.exists(os.path.join(playwright_dir, "chromium-")):
        # print("Téléchargement de Chromium pour Playwright...")
        subprocess.run(["playwright", "install", "chromium"], check=True)

    """Point d'entrée principal du programme de téléchargement"""
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
                # Identifier l'épisode déjà sélectionné sur la page
                initial_episode_text = await page.evaluate("document.querySelector('#selectEpisodes').value")
                print(f"  → Page chargée sur : '{initial_episode_text}'. Attente de son M3U8...")
                
                new_m3u8_event.clear()
                await asyncio.wait_for(new_m3u8_event.wait(), timeout=30)
                
                if pending_m3u8_data:
                    m3u8_by_episode[initial_episode_text] = pending_m3u8_data
                    print(f"M3U8 de '{initial_episode_text}' stocké (total: 1)")
                    pending_m3u8_data = None
                else:
                    print(f"M3U8 pour l'épisode initial non détecté à temps.")

            except asyncio.TimeoutError:
                print(f"Timeout : Le M3U8 de l'épisode initial n'a pas été capturé. La boucle principale tentera de le récupérer.")
            except Exception as e:
                print(f"Erreur lors de la capture initiale : {e}")


            print(f"\nPhase 1 : Collecte des données M3U8 pour les autres épisodes...")
            
            try:
                for episode in episodes_to_download:
                    ep_num, ep_text = episode["number"], episode["text"]
                    
                    # Si on l'a déjà capturé (en phase 0 ou dans une exécution précédente de la boucle), on passe.
                    if ep_text in m3u8_by_episode:
                        print(f" {ep_text} déjà capturé, passage au suivant")
                        continue
                    
                    print(f"\n--- Traitement de la collecte pour : {ep_text} ---")
                    
                    success = False
                    MAX_RETRIES = 3
                    for attempt in range(1, MAX_RETRIES + 1):
                        if attempt > 1:
                            print(f"Tentative {attempt}/{MAX_RETRIES} pour {ep_text}...")
                        
                        new_m3u8_event.clear()
                        
                        try:
                            # === NAVIGATION PAR CLAVIER ===
                            await page.bring_to_front()
                            await page.click("#selectEpisodes")
                            await asyncio.sleep(0.4)

                            current_text = await page.evaluate("document.querySelector('#selectEpisodes').value")
                            all_texts = [ep["text"] for ep in episodes_to_download]
                            current_index = all_texts.index(current_text) if current_text in all_texts else 0
                            target_index = all_texts.index(ep_text)
                            steps = target_index - current_index

                            if steps > 0:
                                for _ in range(steps):
                                    await page.keyboard.press("ArrowDown")
                                    await asyncio.sleep(0.2)
                            elif steps < 0:
                                for _ in range(abs(steps)):
                                    await page.keyboard.press("ArrowUp")
                                    await asyncio.sleep(0.2)

                            await asyncio.sleep(2)

                            selected_episode = await page.evaluate("document.querySelector('#selectEpisodes').value")
                            if selected_episode != ep_text:
                                # print(f"Navigation clavier échouée : sur '{selected_episode}' au lieu de '{ep_text}'")
                                # print(f"Fallback JavaScript pour {ep_text}...")
                                await page.evaluate(f"""
                                    const select = document.querySelector('#selectEpisodes');
                                    select.value = '{ep_text}';
                                    select.dispatchEvent(new Event('change', {{bubbles: true}}));
                                    select.dispatchEvent(new Event('input', {{bubbles: true}}));
                                """)
                                await asyncio.sleep(2)
                                selected_episode = await page.evaluate("document.querySelector('#selectEpisodes').value")

                            if selected_episode == ep_text:
                                print(f"Attente du M3U8 pour {ep_text}...")
                                await asyncio.wait_for(new_m3u8_event.wait(), timeout=30)
                                if pending_m3u8_data:
                                    m3u8_by_episode[ep_text] = pending_m3u8_data
                                    print(f"M3U8 de '{ep_text}' stocké (total: {len(m3u8_by_episode)})")
                                    pending_m3u8_data = None
                                    success = True
                                    break 
                            else:
                                print(f"Impossible de sélectionner {ep_text} (toujours sur '{selected_episode}')")
                        except asyncio.TimeoutError:
                            print(f"Timeout lors de la capture M3U8 pour {ep_text}.")

                    if not success:
                        print(f"ERREUR CRITIQUE : Impossible de capturer {ep_text} après {MAX_RETRIES} tentatives")
                        Cardinal.log_error(anime_title, season_number, ep_num, f"Échec de la capture M3U8 après {MAX_RETRIES} tentatives")

            except asyncio.TimeoutError:
                print("Timeout général atteint.")
            finally:
                page.remove_listener("request", intercept_request)

            print(f"\nCollecte terminée. {len(m3u8_by_episode)} ensembles de données M3U8 uniques trouvés.\n")
            if len(m3u8_by_episode) != len(episodes_to_download):
                print(f"ATTENTION : {len(episodes_to_download)} épisodes détectés vs {len(m3u8_by_episode)} M3U8 collectés !")
                missing = [ep['text'] for ep in episodes_to_download if ep['text'] not in m3u8_by_episode]
                print(f"Épisodes manquants : {missing}")
                if input("Voulez-vous continuer quand même ? (o/n) ").lower() != 'o':
                    return

            # --- TÉLÉCHARGEMENT ---
            print(f"Phase 2 : Téléchargement des épisodes...\n")
            for episode in episodes_to_download:
                ep_num, ep_text = episode["number"], episode["text"]
                if ep_text not in m3u8_by_episode:
                    print(f"Pas de données M3U8 pour {ep_text}. Il est ignoré.")
                    Cardinal.log_error(anime_title, season_number, ep_num, "Aucune donnée M3U8 collectée")
                    continue
                print(f"\n--- Traitement de : {ep_text} ---")
                try:
                    m3u8_info = m3u8_by_episode[ep_text]
                    await Cardinal.download_and_compile_episode(
                        m3u8_info["url"], m3u8_info["headers"], anime_title, season_number, ep_num
                    )
                    Cardinal.cleanscreen()
                except Exception as e:
                    print(f"ERREUR pour l'épisode {ep_num}: {e}")
                    Cardinal.log_error(anime_title, season_number, ep_num, str(e))
                    Cardinal.cleanscreen()

        except Exception as e:
            print(f"Une erreur critique est survenue : {e}")
        
        finally:
            print("\nTravail terminé. Fermeture du navigateur.\n\n")
            if context:
                await context.close()

if __name__ == "__main__":
    asyncio.run(main())