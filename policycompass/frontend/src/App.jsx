import { useState } from 'react'
import CompareForm from './components/CompareForm'
import ResultDisplay from './components/ResultDisplay'
import axios from 'axios'

function App() {
  const [comparisonId, setComparisonId] = useState(null)
  const [status, setStatus] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCompare = async (policyA, policyB) => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await axios.post('/api/compare', { policy_a: policyA, policy_b: policyB })
      setComparisonId(data.id)
      setStatus('queued')
      pollResult(data.id)
    } catch (err) {
      setError('Failed to submit comparison')
      setLoading(false)
    }
  }

  const pollResult = async (id) => {
    const interval = setInterval(async () => {
      try {
        const { data } = await axios.get(`/api/comparison/${id}`)
        setStatus(data.status)
        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(interval)
          setLoading(false)
          setResult(data.result)
          if (data.status === 'failed') setError(data.result?.error || 'Comparison failed')
        }
      } catch (e) {
        clearInterval(interval)
        setError('Polling error')
        setLoading(false)
      }
    }, 2000)
  }

  return (
    <div className="container">
      <h1>PolicyCompass</h1>
      <CompareForm onSubmit={handleCompare} loading={loading} />
      {error && <p className="error">{error}</p>}
      {loading && <p className="loading">Processing... (status: {status})</p>}
      {result && <ResultDisplay result={result} />}
    </div>
  )
}

export default App
