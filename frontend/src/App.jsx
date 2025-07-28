import React, { useEffect, useState } from "react";

export default function App() {
  const [products, setProducts] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [semanticResults, setSemanticResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState([]);

  //Load product titles on mount
  useEffect(() => {
    fetch("http://localhost:8000/items")
      .then((res) => res.json())
      .then((data) => setProducts(data.items))
      .catch((err) => console.error("Failed to load items", err));
  }, []);

  const fetchRecommendations = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/recommend?item_id=${selectedId}`);
      const data = await res.json();
      setRecommendations(data.recommendations);
      setSemanticResults([]);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSemanticResults = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      setSemanticResults(data.results || []);
      setRecommendations([]);
    } catch (err) {
      console.error("Error with semantic search:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-indigo-700 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-xl p-8 max-w-3xl w-full space-y-6 animate-fade-in">
        <h1 className="text-3xl font-bold text-center text-indigo-800">Product Recommender</h1>

        <div className="space-y-4">
          <div>
            <label className="font-semibold text-gray-700">Select a product:</label>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="w-full mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            >
              <option value="">-- Choose an item --</option>
              {products.map((item) => (
                <option key={item.item_id} value={item.item_id}>
                  {item.title}
                </option>
              ))}
            </select>
            <button
              onClick={fetchRecommendations}
              className="mt-3 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded transition"
            >
              {loading ? "Loading..." : "Get Similar Products"}
            </button>
          </div>

          <div className="pt-4 border-t border-gray-300">
            <label className="font-semibold text-gray-700">Or enter a query:</label>
            <div className="flex gap-2 mt-1">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., waterproof trekking boots"
                className="flex-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
              <button
                onClick={fetchSemanticResults}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition"
              >
                Search
              </button>
            </div>
          </div>
        </div>

        {/* Results */}
        {(recommendations.length > 0 || semanticResults.length > 0) && (
          <div className="pt-6 border-t">
            <h2 className="text-xl font-bold text-gray-800 mb-2">🔎 Results:</h2>
            <ul className="space-y-2">
              {(recommendations.length > 0 ? recommendations : semanticResults).map((item, i) => (
                <li key={i} className="bg-gray-50 p-3 rounded shadow-sm border">
                  <p className="font-semibold">{item.title}</p>
                  <p className="text-gray-600 text-sm">{item.description}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
