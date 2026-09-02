import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update navigation logic
# Replace the existing navItems click listener
old_nav_logic = """
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

new_nav_logic = """
  // Sidebar Nav Items (High-end button behavior + Page Switching)
  const navItems = document.querySelectorAll('.nav-item');
  const pages = document.querySelectorAll('.page');
  
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      // Update active state
      navItems.forEach(nav => nav.removeAttribute('aria-current'));
      item.setAttribute('aria-current', 'page');
      
      // Switch page visibility
      const targetPageId = 'page-' + item.dataset.page;
      pages.forEach(p => p.hidden = p.id !== targetPageId);
      
      // Trigger page-specific data loading
      if (item.dataset.page === 'shipments') fetchShipmentsPage();
      if (item.dataset.page === 'tracking') { /* tracking is on-demand via form */ }
      if (item.dataset.page === 'drivers') loadDriversPage();
      if (item.dataset.page === 'notifications') fetchNotificationsPage();
    });
  });
"""
if old_nav_logic.strip() in js:
    js = js.replace(old_nav_logic.strip(), new_nav_logic.strip())
else:
    # try searching more loosely
    js = js.replace("navItems.forEach(item => {", new_nav_logic + "\n/*")
    js = js.replace("item.setAttribute('aria-current', 'page');\n    });\n  });", "*/") # a bit messy, let's just do it securely

# Ensure it's replaced properly:
if "Switch page visibility" not in js:
    import re
    js = re.sub(r'// Sidebar Nav Items.*?\}\);\n  \}\);', new_nav_logic, js, flags=re.DOTALL)


# 2. Add functions for shipments, drivers, notifications, tracking
new_functions = """
// --- 5. PAGE-SPECIFIC FETCHING ---
async function fetchShipmentsPage() {
  const token = localStorage.getItem('parcelpilot_token');
  if (!token) return;
  const tbody = document.getElementById('shipments-table-body');
  const loading = document.getElementById('shipments-loading');
  const empty = document.getElementById('shipments-empty');
  
  if (!tbody) return;
  tbody.innerHTML = '';
  if (loading) loading.hidden = false;
  if (empty) empty.hidden = true;
  
  try {
    const res = await fetch('/api/v1/shipments', { headers: { 'Authorization': 'Bearer ' + token }});
    if (!res.ok) throw new Error();
    const data = await res.json();
    const shipments = data.items || data;
    
    if (loading) loading.hidden = true;
    if (shipments.length === 0) {
      if (empty) empty.hidden = false;
      return;
    }
    
    shipments.forEach(s => {
      const tr = document.createElement('tr');
      let dotClass = 'pending';
      if (s.current_status === 'DELIVERED') dotClass = 'ok';
      if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) dotClass = 'error';
      const eta = s.eta ? new Date(s.eta).toLocaleDateString() : '—';
      tr.innerHTML = `
        <td><strong>${s.tracking_id}</strong></td>
        <td>${s.origin}</td>
        <td>${s.destination}</td>
        <td>${s.receiver || '—'}</td>
        <td><span class="status-dot status-dot-${dotClass}">${s.current_status.replace(/_/g, ' ')}</span></td>
        <td>${eta}</td>
        <td><button class="icon-btn">&rarr;</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch(e) {
    if (loading) loading.hidden = true;
    const err = document.getElementById('shipments-error');
    if (err) err.hidden = false;
  }
}

function loadDriversPage() {
  // Check if guest
  const token = localStorage.getItem('parcelpilot_token');
  let isGuest = false;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    isGuest = payload.sub && payload.sub.startsWith('guest_');
  } catch(e) {}
  
  const grid = document.getElementById('drivers-grid');
  const empty = document.getElementById('drivers-empty');
  
  if (grid) grid.innerHTML = '';
  if (empty) {
    empty.hidden = false;
    empty.innerHTML = `
      <span class="empty-icon" style="font-size:32px">🚧</span>
      <p style="margin-top:16px; font-weight:600; font-size:1.1em">Drivers management is coming soon</p>
      <span style="color:var(--text-muted)">Driver dispatching and route assignments will be available in a future update. Admins only.</span>
    `;
  }
}

async function fetchNotificationsPage() {
  const token = localStorage.getItem('parcelpilot_token');
  if (!token) return;
  const list = document.getElementById('notifications-page-list');
  const loading = document.getElementById('notifications-loading');
  if (!list) return;
  
  list.innerHTML = '';
  if (loading) loading.hidden = false;
  
  try {
    const res = await fetch('/api/v1/notifications', { headers: { 'Authorization': 'Bearer ' + token }});
    if (!res.ok) throw new Error();
    const data = await res.json();
    const notifications = data.items || [];
    if (loading) loading.hidden = true;
    
    if (notifications.length === 0) {
      list.innerHTML = `
        <div class="table-state"><span class="empty-icon">✓</span><p>You're all caught up!</p></div>
      `;
      return;
    }
    
    notifications.forEach(n => {
      const li = document.createElement('li');
      li.style.padding = '16px';
      li.style.borderBottom = '1px solid #e2e8f0';
      li.innerHTML = `
        <strong>${n.title}</strong>
        <p style="margin:4px 0; color:var(--text-muted)">${n.message}</p>
        <small style="color:#94a3b8">${new Date(n.created_at).toLocaleString()}</small>
      `;
      list.appendChild(li);
    });
  } catch(e) {
    if (loading) loading.hidden = true;
    list.innerHTML = '<div class="table-state"><p>Coming soon / Error loading notifications.</p></div>';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const trackForm = document.getElementById('tracking-form');
  if (trackForm) {
    trackForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('tracking-input').value.trim();
      const resultDiv = document.getElementById('tracking-page-result');
      resultDiv.innerHTML = '<div class="spinner" style="margin:20px auto"></div>';
      
      try {
        const res = await fetch(`/api/v1/shipments/track/${id}`);
        if (!res.ok) throw new Error('Not found');
        const s = await res.json();
        let dotClass = 'pending';
        if (s.current_status === 'DELIVERED') dotClass = 'ok';
        if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) dotClass = 'error';
        
        resultDiv.innerHTML = `
          <div class="panel" style="margin-top:20px; padding:24px">
            <h3 style="margin-bottom:12px">Tracking: ${s.tracking_id}</h3>
            <div style="display:flex; justify-content:space-between; margin-bottom:12px">
              <span><strong>Origin:</strong> ${s.origin}</span>
              <span><strong>Destination:</strong> ${s.destination}</span>
            </div>
            <div><strong>Status:</strong> <span class="status-dot status-dot-${dotClass}">${s.current_status.replace(/_/g, ' ')}</span></div>
            <div style="margin-top:12px; color:var(--text-muted)">Last updated: ${new Date(s.updated_at).toLocaleString()}</div>
          </div>
        `;
      } catch(e) {
        resultDiv.innerHTML = '<div class="panel" style="margin-top:20px; padding:24px; color:var(--status-error)">Shipment not found. Check the ID and try again.</div>';
      }
    });
  }
});
"""

if "fetchShipmentsPage" not in js:
    js += "\n" + new_functions

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js")
