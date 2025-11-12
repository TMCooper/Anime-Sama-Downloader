# Anime-Sama-Downloader

A fast and efficient downloader for anime from Anime-Sama.

## Installation

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
> [!NOTE]
> - If you want to launch in debug mode simply do ``python main.py --debug-mode`` and if you want to launch the api with spécial ip and port do ``python main --api-option -IP 127.0.0.1 -P 5001`` for exemple of course you can do what you want with the port or the ip and if you dont presice Port or IP by default it will be the default configuration like you simply do ``python main.py`` but with only the args you have complited 

1. Verify your anime exists on [Anime-Sama](https://anime-sama.org)
2. Launch `main.py`
3. Enter the anime name (e.g., "Frieren")
4. Choose beetween ``saison`` (season) ``film`` (movie) and ``oav``
   - Note: If you choose ``saison`` (season) keep in mind if the field is empty by default it's the fist season
5. Choose the version: `vostfr` or `vf`

The downloader will automatically process your request and stop when complete.

## Important Warning

**Rate Limiting**: Downloading too many anime in a short period may result in a temporary ban.

**Recommended**: Maximum of 2 anime downloads per hour.

## Recent Updates

- Complete project rework using a new API: [AnimeSamaApi](https://github.com/TMCooper/AnimeSamaApi/)
- Performance improvement: 2-3x faster than previous version
- Estimated download time: ~30 minutes for 12 episodes

## Contributing

Have an idea ? Share it in our [Ideas Discussion](https://github.com/TMCooper/Anime-Sama-Downloader/discussions/categories/ideas)!

## Demo (currently not same update soon)

<img src="./ressources/docs/demo.gif" width="100%" align="center" alt="Anime-Sama-Downloader Demo">