import os
import time
import logging
import pandas as pd
import fastf1
from tqdm import tqdm

# ✅ reduce spam logs
logging.getLogger("fastf1").setLevel(logging.ERROR)

# ✅ cache folder
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

# ✅ rounds for each season (ONLY till 2023)
SEASON_ROUNDS = {
    2022: 22,
    2023: 22,
}

def safe_load_session(year, rnd, retries=8):
    """
    Loads FastF1 session with retries.
    """
    for attempt in range(retries):
        try:
            race = fastf1.get_session(year, rnd, "R")
            # ✅ lightweight load (faster + fewer endpoints)
            race.load(telemetry=False, weather=False, messages=False)
            return race
        except Exception as e:
            print(f"⚠️ {year} Round {rnd} attempt {attempt+1}/{retries} failed")
            time.sleep(2 + attempt)
    return None

def build_year(year):
    rows = []
    total_rounds = SEASON_ROUNDS[year]
    print(f"\n🏁 Building season {year} ({total_rounds} rounds)")

    for rnd in tqdm(range(1, total_rounds + 1), desc=f"{year}"):
        race = safe_load_session(year, rnd)
        if race is None:
            continue

        try:
            results = race.results
            if results is None or results.empty:
                continue

            winner_abbr = results.iloc[0]["Abbreviation"]

            # laps
            laps = race.laps.copy()
            laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

            avg_lap = laps.groupby("Driver")["LapTimeSeconds"].mean().to_dict()

            # tyre compound
            if "Compound" in laps.columns:
                compound_counts = laps.groupby(["Driver", "Compound"]).size().unstack(fill_value=0)
            else:
                compound_counts = pd.DataFrame()

            for i in range(len(results)):
                d = results.iloc[i]
                abbr = d["Abbreviation"]

                soft = int(compound_counts.loc[abbr].get("SOFT", 0)) if abbr in compound_counts.index else 0
                medium = int(compound_counts.loc[abbr].get("MEDIUM", 0)) if abbr in compound_counts.index else 0
                hard = int(compound_counts.loc[abbr].get("HARD", 0)) if abbr in compound_counts.index else 0

                rows.append({
                    "season": year,
                    "round": rnd,
                    "race_name": race.event["EventName"],

                    "driver": d["FullName"],
                    "abbr": abbr,
                    "team": d["TeamName"],

                    "grid": int(d["GridPosition"]),
                    "finish_pos": int(d["Position"]),
                    "points": float(d["Points"]),

                    "avg_lap_time": float(avg_lap.get(abbr, 999)),

                    "soft_laps": soft,
                    "medium_laps": medium,
                    "hard_laps": hard,

                    "winner": 1 if abbr == winner_abbr else 0
                })

        except Exception as e:
            print(f"⚠️ Parse error {year} Round {rnd}: {e}")
            continue

    return pd.DataFrame(rows)

def append_years(existing_csv="data.csv", years=[2022, 2023]):
    old_df = pd.read_csv(existing_csv)
    existing_years = set(old_df["season"].unique())

    print("✅ Current dataset years:", sorted(existing_years))

    new_list = []
    for y in years:
        if y in existing_years:
            print(f"✅ {y} already exists — skipping")
            continue

        df_new = build_year(y)
        print(f"✅ {y} fetched rows:", len(df_new))
        new_list.append(df_new)

    if not new_list:
        print("✅ Nothing to append. Exiting.")
        return

    new_df = pd.concat(new_list, ignore_index=True)
    merged = pd.concat([old_df, new_df], ignore_index=True)

    # remove duplicates
    merged = merged.drop_duplicates(subset=["season", "round", "abbr"])
    merged.to_csv(existing_csv, index=False)

    print("\n✅ SUCCESS: Dataset updated!")
    print("✅ Total rows:", len(merged))
    print("✅ Seasons:", sorted(merged["season"].unique()))

if __name__ == "__main__":
    append_years("data.csv", [2022, 2023])
