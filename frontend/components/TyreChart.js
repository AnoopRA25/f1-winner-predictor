export default function TyreChart() {
  return (
    <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-lg">
      <h2 className="text-xl font-bold text-blue-400 mb-3">🛞 Tyre Strategy</h2>
      <p className="text-gray-300">
        (UI Preview) We will connect this to FastF1 tyre stint data later.
      </p>

      <div className="mt-4 flex gap-3 flex-wrap">
        <span className="px-4 py-2 rounded-full bg-red-500">Soft</span>
        <span className="px-4 py-2 rounded-full bg-yellow-400 text-black">Medium</span>
        <span className="px-4 py-2 rounded-full bg-white text-black">Hard</span>
      </div>

      <div className="mt-6 h-3 rounded-full bg-gradient-to-r from-red-500 via-yellow-400 to-white"></div>
    </div>
  );
}
