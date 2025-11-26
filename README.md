<picture>
    <img align="right" src="https://wakatime.com/badge/github/TMCooper/Anime-Sama-Downloader.svg" alt="Typing SVG"/>
</picture>

# Anime-Sama-Downloader

A fast and efficient downloader for anime from Anime-Sama.

## Installation

> [!IMPORTANT]
> This project requires **Git** to be installed.  
> Download: [here](https://git-scm.com/downloads)

1. Clone the repository with submodules:
```bash
git clone https://github.com/TMCooper/Anime-Sama-Downloader.git --recurse-submodules
```

2. Run the setup:
```bash
python setup.py
```

3. Launch the application (after entering the environment):
```bash
python main.py
```

> [!NOTE]
> - To launch in debug mode, simply run:
>   ```bash
>   python main.py --debug
>   ```
> - To launch the API with a specific IP and port, run:
>   ```bash
>   python main.py --ip 127.0.0.1 --port 5001
>   ```
>   Or using shorthand options:
>   ```bash
>   python main.py -i 127.0.0.1 -p 5001
>   ```
> - You can also specify only the IP or only the port:
>   ```bash
>   python main.py --ip 127.0.0.1
>   python main.py --port 5001
>   ```

### Playwright Installation
If you see this message after installation:
```
Looks like Playwright was just installed or updated.
Please run the following command to download new browsers:
playwright install
```

Simply run (in your virtual environment):
```bash
playwright install
```

## Usage

>[!IMPORTANT]
>If your anime's name contains, for example, "season name," "remake 2024," or something similar, then copy and paste that same name. For example, if you want to play season 1 part 1 "Cinderella Gray" for anime, enter the same name but choose "other image," for example [here](/ressources/images/exempleNomAttypique.png).

1. Verify your anime exists on [Anime-Sama](https://anime-sama.org)
2. Launch `main.py`
3. Enter the anime name (e.g., "Frieren")
4. choose between ``saison`` (season) ``film`` (movie), ``oav`` and ``autre`` (other)
   - Note: If you choose ``saison`` (season) keep in mind that if the field is empty, it will default to the first season
5. Choose the version: `vostfr` or `vf`

The downloader will automatically process your request and stop when it's complete.

## Important Warning

**Rate Limiting**: Downloading too many anime in a short period may result in a temporary ban.

**Recommended**: Maximum of 2 anime downloads per hour.

## Recent Updates

- New system for update notifications and anonymous stats collection. 
  (The file `ressources/Utils/statsChoice.json` will be created at first run. 
  You can change your choice anytime by editing it: replace "yes"/"oui" with "no"/"non".)
- Added argument system: debug (--debug), IP (-i), Port (-p)
- Complete project rework using a new API : [AnimeSamaApi](https://github.com/TMCooper/AnimeSamaApi/)

## Contributing

Have an idea ? Share it in our [Ideas Discussion](https://github.com/TMCooper/Anime-Sama-Downloader/discussions/categories/ideas)!

## Demo

<img src="./ressources/docs/demo.gif" width="100%" align="center" alt="Anime-Sama-Downloader Demo">

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TMCooper/Anime-Sama-Downloader&type=date&legend=top-left)](https://www.star-history.com/#TMCooper/Anime-Sama-Downloader&type=date&legend=top-left)