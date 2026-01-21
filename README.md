# 🏎️ F1 Winner Predictor — Full Stack + ML Dashboard (2026 Tracker)

A complete end-to-end project that predicts the **top F1 race winner probabilities** using historical race performance + tyre usage data, and displays results in a **modern colourful web dashboard**.

This project includes:
- ✅ Dataset generation using **FastF1**
- ✅ Model training using **scikit-learn (RandomForestClassifier)**
- ✅ Backend API using **FastAPI**
- ✅ Frontend dashboard using **Next.js + Tailwind CSS**
- ✅ Round selector + race calendar + live predictions

---

## 🌟 Features

### ✅ ML + Backend
- Builds dataset from historical races (2018–2023)
- Trains ML model to predict **Winner (1 / 0)**
- Saves trained model + encoders as `.pkl`
- API endpoints for predictions, standings, and calendar

### ✅ Frontend Dashboard
- Colourful F1-style UI
- Select any round (calendar dropdown)
- View top 10 predictions with win probabilities
- Tyre strategy UI section
- Driver points standings table

---

## 🧠 Model Summary

- **Type**: Supervised Machine Learning (Classification)
- **Model**: RandomForestClassifier
- **Target**: Winner (1 = race winner, 0 = not winner)
- **Output**: Win probability for each driver

### Features Used
| Feature | Description |
|--------|-------------|
| grid | starting position |
| avg_lap_time | average lap time in race |
| soft_laps | laps driven on Soft tyres |
| medium_laps | laps driven on Medium tyres |
| hard_laps | laps driven on Hard tyres |
| driver_enc | encoded driver ID |
| team_enc | encoded team ID |

---

## 🏗️ Project Structure

```text
f1-winner-predictor/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── ml/
│       ├── build_dataset.py
│       ├── train_model.py
│       ├── data.csv
│       ├── model.pkl
│       ├── le_driver.pkl
│       └── le_team.pkl
│
└── frontend/
    ├── app/
    │   ├── layout.js
    │   ├── page.js
    │   ├── globals.css
    │   └── race/
    │       └── [round]/
    │           └── page.js
    └── components/
        ├── Navbar.js
        ├── PredictionCard.js
        ├── TyreChart.js
        └── StandingsTable.js
⚙️ Installation & Setup
✅ 1) Clone Repository
git clone https://github.com/AnoopRA25/f1-winner-predictor.git
cd f1-winner-predictor
🧪 Backend Setup (FastAPI + ML)
✅ 2) Create Virtual Environment
cd backend
python -m venv venv

✅ 3) Activate Virtual Environment

Windows PowerShell

.\venv\Scripts\Activate.ps1


CMD

venv\Scripts\activate

✅ 4) Install Requirements
pip install -r requirements.txt

📊 Build Dataset + Train Model
✅ 5) Build dataset (FastF1)
cd ml
python build_dataset.py


This generates:
✅ data.csv

✅ 6) Train ML model
python train_model.py


This generates:
✅ model.pkl
✅ le_driver.pkl
✅ le_team.pkl

🚀 Run Backend

Go back to backend folder:

cd ..
uvicorn app:app --reload


Backend will run on:
👉 http://127.0.0.1:8000

🌐 Frontend Setup (Next.js)
✅ 7) Install frontend dependencies
cd ../frontend
npm install

✅ 8) Run frontend dev server
npm run dev


Frontend will run on:
👉 http://localhost:3000

🔌 API Endpoints
✅ Health check

GET /

✅ Round predictions

GET /predict/{season}/{round}
Example:

http://127.0.0.1:8000/predict/2026/5

✅ Race calendar

GET /calendar

✅ Top drivers standings

GET /top-drivers

📌 Note

Predictions are trained on historical seasons (2018–2023).

The model produces probabilities using past performance + tyre usage.

This project can be upgraded to include circuit history and real-time 2026 schedule.

✨ Future Enhancements

✅ Track-wise (circuit history) features

✅ Real tyre stint charts per driver

✅ Pit stop predictions

✅ Deploy online (Render + Vercel)

👨‍💻 Author

Anoop R A
GitHub: https://github.com/AnoopRA25


---

# ✅ Push README to GitHub
Run these:

```bat
git add README.md
git commit -m "Add detailed README"
git push
