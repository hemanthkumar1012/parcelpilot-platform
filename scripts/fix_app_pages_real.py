import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update navigation logic
new_nav_logic = """
  // Sidebar Nav Items (High-end button behavior + Page Switching)
  const navItems = document.querySelectorAll('.nav-item');
  const pages = document.querySelectorAll('.page');
  
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(nav => nav.removeAttribute('aria-current'));
      item.setAttribute('aria-current', 'page');
      
      const targetPageId = 'page-' + item.dataset.page;
      pages.forEach(p => {
        if (p.id === targetPageId) {
          p.classList.remove('hidden');
        } else {
          p.classList.add('hidden');
        }
      });
      
      if (item.dataset.page === 'shipments') fetchShipmentsPage();
      if (item.dataset.page === 'drivers') loadDriversPage();
      if (item.dataset.page === 'notifications') fetchNotificationsPage();
    });
  });
"""
import re
js = re.sub(r'// Sidebar Nav Items.*?(?=\s*\}\);\n\}\);)', new_nav_logic, js, flags=re.DOTALL)


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
      <div style="text-align: center; padding: 40px;">
        <span class="empty-icon" style="font-size:48px">🚧</span>
        <h3 style="margin-top:16px; font-weight:600; font-size:1.4em">Drivers management is coming soon</h3>
        <p style="color:var(--text-muted); margin-top:8px">Driver dispatching and route assignments will be available in a future update. Admins only.</p>
      </div>
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
    list.innerHTML = '<div class="table-state"><p>Error loading notifications.</p></div>';
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

# append to the very end
js += "\n" + new_functions

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js correctly")
