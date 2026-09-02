import os
import re

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# We need to insert renderAuthState() and call it
auth_script = """
function renderAuthState() {
  const isLoggedIn = !!localStorage.getItem('parcelpilot_token');
  const loginView = document.getElementById('login-view');
  const dashboardView = document.getElementById('dashboard-view');
  if (loginView) loginView.hidden = isLoggedIn;
  if (dashboardView) dashboardView.hidden = !isLoggedIn;
  if (isLoggedIn && typeof fetchDashboardData === 'function') fetchDashboardData();
}
"""

if 'function renderAuthState' not in js:
    js = auth_script + js
    
    # We also need to change `window.location.reload()` to `renderAuthState()`
    js = js.replace('window.location.reload();', 'renderAuthState();')
    
    # And call it on DOMContentLoaded
    # There are multiple DOMContentLoaded listeners. We can just add one.
    js += "\ndocument.addEventListener('DOMContentLoaded', renderAuthState);\n"

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js with renderAuthState")
