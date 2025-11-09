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

3. Launch the application:
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
4. Enter the season number (leave empty for Season 1)
   - Note: Seasons can include films or OAVs (so for a films the syntax will be ``film`` and oavs it's ``oav`` but again verify if it's exists)
5. Choose the version: `vostfr` (subbed) or `vf` (dubbed)

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