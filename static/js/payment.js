const hints = {
  mtn: 'Enter your MTN number e.g. 77 123 4567 or 78 123 4567',
  airtel: 'Enter your Airtel number e.g. 70 123 4567 or 75 123 4567',
};

const labels = {
  mtn: (price) => `Pay UGX ${price.toLocaleString()} via MTN MoMo`,
  airtel: (price) => `Pay UGX ${price.toLocaleString()} via Airtel Money`,
};

function updateGateway(radio) {
  const gw = radio.value;
  document.getElementById('phone-hint').textContent = hints[gw];
  const btn = document.getElementById('payBtn');
  btn.dataset.gateway = gw;
  const numericPrice = Number(window.APP_DATA.price);
  btn.querySelector('.btn-text').textContent = labels[gw](numericPrice);
}

document.getElementById('payForm').addEventListener('submit', function (e) {
  const btn = document.getElementById('payBtn');
  const spinner = document.getElementById('btnSpinner');
  btn.disabled = true;
  spinner.style.display = 'block';
  btn.querySelector('.btn-text').textContent = 'Processing…';
});
