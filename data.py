from pathlib import Path
import pandas as pd

def season_code(start_year):
    return f"{start_year % 100:02d}{(start_year + 1) % 100:02d}"  

def load_pl(first=2010, last=2024, cache="data/pl_matches.csv"):
    path = Path(cache)
    if path.exists():
        return pd.read_csv(path, parse_dates=["Date"], low_memory=False)
    frames = []
    for y in range(first, last + 1):
        url = f"https://www.football-data.co.uk/mmz4281/{season_code(y)}/E0.csv"
        s = pd.read_csv(url, encoding="latin-1")      # older files aren't always UTF-8
        s = s.dropna(subset=["HomeTeam"])             # some files have blank trailing rows
        s["Season"] = f"{y}-{str(y + 1)[-2:]}"         # "2023-24"
        frames.append(s)
    out = pd.concat(frames, ignore_index=True)
    out["Date"] = pd.to_datetime(out["Date"], dayfirst=True, format="mixed")   # old seasons use dd/mm/yy
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)
    return out

pl = load_pl()
pl.groupby("Season").size()   