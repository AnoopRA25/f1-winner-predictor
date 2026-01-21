"use client";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import PredictionCard from "../components/PredictionCard";
import TyreChart from "../components/TyreChart";
import StandingsTable from "../components/StandingsTable";

export default function Home() {
  const [pred, setPred] = useState([]);
  const [topDrivers, setTopDrivers] = useState([]);

  const API = "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API}/predict/2026/1`)
      .then((res) => res.json())
      .then((data) => setPred(data.top_predictions || []))
      .catch((err) => console.log("Prediction fetch error:", err));

    fetch(`${API}/top-drivers`)
      .then((res) => res.json())
      .then((data) => setTopDrivers(data.top_drivers || []))
      .catch((err) => console.log("Top drivers fetch error:", err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Navbar />

      <div className="p-8 grid gap-8 md:grid-cols-2">
        <PredictionCard data={pred} />
        <TyreChart />
      </div>

      <div className="px-8 pb-10">
        <StandingsTable data={topDrivers.slice(0, 10)} />
      </div>
    </div>
  );
}
