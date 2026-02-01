import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateImage = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setImageUrl(null);
    setError(null);

    try {
      const res = await fetch("https://image-create-backend.onrender.com/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: prompt }),
      });

      const data = await res.json();

      if (data.image) {
        setImageUrl(`data:image/png;base64,${data.image}`);
      } else if (data.detail) {
        setError(data.detail);
      }
    } catch (err) {
      console.error("Error generating image:", err);
      setError("Failed to generate image. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🎨 AI Image Generator</h1>
      <p className="subtitle">Powered by Freepik AI - Free!</p>

      <input
        type="text"
        placeholder="Describe the image you want to create..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && generateImage()}
      />

      <button onClick={generateImage} disabled={loading || !prompt.trim()}>
        {loading ? "✨ Generating..." : "🚀 Generate Image"}
      </button>

      {error && <div className="error">{error}</div>}

      {imageUrl && (
        <div className="image-container">
          <img src={imageUrl} alt="Generated" />
        </div>
      )}
    </div>
  );
}

export default App;
