import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train():
    df = pd.read_csv("data.csv")

    # ✅ encoders for driver and team (FastF1 columns)
    le_driver = LabelEncoder()
    le_team = LabelEncoder()

    # ✅ FastF1 uses "abbr" not "driverId"
    df["driver_enc"] = le_driver.fit_transform(df["abbr"])
    df["team_enc"] = le_team.fit_transform(df["team"])

    features = [
        "grid",
        "avg_lap_time",
        "soft_laps",
        "medium_laps",
        "hard_laps",
        "driver_enc",
        "team_enc"
    ]

    # Safety: ensure columns exist
    for col in features:
        if col not in df.columns:
            df[col] = 0

    X = df[features].fillna(0)
    y = df["winner"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=18,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("✅ Model training complete!")
    print(f"✅ Accuracy: {acc:.4f}")

    joblib.dump(model, "model.pkl")
    joblib.dump(le_driver, "le_driver.pkl")
    joblib.dump(le_team, "le_team.pkl")

    print("✅ Saved: model.pkl, le_driver.pkl, le_team.pkl")

if __name__ == "__main__":
    train()
