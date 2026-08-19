# Basketball Stats App

A desktop app for browsing NBA statistics, built with Python and PyQt6. Player
careers, team shooting splits, and league leaderboards — pulled live from the
NBA's public stats API.

## Features

- **Stats by Player** — browse the player list and open any player for
  season-by-season career stats (regular season and playoffs), last-game box
  scores, and shot charts. Toggle between Per Game, Totals, and Per 36 minutes.
- **Team Stats** — team shooting splits rendered on a drawn basketball court.
- **League Leaders** — leaderboards across 14 stat categories including points,
  rebounds, assists, steals, blocks, and shooting percentages.

Network calls run on background threads, so the UI stays responsive while data
loads.

## Requirements

- Python 3.9 or newer
- An internet connection (all stats are fetched live)

## Installation

```bash
git clone https://github.com/<your-username>/basketballApp.git
cd basketballApp

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Running

```bash
python src/main.py
```

## Building a standalone executable

The app bundles with [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller

# macOS
pyinstaller src/main.py --onefile --name basketballApp-mac \
  --hidden-import PyQt6 --icon assets/bball_new.ico \
  --add-data "assets/bball_new.ico:assets"

# Windows
pyinstaller src/main.py --onefile --name basketballApp-win.exe ^
  --hidden-import PyQt6 --icon assets/bball_new.ico ^
  --add-data "assets/bball_new.ico;assets" --noconsole
```

GitHub Actions builds both targets automatically on every push to `main` — see
[.github/workflows/build.yml](.github/workflows/build.yml). Binaries are
published as workflow artifacts.

## Project structure

```
src/
  main.py             Entry point; sets up the QStackedWidget page stack
  main_menu.py        Landing page
  player_list.py      Player browser
  player_dialogs.py   Career stats, box scores, shot charts
  team_list.py        Team browser
  team_dialogs.py     Team shooting splits and court rendering
  league_leaders.py   Leaderboards by stat category
  nbaData.py          All nba_api calls live here
  styles.py           Application-wide Qt stylesheet
assets/               Application icons
docs/                 Project documentation
```

## Data source

Stats come from the NBA's public stats endpoints via the
[`nba_api`](https://github.com/swar/nba_api) package. This project is not
affiliated with, endorsed by, or sponsored by the NBA. Team names, logos, and
statistics are the property of their respective owners.

## License

Released under the [MIT License](LICENSE).
