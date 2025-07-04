import { useState } from 'react'
import './index.css'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch('/analyse', { method: 'POST', body: formData })
    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">KonpliAI</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} className="block" />
        <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">
          Analyse
        </button>
      </form>
      {result && (
        <div className="mt-6 bg-gray-100 p-4 rounded">
          <p><strong>SHA256:</strong> {result.sha256}</p>
          <p className="mt-2 whitespace-pre-wrap">{result.summary}</p>
          <a href={result.ledger_url} className="text-blue-600 underline" target="_blank" rel="noopener noreferrer">
            Ledger proof
          </a>
        </div>
      )}
    </div>
  )
}

export default App
