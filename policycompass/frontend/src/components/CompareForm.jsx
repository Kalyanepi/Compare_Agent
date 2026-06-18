import { useState } from 'react'

export default function CompareForm({ onSubmit, loading }) {
  const [policyA, setPolicyA] = useState('')
  const [policyB, setPolicyB] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (policyA.trim() && policyB.trim()) {
      onSubmit(policyA, policyB)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Policy A</label>
        <textarea value={policyA} onChange={e => setPolicyA(e.target.value)} placeholder="Paste policy text or upload content..." required />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <label>Policy B</label>
        <textarea value={policyB} onChange={e => setPolicyB(e.target.value)} placeholder="Paste second policy text..." required />
      </div>
      <button type="submit" disabled={loading} style={{ marginTop: '1rem' }}>Compare Policies</button>
    </form>
  )
}
