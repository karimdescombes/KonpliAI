import React, { useState } from 'react'

export default function UploadForm() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch('/analyse', { method: 'POST', body: formData })
    const data = await res.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded" disabled={loading}>
          {loading ? 'Analyzing...' : 'Upload'}
        </button>
      </form>
      {result && (
        <div className="mt-4 p-4 border rounded">
          <h2 className="font-semibold">Summary</h2>
          <p className="mb-2 whitespace-pre-wrap">{result.summary}</p>
          <p>Hash: {result.hash}</p>
          {result.proof_link && (
            <p>
              Proof: <a className="text-blue-600" href={result.proof_link}>{result.proof_link}</a>
            </p>
          )}
        </div>
      )}
    </div>
  )
}
