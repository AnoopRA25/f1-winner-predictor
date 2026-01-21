export default function Navbar() {
  return (
    <nav className="w-full px-8 py-5 flex justify-between items-center bg-black/60 backdrop-blur-md border-b border-gray-800 sticky top-0 z-50">
      <h1 className="text-2xl font-extrabold tracking-tight">
        <span className="text-red-500">🏎️ F1</span>{" "}
        <span className="text-white">Winner Predictor</span>
      </h1>

      <div className="hidden md:flex gap-6 text-gray-300 text-sm font-medium">
        <span className="hover:text-white transition">2026 Live</span>
        <span className="hover:text-white transition">Tyres</span>
        <span className="hover:text-white transition">Predictions</span>
      </div>
    </nav>
  );
}
