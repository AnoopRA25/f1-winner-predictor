import fastf1
import pandas as pd
from tqdm import tqdm

fastf1.Cache.enable_cache("cache")   # ✅ creates cache folder automatically

def build_dataset(start=2018, end=2024):
    """
    Builds dataset driver-wise per race using FastF1
    Winner label = 1 if driver won else 0
    """

    rows = []

    for year in range(start, end + 1):
        try:
            schedule = fastf1.get_event_schedule(year)
        except Exception as e:
            print(f"❌ Schedule error for {year}: {e}")
            continue

        for _, event in tqdm(schedule.iterrows(), total=len(schedule), desc=f"Season {year}"):
            try:
                rnd = int(event["RoundNumber"])
                race = fastf1.get_session(year, rnd, "R")
                race.load()

                results = race.results
                if results is None or results.empty:
                    continue

                # winner
                winner_abbr = results.iloc[0]["Abbreviation"]

                # lap based features (avg lap time)
                laps = race.laps
                laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

                # compute avg lap time for each driver (ignoring NaNs)
                avg_lap = laps.groupby("Driver")["LapTimeSeconds"].mean().to_dict()

                # stint + tyre compound counts
                compound_counts = laps.groupby(["Driver", "Compound"]).size().unstack(fill_value=0)

                for i in range(len(results)):
                    d = results.iloc[i]
                    abbr = d["Abbreviation"]

                    soft = int(compound_counts.loc[abbr].get("SOFT", 0)) if abbr in compound_counts.index else 0
                    medium = int(compound_counts.loc[abbr].get("MEDIUM", 0)) if abbr in compound_counts.index else 0
                    hard = int(compound_counts.loc[abbr].get("HARD", 0)) if abbr in compound_counts.index else 0

                    rows.append({
                        "season": year,
                        "round": rnd,
                        "event": event["EventName"],

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
                print(f"⚠️ Skipping {year} round {event.get('RoundNumber','?')}: {e}")
                continue

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = build_dataset(2018, 2024)   # ✅ safest range
    df.to_csv("data.csv", index=False)
    print("✅ Saved FastF1 dataset as data.csv")
