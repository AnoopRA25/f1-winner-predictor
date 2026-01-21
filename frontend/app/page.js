"use client";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import PredictionCard from "../components/PredictionCard";
import TyreChart from "../components/TyreChart";
import StandingsTable from "../components/StandingsTable";

export default function Home() {
  const API = "http://127.0.0.1:8000";

  const [pred, setPred] = useState([]);
  const [topDrivers, setTopDrivers] = useState([]);
  const [calendar, setCalendar] = useState([]);
  const [selectedRound, setSelectedRound] = useState(1);

  // load calendar
  useEffect(() => {
    fetch(`${API}/calendar`)
      .then((res) => res.json())
      .then((data) => {
        setCalendar(data.races || []);
        if ((data.races || []).length > 0) setSelectedRound(data.races[0].round);
      })
      .catch((err) => console.log("Calendar fetch error:", err));
  }, []);

  // fetch predictions when round changes
  useEffect(() => {
    fetch(`${API}/predict/2026/${selectedRound}`)
      .then((res) => res.json())
      .then((data) => setPred(data.top_predictions || []))
      .catch((err) => console.log("Prediction fetch error:", err));

    fetch(`${API}/top-drivers`)
      .then((res) => res.json())
      .then((data) => setTopDrivers(data.top_drivers || []))
      .catch((err) => console.log("Top drivers fetch error:", err));
  }, [selectedRound]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-black text-white">
      <Navbar />

      {/* ROUND SELECTOR */}
      <div className="px-8 pt-6">
        <div className="bg-gray-900/70 border border-gray-800 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
          <div>
            <h2 className="text-xl font-bold text-red-400">🏁 Race Round Selector</h2>
            <p className="text-gray-300 text-sm">
              Choose a round to predict winner probabilities.
            </p>
          </div>

          <select
            value={selectedRound}
            onChange={(e) => setSelectedRound(Number(e.target.value))}
            className="bg-black border border-gray-700 rounded-xl px-4 py-3 text-white outline-none"
          >
            {calendar.map((r) => (
              <option key={r.round} value={r.round}>
                Round {r.round} — {r.race_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* MAIN GRID */}
      <div className="p-8 grid gap-8 md:grid-cols-2">
        <PredictionCard data={pred} round={selectedRound} calendar={calendar} />
        <TyreChart />
      </div>

      <div className="px-8 pb-10">
        <StandingsTable data={topDrivers.slice(0, 10)} />
      </div>
    </div>
  );
}
