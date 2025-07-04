import { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">KoNpLiAI</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-2"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Upload
        </button>
      </form>
      {result && (
        <div className="bg-gray-100 p-4 rounded">
          <p><strong>SHA256:</strong> {result.sha256}</p>
          <p><strong>Summary:</strong> {result.summary}</p>
          <p>
            <strong>Ledger:</strong> <a href={result.ledger_url} target="_blank" className="text-blue-600">View Proof</a>
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
