let seconds = 3 * 60;
const timerEl = document.getElementById('countdown');

const tick = setInterval(() => {
  seconds--;
  if (seconds <= 0) {
    clearInterval(tick);
    timerEl.style.color = 'var(--accent2)';
    timerEl.textContent = 'Timed out';
    return;
  }
  const m = String(Math.floor(seconds / 60)).padStart(2, '0');
  const s = String(seconds % 60).padStart(2, '0');
  timerEl.textContent = `${m}:${s}`;
}, 1000);

const txRef = window.APP_DATA.txRef;

async function pollStatus() {
  try {
    const res = await fetch(`/api/payment/status/${txRef}`);
    const data = await res.json();

    if (data.status === 'success') {
      clearInterval(tick);
      clearInterval(poll);
      window.location.href = `/success?ref=${txRef}`;
    } else if (data.status === 'failed') {
      clearInterval(tick);
      clearInterval(poll);
      window.location.href = `/payment/failed?ref=${txRef}`;
    }
  } catch (e) {
    console.error('Poll error:', e);
  }
}

const poll = setInterval(pollStatus, 5000);
setTimeout(pollStatus, 8000);
