// =========================================================================
// ParcelPilot — app.js
// =========================================================================

async function renderAuthState() {
  const token = localStorage.getItem('parcelpilot_token');
  const isLoggedIn = !!token;
  const loginView = document.getElementById('login-view');
  const dashboardView = document.getElementById('dashboard-view');
  
  if (loginView) loginView.hidden = isLoggedIn;
  if (dashboardView) {
    dashboardView.hidden = !isLoggedIn;
    if (isLoggedIn) {
      dashboardView.classList.remove('hidden');
      dashboardView.removeAttribute('hidden');
    }
  }
  
  if (isLoggedIn) {
    if (typeof fetchDashboardData === 'function') fetchDashboardData();
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
          <td><button class="icon-btn">&rarr;</button></td>
        `;
        shipmentsList.appendChild(tr);
      }
    });

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
  const distCanvas = document.getElementById('status-distribution');
  const actCanvas = document.getElementById('activity-chart');
  
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
        <td><button class="icon-btn">&rarr;</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch(e) {}
}

function loadDriversPage() {
  const grid = document.getElementById('drivers-grid');
  const empty = document.getElementById('drivers-empty');
  if (grid) grid.innerHTML = '';
  if (empty) empty.hidden = false;
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
      try {
        const res = await fetch('/api/v1/auth/guest', { method: 'POST' });
        if (!res.ok) throw new Error();
        const data = await res.json();
        localStorage.setItem('parcelpilot_token', data.access_token);
        renderAuthState();
      } catch (err) {}
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
