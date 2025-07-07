import { useState } from 'react'
import './index.css'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await fetch('/upload', {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      setResult(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow w-full max-w-md">
        <h1 className="text-2xl mb-4 font-bold text-center">KoNpLiAI Upload</h1>
        <input type="file" accept=".pdf,.docx" onChange={e => setFile(e.target.files[0])} className="mb-4" />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded" disabled={loading}>{loading ? 'Uploading...' : 'Upload'}</button>
        {result && (
          <div className="mt-4 text-sm">
            <p><strong>SHA256:</strong> {result.sha256}</p>
            <p className="mt-2"><strong>Summary:</strong></p>
            <p className="whitespace-pre-wrap">{result.summary}</p>
            <p className="mt-2"><a href={result.ledger_url} className="text-blue-600 underline" target="_blank" rel="noreferrer">View Ledger Proof</a></p>
          </div>
        )}
      </form>
    </div>
  )
}

export default App
