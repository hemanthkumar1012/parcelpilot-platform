import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Add logout logic and nav item active state logic inside DOMContentLoaded
logout_script = """
  // Logout Button
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('parcelpilot_token');
      renderAuthState();
    });
  }

  // Sidebar Nav Items (High-end button behavior)
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      // Remove active state from all
      navItems.forEach(nav => nav.removeAttribute('aria-current'));
      // Set active state on clicked
      item.setAttribute('aria-current', 'page');
    });
  });
"""

# Insert right after `renderAuthState();` inside `document.addEventListener('DOMContentLoaded', ...)`
js = js.replace('  renderAuthState();', '  renderAuthState();\n' + logout_script)

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js with logout and nav behavior")
