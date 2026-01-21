export default function PredictionCard({ data, round, calendar }) {
  const raceName =
    calendar?.find((x) => x.round === round)?.race_name || `Round ${round}`;

  return (
    <div className="rounded-3xl p-6 bg-gradient-to-br from-red-600/90 via-orange-500/70 to-yellow-300/30 shadow-[0_0_35px_rgba(255,60,60,0.25)] border border-white/10">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-2xl font-extrabold">🏁 Winner Predictions</h2>
          <p className="text-white/80 text-sm mt-1">{raceName}</p>
        </div>
        <span className="px-4 py-2 rounded-full bg-black/40 text-white text-sm border border-white/15">
          Round {round}
        </span>
      </div>

      {(!data || data.length === 0) && (
        <p className="text-white/80">Loading predictions...</p>
      )}

      <div className="space-y-3">
        {data?.slice(0, 8).map((d, i) => (
          <div
            key={i}
            className="flex items-center justify-between p-4 rounded-2xl bg-black/35 border border-white/10 hover:bg-black/45 transition"
          >
            <div>
              <p className="font-bold text-lg">
                {i + 1}. {d.driver} <span className="text-white/70">({d.abbr})</span>
              </p>
              <p className="text-sm text-white/70">{d.team}</p>
            </div>

            <div className="text-right">
              <p className="text-xl font-extrabold">
                {(d.win_probability * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-white/70">Win chance</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
