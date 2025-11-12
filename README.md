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
> [!NOTE]
> - If you want to launch in debug mode simply do ``python main.py --debug``
> - To launch the API with a specific IP and port, use : ``python main --api-option -ip 127.0.0.1 -port 5001`` or, with shorthand options : ``python main --api-option -i 127.0.0.1 -p 5001`` You can choose any IP or port you want.
> - If you don’t specify an IP or port, the API will use the default configuration some other exemple : ``python main --api-option -port 5001`` or ``python main --api-option -ip 127.0.0.1``
> If you want to run normaly simply do the command below
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