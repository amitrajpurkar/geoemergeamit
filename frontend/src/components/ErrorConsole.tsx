interface ErrorConsoleProps {
  error: Error | string | null
}

export function ErrorConsole({ error }: ErrorConsoleProps) {
  if (!error) return null

  const errorMessage = error instanceof Error ? error.message : error
  const stackLines = error instanceof Error && error.stack 
    ? error.stack.split('\n').slice(0, 6)
    : []

  const interpretedMessage = errorMessage.includes('503')
    ? 'Earth Engine is not initialized. Authenticate locally (earthengine authenticate) and retry.'
    : errorMessage.includes('500')
    ? 'Internal server error. Check backend logs for details.'
    : errorMessage.includes('400')
    ? 'Bad request. Check your input parameters.'
    : errorMessage.includes('404')
    ? 'Resource not found. Check the API endpoint.'
    : errorMessage

  return (
    <div
      style={{
        backgroundColor: '#fee',
        border: '2px solid #c33',
        borderRadius: 8,
        padding: 16,
        marginBottom: 16,
        fontFamily: 'monospace',
        fontSize: 13
      }}
    >
      <div style={{ fontWeight: 'bold', color: '#c33', marginBottom: 8 }}>
        ERROR
      </div>
      <div style={{ marginBottom: 12, color: '#333' }}>
        <strong>Message:</strong> {interpretedMessage}
      </div>
      {stackLines.length > 0 && (
        <div>
          <div style={{ fontWeight: 'bold', color: '#666', marginBottom: 4 }}>
            Stack trace (last 5 lines):
          </div>
          <pre
            style={{
              backgroundColor: '#fff',
              border: '1px solid #ddd',
              borderRadius: 4,
              padding: 8,
              margin: 0,
              overflow: 'auto',
              fontSize: 11,
              lineHeight: 1.4
            }}
          >
            {stackLines.join('\n')}
          </pre>
        </div>
      )}
    </div>
  )
}
