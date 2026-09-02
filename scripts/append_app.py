with open('frontend/app.js', 'a', encoding='utf-8') as f:
    f.write("""
// --- DASHBOARD DATA FETCHING (Step 2) ---
(function() {
  async function fetchDashboardData() {
    const token = localStorage.getItem('parcelpilot_token');
    if (!token) return;

    const shipmentsList = document.getElementById('shipments-page-list');
    const loadingState = document.getElementById('shipments-loading');
    const emptyState = document.getElementById('shipments-empty');
    const errorState = document.getElementById('shipments-error');

    if (shipmentsList && loadingState) {
      loadingState.hidden = false;
      shipmentsList.innerHTML = '';
      if(emptyState) emptyState.hidden = true;
      if(errorState) errorState.hidden = true;

      try {
        const res = await fetch('/api/v1/shipments', {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        const shipments = data.items || data;
        loadingState.hidden = true;

        if (shipments.length === 0) {
          if (emptyState) emptyState.hidden = false;
        } else {
          let inTransit = 0, delivered = 0, alerts = 0;
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
          });

          const statTotal = document.getElementById('stat-total');
          if (statTotal) statTotal.innerText = shipments.length;
          const statTransit = document.getElementById('stat-in-transit');
          if (statTransit) statTransit.innerText = inTransit;
          const statDelivered = document.getElementById('stat-delivered');
          if (statDelivered) statDelivered.innerText = delivered;
          const statAlerts = document.getElementById('stat-alerts');
          if (statAlerts) statAlerts.innerText = alerts;
        }
      } catch (err) {
        loadingState.hidden = true;
        if (errorState) errorState.hidden = false;
      }
    }
  }
  document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('parcelpilot_token')) fetchDashboardData();
  });
  window.fetchDashboardData = fetchDashboardData;
})();
""")
