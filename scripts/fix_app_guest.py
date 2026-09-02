import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# We update renderAuthState to also fetch user profile and hide mutation buttons
new_auth_script = """
async function renderAuthState() {
  const token = localStorage.getItem('parcelpilot_token');
  const isLoggedIn = !!token;
  const loginView = document.getElementById('login-view');
  const dashboardView = document.getElementById('dashboard-view');
  
  if (loginView) loginView.hidden = isLoggedIn;
  if (dashboardView) dashboardView.hidden = !isLoggedIn;
  
  if (isLoggedIn) {
    if (typeof fetchDashboardData === 'function') fetchDashboardData();
    
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
  }
}
"""

js = js.replace("""function renderAuthState() {
  const isLoggedIn = !!localStorage.getItem('parcelpilot_token');
  const loginView = document.getElementById('login-view');
  const dashboardView = document.getElementById('dashboard-view');
  if (loginView) loginView.hidden = isLoggedIn;
  if (dashboardView) dashboardView.hidden = !isLoggedIn;
  if (isLoggedIn && typeof fetchDashboardData === 'function') fetchDashboardData();
}""", new_auth_script.strip())

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js with guest check")
