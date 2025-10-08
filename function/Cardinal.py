import os
import re
import requests
import subprocess
import tempfile
import platform
from tqdm import tqdm # type: ignore
from datetime import datetime


class Cardinal:
    """Classe pour le téléchargement et la compilation des épisodes"""
    
    OUTPUT_DIRECTORY = "dist"
    
    @staticmethod
    def log_error(anime_title, season_number, episode_number, error):
        """Enregistre les erreurs dans un fichier de log"""
        os.makedirs(Cardinal.OUTPUT_DIRECTORY, exist_ok=True)
        log_file = os.path.join(Cardinal.OUTPUT_DIRECTORY, "error_log.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Échec pour {anime_title} - S{season_number:02d}E{episode_number:02d}: {error}\n")
    
    @staticmethod
    def get_best_quality_url(master_url, headers):
        """Récupère l'URL de la meilleure qualité depuis le master.m3u8"""
        res_master = requests.get(master_url, headers=headers)
        res_master.raise_for_status()
        
        best_quality_url = ""
        max_resolution = 0
        lines = res_master.text.strip().split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith("#EXT-X-STREAM-INF"):
                resolution_match = re.search(r'RESOLUTION=(\d+)x(\d+)', line)
                if resolution_match:
                    width, height = map(int, resolution_match.groups())
                    if width * height > max_resolution:
                        max_resolution = width * height
                        best_quality_url = lines[i + 1]
        
        if not best_quality_url:
            raise ValueError("URL de qualité non trouvée.")
        
        # Construction de l'URL complète si nécessaire
        if not best_quality_url.startswith('http'):
            base_url = master_url.rsplit('/', 1)[0]
            best_quality_url = f"{base_url}/{best_quality_url}"
        
        return best_quality_url, max_resolution
    
    @staticmethod
    def get_segment_urls(quality_url, headers):
        """Récupère la liste des URLs des segments vidéo"""
        res_quality = requests.get(quality_url, headers=headers)
        res_quality.raise_for_status()
        
        segment_urls = [
            line for line in res_quality.text.strip().split('\n')
            if not line.startswith('#')
        ]
        
        if not segment_urls:
            raise ValueError("Playlist de qualité vide.")
        
        return segment_urls
    
    @staticmethod
    def download_segments(segment_urls, base_url, headers, temp_dir, season_number, episode_number):
        """Télécharge tous les segments vidéo dans un dossier temporaire"""
        segment_paths_file = os.path.join(temp_dir, "segments.txt")
        
        with open(segment_paths_file, 'w', encoding='utf-8') as f:
            desc = f"S{season_number:02d}E{episode_number:02d}"
            
            for i, segment_url in enumerate(tqdm(segment_urls, desc=desc)):
                segment_filename = f"seg_{i:05d}.ts"
                segment_path = os.path.join(temp_dir, segment_filename)
                
                # Construction de l'URL complète si nécessaire
                if not segment_url.startswith('http'):
                    segment_url = f"{base_url}/{segment_url}"
                
                # Téléchargement du segment
                segment_res = requests.get(segment_url, headers=headers, timeout=30)
                segment_res.raise_for_status()
                
                with open(segment_path, 'wb') as seg_file:
                    seg_file.write(segment_res.content)
                
                f.write(f"file '{segment_filename}'\n")
        
        return segment_paths_file
    
    @staticmethod
    def compile_episode(segment_paths_file, anime_title, season_number, episode_number):
        """Compile les segments en un fichier MP4 final avec FFmpeg"""
        print(f"Compilation de l'épisode {episode_number:02d}...")
        
        # Création du dossier de sortie
        season_folder_name = f"Saison {season_number:02d}"
        output_folder = os.path.join(Cardinal.OUTPUT_DIRECTORY, anime_title, season_folder_name)
        os.makedirs(output_folder, exist_ok=True)
        
        output_filename = os.path.join(output_folder, f"Episode {episode_number:02d}.mp4")
        
        # Commande FFmpeg
        command = [
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', segment_paths_file,
            '-c', 'copy', '-y', output_filename
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            raise RuntimeError(f"Erreur FFmpeg: {result.stderr}")
        
        print(f"Succès ! S{season_number:02d}E{episode_number:02d} sauvegardé.")
    
    @staticmethod
    async def download_and_compile_episode(master_url, headers, anime_title, season_number, episode_number):
        """Fonction principale pour télécharger et compiler un épisode complet"""
        print(f"\nTéléchargement pour S{season_number:02d}E{episode_number:02d}...")
        
        try:
            # Récupération de la meilleure qualité
            best_quality_url, max_resolution = Cardinal.get_best_quality_url(master_url, headers)
            
            # Récupération des segments
            segment_urls = Cardinal.get_segment_urls(best_quality_url, headers)
            base_url = best_quality_url.rsplit('/', 1)[0]
            
            # Téléchargement et compilation dans un dossier temporaire
            with tempfile.TemporaryDirectory() as temp_dir:
                segment_paths_file = Cardinal.download_segments(
                    segment_urls, base_url, headers, temp_dir,
                    season_number, episode_number
                )
                
                Cardinal.compile_episode(
                    segment_paths_file, anime_title,
                    season_number, episode_number
                )
        
        except Exception as e:
            Cardinal.log_error(anime_title, season_number, episode_number, str(e))
            raise

    @staticmethod  # <-- Ajouté ici
    def cleanscreen():
        if platform.system() == "Windows":
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)