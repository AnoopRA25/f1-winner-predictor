export default function StandingsTable({ data }) {
  return (
    <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-lg overflow-x-auto">
      <h2 className="text-xl font-bold text-green-400 mb-4">
        📊 Top Drivers (Dataset Points)
      </h2>

      <table className="w-full text-left">
        <thead>
          <tr className="text-gray-400 border-b border-gray-700">
            <th className="py-2">Rank</th>
            <th className="py-2">Driver</th>
            <th className="py-2">Points</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((d, i) => (
            <tr key={i} className="border-b border-gray-800">
              <td className="py-2">{i + 1}</td>
              <td className="py-2">{d.driver} ({d.abbr})</td>
              <td className="py-2 font-semibold">{d.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
