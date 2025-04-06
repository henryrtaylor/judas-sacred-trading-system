
export function renderSignalCard(signal) {
  return `
    <div class="card">
      <h3>${signal.symbol}</h3>
      <p>Signal: ${signal.signal}</p>
      <p>Confidence: ${(signal.confidence * 100).toFixed(1)}%</p>
      <p class="updated">Updated: ${new Date(signal.updated).toLocaleTimeString()}</p>
    </div>
  `;
}
