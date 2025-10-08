import asyncio
from function.Yui import Yui
from function.Cardinal import Cardinal


async def main():
    """Point d'entrée principal du programme de téléchargement"""
    print("Démarrage du script de téléchargement de saison...\n")
    
    # Détection du profil navigateur
    browser_user_data_path, browser_channel = Yui.find_browser_profile()
    if not browser_user_data_path:
        print("Aucun profil navigateur détecté (Edge ou Chrome requis).")
        return
    
    # Demande de l'URL
    url = input("Veuillez coller l'URL de la page (n'importe quel épisode de la saison) : ")
    if not url.startswith('http'):
        print("URL invalide. Elle doit commencer par http:// ou https://")
        return
    
    # Avertissement utilisateur
    print("\n--- IMPORTANT ---")
    print(f"Le script va utiliser votre profil {browser_channel.title()}. Fermez toutes ses fenêtres.")
    input("Appuyez sur Entrée lorsque c'est fait...")

    Cardinal.cleanscreen()
    
    playwright_instance = None
    context = None
    
    try:
        # Création du contexte navigateur
        playwright_instance, context = await Yui.create_browser_context(
            browser_user_data_path, browser_channel
        )
        page = await context.new_page()
        
        # Récupération des informations (charge aussi la page pour le 1er épisode)
        anime_title, season_number, episodes_to_download = await Yui.get_anime_info(page, url)
        
        # --- LOGIQUE D'INTERCEPTION RECONSTRUITE ICI ---
        for i, episode in enumerate(episodes_to_download):
            ep_num, ep_text, ep_value = episode["number"], episode["text"], episode["value"]
            print(f"\n--- Traitement de : {ep_text} ---")
            
            try:
                # 1. Recharger la page pour les épisodes suivants (sauf le premier)
                if i > 0:
                    await page.select_option("#selectEpisodes", value=ep_value)
                    await page.reload(wait_until="domcontentloaded")

                # 2. Mettre en place l'intercepteur réseau
                url_found = asyncio.Future()
                
                async def intercept_request(request):
                    if "master.m3u8" in request.url and not url_found.done():
                        url_found.set_result((request.url, await request.all_headers()))
                
                page.on("request", intercept_request)
                
                # 3. Attendre que l'URL soit trouvée
                try:
                    master_url, req_headers = await asyncio.wait_for(url_found, timeout=30)
                finally:
                    # On retire le listener quoi qu'il arrive (succès ou timeout)
                    page.remove_listener("request", intercept_request)
                
                # 4. Lancer le téléchargement avec Cardinal
                await Cardinal.download_and_compile_episode(
                    master_url, req_headers, anime_title, season_number, ep_num
                )
                
                Cardinal.cleanscreen()
            
            except asyncio.TimeoutError:
                error_message = "Timeout de 30s atteint. Le M3U8 n'a pas été trouvé."
                print(f"ERREUR pour l'épisode {ep_num}: {error_message}")
                Cardinal.log_error(anime_title, season_number, ep_num, error_message)
                print("Passage à l'épisode suivant.")
                Cardinal.cleanscreen()
            
            except Exception as e:
                print(f"ERREUR pour l'épisode {ep_num}: {e}")
                Cardinal.log_error(anime_title, season_number, ep_num, str(e))
                print("Passage à l'épisode suivant.")
                Cardinal.cleanscreen()
    
    except Exception as e:
        print(f"Une erreur critique est survenue : {e}")
    
    finally:
        print("\nTravail terminé. Fermeture du navigateur.\n\n")
        if context:
            await context.close()
        if playwright_instance:
            await playwright_instance.stop()


if __name__ == "__main__":
    asyncio.run(main())