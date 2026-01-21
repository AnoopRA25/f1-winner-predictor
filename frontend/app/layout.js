import "./globals.css";

export const metadata = {
  title: "F1 Winner Predictor",
  description: "Predict F1 winners with ML + live dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-white">{children}</body>
    </html>
  );
}
