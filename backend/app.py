from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import os

# ✅ Create app FIRST
app = FastAPI()

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, "ml")

DATA_PATH = os.path.join(ML_DIR, "data.csv")
MODEL_PATH = os.path.join(ML_DIR, "model.pkl")
LE_DRIVER_PATH = os.path.join(ML_DIR, "le_driver.pkl")
LE_TEAM_PATH = os.path.join(ML_DIR, "le_team.pkl")

# ✅ Load files
df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else pd.DataFrame()
model = joblib.load(MODEL_PATH)
le_driver = joblib.load(LE_DRIVER_PATH)
le_team = joblib.load(LE_TEAM_PATH)


@app.get("/")
def home():
    return {"message": "F1 Winner Predictor Backend Running ✅"}


@app.get("/calendar")
def calendar():
    """
    Returns list of rounds and race names from latest season in dataset.
    """
    if df.empty:
        return {"error": "Dataset empty"}

    latest_season = int(df["season"].max())
    season_df = df[df["season"] == latest_season].copy()

    races = (
        season_df[["round", "race_name"]]
        .drop_duplicates()
        .sort_values("round")
        .to_dict(orient="records")
    )

    return {"season": latest_season, "races": races}


@app.get("/top-drivers")
def top_drivers():
    if df.empty:
        return {"top_drivers": []}

    top = (
        df.groupby(["abbr", "driver"], as_index=False)["points"]
        .sum()
        .sort_values("points", ascending=False)
        .head(20)
    )

    out = []
    for _, r in top.iterrows():
        out.append({
            "abbr": r["abbr"],
            "driver": r["driver"],
            "points": float(r["points"])
        })

    return {"top_drivers": out}


@app.get("/predict/{season}/{round_no}")
def predict(season: int, round_no: int):
    """
    ✅ Dynamic prediction that changes per round:
    Uses driver stats up to (round_no - 1) from latest dataset season.
    """

    if df.empty:
        return {"error": "Dataset is empty"}

    latest_season = int(df["season"].max())
    season_df = df[df["season"] == latest_season].copy()

    prev_round = max(1, round_no - 1)

    # ✅ use all races up to prev_round
    past_df = season_df[season_df["round"] <= prev_round].copy()

    # ✅ aggregate driver form
    driver_form = past_df.groupby("abbr").agg({
        "driver": "last",
        "team": "last",
        "grid": "mean",
        "avg_lap_time": "mean",
        "soft_laps": "mean",
        "medium_laps": "mean",
        "hard_laps": "mean",
        "winner": "sum"
    }).reset_index()

    driver_form.rename(columns={"winner": "wins_so_far"}, inplace=True)

    # ✅ safe encoder
    def safe_driver_enc(x):
        return le_driver.transform([x])[0] if x in le_driver.classes_ else 0

    def safe_team_enc(x):
        return le_team.transform([x])[0] if x in le_team.classes_ else 0

    driver_form["driver_enc"] = driver_form["abbr"].apply(safe_driver_enc)
    driver_form["team_enc"] = driver_form["team"].apply(safe_team_enc)

    features = [
        "grid",
        "avg_lap_time",
        "soft_laps",
        "medium_laps",
        "hard_laps",
        "driver_enc",
        "team_enc"
    ]

    X = driver_form[features].fillna(0)
    probs = model.predict_proba(X)[:, 1]
    driver_form["win_probability"] = probs

    top = driver_form.sort_values("win_probability", ascending=False).head(10)

    return {
        "season": season,
        "round": round_no,
        "using_active_season": latest_season,
        "using_data_up_to_round": prev_round,
        "top_predictions": top[["driver", "abbr", "team", "win_probability"]].to_dict(orient="records"),
    }
