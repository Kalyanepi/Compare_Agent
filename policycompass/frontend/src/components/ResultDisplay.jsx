export default function ResultDisplay({ result }) {
  if (!result) return null
  const { summary, clauses } = result

  return (
    <div style={{ marginTop: '2rem' }}>
      <h2>Comparison Result</h2>
      <p><strong>Summary:</strong> {summary || 'No summary'}</p>
      {clauses && clauses.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Clause</th>
              <th>Policy A</th>
              <th>Policy B</th>
              <th>Difference</th>
            </tr>
          </thead>
          <tbody>
            {clauses.map((c, idx) => (
              <tr key={idx}>
                <td>{c.clause}</td>
                <td>{c.policy_a_value}</td>
                <td>{c.policy_b_value}</td>
                <td>{c.difference}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
