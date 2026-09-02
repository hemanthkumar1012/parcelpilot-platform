import re

app_js_path = 'frontend/app.js'
with open(app_js_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace the shipment processing block
old_block = """          let inTransit = 0, delivered = 0, alerts = 0;
          shipments.forEach(s => {
            const li = document.createElement('li');
            li.className = 'panel-recent'; // Real class used in HTML
            li.innerHTML = `
              <div style="display:flex; justify-content:space-between">
                <div>
                  <strong>${s.tracking_id}</strong>
                  <div class="user-meta">${s.origin} &rarr; ${s.destination}</div>
                </div>
                <span class="status-dot status-dot-${s.current_status === 'DELIVERED' ? 'ok' : 'pending'}">${s.current_status}</span>
              </div>
            `;
            shipmentsList.appendChild(li);
            if (s.current_status === 'IN_TRANSIT') inTransit++;
            if (s.current_status === 'DELIVERED') delivered++;
            if (s.current_status === 'EXCEPTION' || s.current_status === 'PENDING') alerts++;
          });"""

new_block = """          let inTransit = 0, delivered = 0, alerts = 0;
          shipments.forEach(s => {
            const li = document.createElement('li');
            li.className = 'panel-recent'; // Real class used in HTML
            
            // Map the backend status to frontend display styles
            let dotClass = 'pending';
            if (s.current_status === 'DELIVERED') dotClass = 'ok';
            if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) dotClass = 'error';

            li.innerHTML = `
              <div style="display:flex; justify-content:space-between">
                <div>
                  <strong>${s.tracking_id}</strong>
                  <div class="user-meta">${s.origin} &rarr; ${s.destination}</div>
                </div>
                <span class="status-dot status-dot-${dotClass}">${s.current_status}</span>
              </div>
            `;
            shipmentsList.appendChild(li);
            
            // Fix status counting to explicitly map all enum values
            if (['CREATED', 'ASSIGNED', 'PICKED_UP', 'IN_TRANSIT', 'OUT_FOR_DELIVERY'].includes(s.current_status)) {
                inTransit++;
            } else if (s.current_status === 'DELIVERED') {
                delivered++;
            } else if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) {
                alerts++;
            }
          });"""

content = content.replace(old_block, new_block)

# Add login form logic if it's missing
login_block = """
// --- LOGIN & AUTH LOGIC ---
(function() {
  const loginForm = document.getElementById('login-form');
  const guestBtn = document.getElementById('guest-demo-btn'); // from index.html (actually class guest-mode-btn but let's select it by class)
  const guestBtnClass = document.querySelector('.guest-mode-btn');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      try {
        const res = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData
        });
        if (!res.ok) throw new Error('Login failed');
        const data = await res.json();
        localStorage.setItem('parcelpilot_token', data.access_token);
        window.location.reload();
      } catch (err) {
        alert('Login failed: Check credentials');
      }
    });
  }

  if (guestBtnClass) {
    guestBtnClass.addEventListener('click', async () => {
      try {
        const res = await fetch('/api/v1/auth/guest', { method: 'POST' });
        if (!res.ok) throw new Error('Guest login failed');
        const data = await res.json();
        localStorage.setItem('parcelpilot_token', data.access_token);
        window.location.reload();
      } catch (err) {
        alert('Guest login failed');
      }
    });
  }
})();
"""

if "LOGIN & AUTH LOGIC" not in content:
    content += login_block

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(content)
