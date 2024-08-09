import React, { useState } from "react";
import './App.css';  // Import the CSS file

function App() {
  const [query, setQuery] = useState("");
  const [images, setImages] = useState([]);
  const [resultsCount, setResultsCount] = useState(10); // default to 10

  const handleSearch = async () => {
    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, top_n: resultsCount }), // include top_n
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setImages(data.results.slice(0, resultsCount));
    } catch (error) {
      console.error("Search error:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Meme Search</h1>
      </header>

      <div className="search-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for memes"
          className="search-input"
        />
        <select
          value={resultsCount}
          onChange={(e) => setResultsCount(Number(e.target.value))}
          className="select-topN"
        >
          <option value={10}>Top 10</option>
          <option value={25}>Top 25</option>
          <option value={50}>Top 50</option>
          <option value={100}>Top 100</option>
        </select>

        <button onClick={handleSearch} className="search-button">Search</button>
      </div>

      <div className="results-container">
        {images.map((img, index) => (
          <div key={index} className="result-item">
            <img
              src={`http://localhost:5000/image?filepath=${encodeURIComponent(
                img.filepath
              )}`}
              alt={`meme-${index}`}
              className="meme-image"
            />
            <p>Score: {(img.confidence).toFixed(2)}%</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;