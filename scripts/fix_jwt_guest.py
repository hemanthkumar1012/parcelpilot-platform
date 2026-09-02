import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the fetch('/api/v1/auth/me') block with simple JWT decode
old_auth_check = """
    // Check role and hide mutation buttons if guest
    try {
      const res = await fetch('/api/v1/auth/me', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (res.ok) {
        const user = await res.json();
        if (user.role === 'GUEST') {
          // Hide all buttons containing "New" or mutation actions
          document.querySelectorAll('button').forEach(btn => {
            const text = btn.innerText.toLowerCase();
            if (text.includes('new shipment') || text.includes('new driver')) {
              btn.style.display = 'none';
            }
          });
        }
      }
    } catch (e) {
      console.error('Failed to fetch user profile', e);
    }
"""

new_auth_check = """
    // Check role and hide mutation buttons if guest
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const isGuest = payload.sub && payload.sub.startsWith('guest_');
      if (isGuest) {
        document.querySelectorAll('button').forEach(btn => {
          const text = btn.innerText.toLowerCase();
          if (text.includes('new shipment') || text.includes('new driver')) {
            btn.style.display = 'none';
          }
        });
      }
    } catch (e) {
      console.error('Failed to parse token', e);
    }
"""

js = js.replace(old_auth_check.strip(), new_auth_check.strip())

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
