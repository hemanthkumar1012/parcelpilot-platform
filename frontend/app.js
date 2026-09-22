// =========================================================================
// ParcelPilot — app.js
// =========================================================================

async function renderAuthState() {
  const token = localStorage.getItem('parcelpilot_token');
  const isLoggedIn = !!token;
  const loginView = document.getElementById('login-view');
  const dashboardView = document.getElementById('dashboard-view');
  
  // Add base classes for transition
  if (loginView && !loginView.classList.contains('view-container')) loginView.classList.add('view-container');
  if (dashboardView && !dashboardView.classList.contains('view-container')) dashboardView.classList.add('view-container');

  if (isLoggedIn) {
    if (loginView) {
      loginView.classList.add('view-hidden');
      loginView.classList.remove('view-visible');
      setTimeout(() => { loginView.hidden = true; }, 400); // Wait for fade out
    }
    if (dashboardView) {
      dashboardView.hidden = false;
      dashboardView.classList.remove('hidden');
      // Small timeout to allow display:block to apply before opacity transition
      setTimeout(() => {
        dashboardView.classList.remove('view-hidden');
        dashboardView.classList.add('view-visible');
      }, 50);
    }
    
    // Switch default active page to dashboard if not set
    const currentActive = document.querySelector('.page:not(.hidden)');
    if (!currentActive) {
      document.querySelectorAll('.page').forEach(p => {
        if (p.id === 'page-dashboard') {
          p.classList.remove('hidden');
          p.hidden = false;
        } else {
          p.classList.add('hidden');
          p.hidden = true;
        }
      });
      document.querySelectorAll('.nav-item').forEach(nav => {
        if (nav.dataset.page === 'dashboard') nav.setAttribute('aria-current', 'page');
        else nav.removeAttribute('aria-current');
      });
    }
    
    if (typeof fetchDashboardData === 'function') fetchDashboardData();
  } else {
    // Logged out
    if (dashboardView) {
      dashboardView.classList.add('view-hidden');
      dashboardView.classList.remove('view-visible');
      setTimeout(() => { dashboardView.hidden = true; }, 400);
    }
    if (loginView) {
      loginView.hidden = false;
      setTimeout(() => {
        loginView.classList.remove('view-hidden');
        loginView.classList.add('view-visible');
      }, 50);
    }
  }
}

async function fetchDashboardData() {
  const token = localStorage.getItem('parcelpilot_token');
  if (!token) return;

  const shipmentsList = document.getElementById('recent-shipments-body');
  
  try {
    const res = await fetch('/api/v1/shipments', {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (!res.ok) throw new Error('Failed to fetch');
    const data = await res.json();
    const shipments = data.items || data;

    let inTransit = 0, delivered = 0, alerts = 0;
    const total = shipments.length;

    if (shipmentsList) shipmentsList.innerHTML = '';

    shipments.forEach(s => {
      if (s.current_status === 'IN_TRANSIT' || s.current_status === 'OUT_FOR_DELIVERY') inTransit++;
      if (s.current_status === 'DELIVERED') delivered++;
      if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) alerts++;

      if (shipmentsList) {
        const tr = document.createElement('tr');
        let dotClass = 'pending';
        if (s.current_status === 'DELIVERED') dotClass = 'ok';
        if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) dotClass = 'error';

        const eta = s.estimated_delivery ? new Date(s.estimated_delivery).toLocaleDateString() : '—';
        tr.innerHTML = `
          <td><strong>${s.tracking_id}</strong></td>
          <td>${s.origin}</td>
          <td>${s.destination}</td>
          <td>${s.receiver_name || '—'}</td>
          <td><span class="status-dot status-dot-${dotClass}">${s.current_status.replace(/_/g, ' ')}</span></td>
          <td>${eta}</td>
          <td><button class="icon-btn"><i data-lucide="chevron-right"></i></button></td>
        `;
        shipmentsList.appendChild(tr);
      }
    });
    if (typeof lucide !== 'undefined') lucide.createIcons();

    // Update Stats
    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-in-transit').textContent = inTransit;
    document.getElementById('stat-delivered').textContent = delivered;
    document.getElementById('stat-alerts').textContent = alerts;

    // Render Charts
    renderCharts(total, inTransit, delivered, alerts);
  } catch(e) {
    console.error('Error fetching dashboard data:', e);
  }
}

function renderCharts(total, inTransit, delivered, alerts) {
  if (window.Chart) Chart.defaults.font.family = "'Inter', system-ui, -apple-system, sans-serif";

  const distCanvas = document.getElementById('chart-distribution');
  const actCanvas = document.getElementById('chart-activity');
  
  if (distCanvas && window.Chart) {
    const ctxDist = distCanvas.getContext('2d');
    if (window.distChart) window.distChart.destroy();
    window.distChart = new Chart(ctxDist, {
      type: 'doughnut',
      data: {
        labels: ['In Transit', 'Delivered', 'Alerts', 'Other'],
        datasets: [{
          data: [inTransit, delivered, alerts, Math.max(0, total - inTransit - delivered - alerts)],
          backgroundColor: ['#f59e0b', '#10b981', '#ef4444', '#e2e8f0'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: {
          legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true } },
          tooltip: {
            backgroundColor: '#ffffff',
            titleColor: '#0f172a',
            bodyColor: '#334155',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8
          }
        }
      }
    });
  }

  if (actCanvas && window.Chart) {
    const ctxAct = actCanvas.getContext('2d');
    const gradient = ctxAct.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)');
    gradient.addColorStop(1, 'rgba(37, 99, 235, 0)');
    
    if (window.actChart) window.actChart.destroy();
    window.actChart = new Chart(ctxAct, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Shipments',
          data: [12, 19, 14, 25, 22, 30, total],
          borderColor: '#2563eb',
          borderWidth: 3,
          backgroundColor: gradient,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#2563eb',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
          legend: { display: false },
          tooltip: {
            backgroundColor: '#ffffff',
            titleColor: '#0f172a',
            bodyColor: '#334155',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              label: function(context) { return context.parsed.y + ' shipments'; }
            },
            boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
          }
        },
        scales: {
          y: { beginAtZero: true, grid: { color: '#f1f5f9', drawBorder: false }, border: { dash: [4, 4] } },
          x: { grid: { display: false }, border: { display: false } }
        }
      }
    });
  }
}

async function fetchShipmentsPage() {
  const token = localStorage.getItem('parcelpilot_token');
  if (!token) return;
  const tbody = document.getElementById('shipments-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';
  try {
    const res = await fetch('/api/v1/shipments', { headers: { 'Authorization': 'Bearer ' + token }});
    const data = await res.json();
    const shipments = data.items || data;
    shipments.forEach(s => {
      const tr = document.createElement('tr');
      let dotClass = 'pending';
      if (s.current_status === 'DELIVERED') dotClass = 'ok';
      if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) dotClass = 'error';
      const eta = s.estimated_delivery ? new Date(s.estimated_delivery).toLocaleDateString() : '—';
      tr.innerHTML = `
        <td><strong>${s.tracking_id}</strong></td>
        <td>${s.origin}</td>
        <td>${s.destination}</td>
        <td>${s.receiver_name || '—'}</td>
        <td><span class="status-dot status-dot-${dotClass}">${s.current_status.replace(/_/g, ' ')}</span></td>
        <td>${eta}</td>
        <td><button class="icon-btn"><i data-lucide="chevron-right"></i></button></td>
      `;
      tbody.appendChild(tr);
    });
    if (typeof lucide !== 'undefined') lucide.createIcons();
  } catch(e) {}
}

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

async function fetchNotificationsPage() {
  const token = localStorage.getItem('parcelpilot_token');
  if (!token) return;
  const list = document.getElementById('notifications-page-list');
  if (!list) return;
  list.innerHTML = '';
  try {
    const res = await fetch('/api/v1/notifications', { headers: { 'Authorization': 'Bearer ' + token }});
    const data = await res.json();
    const notifications = data.items || [];
    notifications.forEach(n => {
      const li = document.createElement('li');
      li.style.padding = '16px';
      li.style.borderBottom = '1px solid #e2e8f0';
      li.innerHTML = `<strong>${n.title}</strong><p>${n.message}</p><small>${new Date(n.created_at).toLocaleString()}</small>`;
      list.appendChild(li);
    });
  } catch(e) {}
}

function initTiltEffect(selector) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll(selector).forEach(card => {
    card.style.transformStyle = 'preserve-3d';
    card.style.transition = 'transform 150ms ease, box-shadow 150ms ease';
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const rotateX = ((y - rect.height/2) / (rect.height/2)) * -5;
      const rotateY = ((x - rect.width/2) / (rect.width/2)) * 5;
      card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  renderAuthState();
  if (typeof lucide !== 'undefined') lucide.createIcons();
  
  setTimeout(() => initTiltEffect('.stat-card, .panel, .login-form-card'), 500);

  
  // SHIPMENTS PAGE LOGIC
  const searchInput = document.getElementById('shipment-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase();
      const rows = document.querySelectorAll('#shipments-table-body tr');
      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }

  const refreshBtn = document.getElementById('shipments-refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', async () => {
      const icon = refreshBtn.querySelector('svg');
      if (icon) icon.style.transform = 'rotate(180deg)';
      if (icon) icon.style.transition = 'transform 0.3s ease';
      await fetchShipmentsPage();
      setTimeout(() => { if(icon) icon.style.transform = 'rotate(0deg)'; }, 300);
    });
  }

  const newShipmentBtn = document.getElementById('new-shipment-btn');
  const modal = document.getElementById('new-shipment-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const nsForm = document.getElementById('new-shipment-form');

  if (newShipmentBtn && modal) {
    newShipmentBtn.addEventListener('click', () => {
      modal.classList.remove('hidden');
    });
  }
  if (closeModalBtn && modal) {
    closeModalBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
    });
  }
  if (nsForm) {
    nsForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const origin = document.getElementById('ns-origin').value;
      const destination = document.getElementById('ns-destination').value;
      const receiver = document.getElementById('ns-receiver').value;
      const sender = document.getElementById('ns-sender').value;
      
      const token = localStorage.getItem('parcelpilot_token');
      const submitBtn = document.getElementById('ns-submit-btn');
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.7';
      submitBtn.textContent = 'Creating...';

      try {
        const payload = { origin, destination, receiver_name: receiver, sender_name: sender };
        const res = await fetch('/api/v1/shipments', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify(payload)
        });
        
        if (res.ok) {
          modal.classList.add('hidden');
          nsForm.reset();
          await fetchShipmentsPage();
          if (typeof fetchDashboardData === 'function') fetchDashboardData(); // Update dashboard too
        } else {
          alert('Failed to create shipment. Please try again.');
        }
      } catch (err) {
        console.error(err);
        alert('Connection error.');
      } finally {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.textContent = 'Create Shipment';
      }
    });
  }

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('parcelpilot_token');
      renderAuthState();
    });
  }

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
          p.removeAttribute('hidden');
        } else {
          p.classList.add('hidden');
          p.setAttribute('hidden', '');
        }
      });
      if (item.dataset.page === 'shipments') fetchShipmentsPage();
      if (item.dataset.page === 'drivers') loadDriversPage();
      if (item.dataset.page === 'notifications') fetchNotificationsPage();
    });
  });

  const loginForm = document.getElementById('login-form');
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
        if (!res.ok) throw new Error();
        const data = await res.json();
        localStorage.setItem('parcelpilot_token', data.access_token);
        renderAuthState();
      } catch (err) {}
    });
  }

  const guestBtnClass = document.querySelector('.guest-mode-btn');
  if (guestBtnClass) {
    guestBtnClass.addEventListener('click', async () => {
      if (guestBtnClass.disabled) return;

      guestBtnClass.classList.add('btn-loading');
      guestBtnClass.disabled = true;

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);

      try {
        const res = await fetch('/api/v1/auth/guest', {
          method: 'POST',
          signal: controller.signal,
          headers: { 'Accept': 'application/json' }
        });

        const raw = await res.text();
        let data = {};
        try {
          data = raw ? JSON.parse(raw) : {};
        } catch (_) {
          data = { error: { message: raw || 'Invalid server response' } };
        }

        if (!res.ok || !data.access_token) {
          const message = data?.error?.message || data?.detail || 'Guest login failed';
          throw new Error(message);
        }

        localStorage.setItem('parcelpilot_token', data.access_token);
        renderAuthState();
      } catch (err) {
        console.error('Guest login failed:', err);
        const loginError = document.getElementById('login-error');
        if (loginError) {
          loginError.textContent =
            err?.name === 'AbortError'
              ? 'Guest login timed out. The API/database is not responding.'
              : (err?.message || 'Guest login failed. Please try again.');
          loginError.hidden = false;
        }
      } finally {
        clearTimeout(timeoutId);
        guestBtnClass.classList.remove('btn-loading');
        guestBtnClass.disabled = false;
      }
    });
  }

  const aiFloatingBtn = document.getElementById('ai-floating-btn');
  const aiWidget = document.getElementById('ai-assistant-widget');
  const aiCloseBtn = document.getElementById('ai-close-btn');
  if (aiFloatingBtn && aiWidget && aiCloseBtn) {
    aiFloatingBtn.addEventListener('click', () => aiWidget.classList.remove('hidden'));
    aiCloseBtn.addEventListener('click', () => aiWidget.classList.add('hidden'));
  }
  
  const aiForm = document.getElementById('ai-form');
  const aiMessages = document.getElementById('ai-messages');
  if (aiForm) {
    aiForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('ai-input');
      const text = input.value.trim();
      if (!text) return;
      
      const userMsg = document.createElement('div');
      userMsg.className = 'ai-message ai-message-user';
      userMsg.textContent = text;
      aiMessages.appendChild(userMsg);
      input.value = '';
      aiMessages.scrollTop = aiMessages.scrollHeight;

      try {
        const token = localStorage.getItem('parcelpilot_token');
        const res = await fetch('/api/v1/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        const aiMsg = document.createElement('div');
        aiMsg.className = 'ai-message ai-message-assistant';
        aiMsg.textContent = data.response;
        aiMessages.appendChild(aiMsg);
        aiMessages.scrollTop = aiMessages.scrollHeight;
      } catch (err) {}
    });
  }
  
  const trackForm = document.getElementById('tracking-form');
  if (trackForm) {
    trackForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('tracking-input').value.trim();
      const resultDiv = document.getElementById('tracking-page-result');
      if(resultDiv) resultDiv.innerHTML = '<div class="spinner" style="margin:20px auto"></div>';
      
      try {
        const res = await fetch(`/api/v1/shipments/track/${id}`);
        if (!res.ok) throw new Error();
        const s = await res.json();
        let dotClass = 'pending';
        if (s.current_status === 'DELIVERED') dotClass = 'ok';
        if (['FAILED', 'CANCELLED', 'RETURNED'].includes(s.current_status)) dotClass = 'error';
        if(resultDiv) resultDiv.innerHTML = `
          <div class="panel" style="margin-top:20px; padding:24px">
            <h3 style="margin-bottom:12px">Tracking: ${s.tracking_id}</h3>
            <div><strong>Status:</strong> <span class="status-dot status-dot-${dotClass}">${s.current_status.replace(/_/g, ' ')}</span></div>
          </div>
        `;
      } catch(e) {
        if(resultDiv) resultDiv.innerHTML = '<div class="panel" style="margin-top:20px; padding:24px; color:var(--status-error)">Shipment not found.</div>';
      }
    });
  }
});
