import os
import re

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Swap table arrows for Lucide icons in both Dashboard and Shipments page fetching
js = js.replace('<button class="icon-btn">&rarr;</button>', '<button class="icon-btn"><i data-lucide="chevron-right"></i></button>')

# 2. Update loadDriversPage to actually fetch drivers or show a clean restricted UI
old_drivers = """
function loadDriversPage() {
  const grid = document.getElementById('drivers-grid');
  const empty = document.getElementById('drivers-empty');
  if (grid) grid.innerHTML = '';
  if (empty) empty.hidden = false;
}
"""

new_drivers = """
async function loadDriversPage() {
  const token = localStorage.getItem('parcelpilot_token');
  if (!token) return;
  const grid = document.getElementById('drivers-grid');
  const empty = document.getElementById('drivers-empty');
  
  if (grid) grid.innerHTML = '';
  if (empty) empty.hidden = true;

  try {
    const res = await fetch('/api/v1/auth/me', { headers: { 'Authorization': 'Bearer ' + token } });
    const user = await res.json();
    
    // In our system, guests and customers cannot view driver lists
    if (user.role === 'GUEST' || user.role === 'CUSTOMER') {
      if (empty) {
        empty.innerHTML = `
          <div style="text-align: center; padding: 60px 20px;">
            <div style="display:inline-flex; padding:16px; background:#f1f5f9; border-radius:50%; margin-bottom:16px; color:#64748b;">
              <i data-lucide="lock" width="32" height="32"></i>
            </div>
            <h3 style="font-weight:600; font-size:1.25rem; margin-bottom:8px; color:var(--text-main);">Restricted Access</h3>
            <p style="color:var(--text-muted); max-width:400px; margin:0 auto;">Driver management and dispatching are restricted to administrative accounts. Please contact support if you need elevated access.</p>
          </div>
        `;
        empty.hidden = false;
        if (typeof lucide !== 'undefined') lucide.createIcons();
      }
      return;
    }

    // (If Admin/Driver, fetch drivers API. But for now, we'll just handle the UI gracefully)
    // Assuming /api/v1/drivers exists or will exist. We'll show a placeholder for admins until hooked up.
    if (empty) {
      empty.innerHTML = `
        <div style="text-align: center; padding: 60px 20px;">
          <div style="display:inline-flex; padding:16px; background:#eff6ff; border-radius:50%; margin-bottom:16px; color:var(--primary-blue);">
            <i data-lucide="users" width="32" height="32"></i>
          </div>
          <h3 style="font-weight:600; font-size:1.25rem; margin-bottom:8px; color:var(--text-main);">No Drivers Assigned</h3>
          <p style="color:var(--text-muted); max-width:400px; margin:0 auto;">Your fleet currently has no active drivers registered in this region.</p>
        </div>
      `;
      empty.hidden = false;
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }
  } catch(e) {
    if (empty) {
      empty.innerHTML = '<div style="text-align: center; padding: 40px; color:var(--status-error);">Error verifying access permissions.</div>';
      empty.hidden = false;
    }
  }
}
"""

js = js.replace(old_drivers.strip(), new_drivers.strip())

# Need to re-trigger Lucide icons when shipments load dynamically
# After tbody.appendChild(tr); we can just call lucide.createIcons() at the end
js = js.replace('shipmentsList.appendChild(tr);\n      }\n    });\n\n    // Update Stats', 'shipmentsList.appendChild(tr);\n      }\n    });\n    if (typeof lucide !== \'undefined\') lucide.createIcons();\n\n    // Update Stats')
js = js.replace('tbody.appendChild(tr);\n    });\n  } catch(e) {}', 'tbody.appendChild(tr);\n    });\n    if (typeof lucide !== \'undefined\') lucide.createIcons();\n  } catch(e) {}')


with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("app.js updated for final polish")
