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

1. Verify your anime exists on [Anime-Sama](https://anime-sama.org)
2. Launch `main.py`
3. Enter the anime name (e.g., "Frieren")
4. choose between ``saison`` (season) ``film`` (movie) and ``oav``
   - Note: If you choose ``saison`` (season) keep in mind that if the field is empty, it will default to the first season
5. Choose the version: `vostfr` or `vf`

The downloader will automatically process your request and stop when it's complete.

## Important Warning

**Rate Limiting**: Downloading too many anime in a short period may result in a temporary ban.

**Recommended**: Maximum of 2 anime downloads per hour.

## Recent Updates

- Added argument system: debug (--debug), IP (-i), Port (-p)
- Complete project rework using a new API : [AnimeSamaApi](https://github.com/TMCooper/AnimeSamaApi/)
- Performance improvement: 2-3x faster than previous version

## Contributing

Have an idea ? Share it in our [Ideas Discussion](https://github.com/TMCooper/Anime-Sama-Downloader/discussions/categories/ideas)!

## Demo (currently not same update soon)

<img src="./ressources/docs/demo.gif" width="100%" align="center" alt="Anime-Sama-Downloader Demo">

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TMCooper/Anime-Sama-Downloader&type=date&legend=top-left)](https://www.star-history.com/#TMCooper/Anime-Sama-Downloader&type=date&legend=top-left)