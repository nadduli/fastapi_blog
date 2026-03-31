const expiresAt = new Date(window.APP_DATA.expiresAtIso);
const timerEl = document.getElementById('sessionTimer');

function updateTimer() {
  const now = new Date();
  const diff = Math.max(0, Math.floor((expiresAt - now) / 1000));

  if (diff === 0) {
    timerEl.textContent = 'Session expired';
    timerEl.style.color = 'var(--accent2)';
    return;
  }

  const h = String(Math.floor(diff / 3600)).padStart(2, '0');
  const m = String(Math.floor((diff % 3600) / 60)).padStart(2, '0');
  const s = String(diff % 60).padStart(2, '0');
  timerEl.textContent = `${h}:${m}:${s}`;
}

updateTimer();
setInterval(updateTimer, 1000);

const colors = ['#ffcc00', '#e8442a', '#38d9a9', '#ffffff', '#4dabf7'];
const container = document.getElementById('confetti');

for (let i = 0; i < 60; i++) {
  const piece = document.createElement('div');
  piece.className = 'confetti-piece';
  piece.style.cssText = `
    left: ${Math.random() * 100}%;
    background: ${colors[Math.floor(Math.random() * colors.length)]};
    animation-duration: ${1.5 + Math.random() * 2}s;
    animation-delay: ${Math.random() * 0.8}s;
    width: ${6 + Math.random() * 8}px;
    height: ${6 + Math.random() * 8}px;
    border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
  `;
  container.appendChild(piece);
}

setTimeout(() => container.remove(), 4000);
