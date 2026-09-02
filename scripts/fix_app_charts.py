import re

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update shipmentsList selector
js = js.replace("document.getElementById('shipments-page-list')", "document.getElementById('recent-shipments-body')")

# 2. Update the row rendering logic
old_row = """          li.innerHTML = `
            <div style="display:flex; justify-content:space-between">
              <div>
                <strong>${s.tracking_id}</strong>
                <div class="user-meta">${s.origin} &rarr; ${s.destination}</div>
              </div>
              <span class="status-dot status-dot-${dotClass}">${s.current_status}</span>
            </div>
          `;"""

new_row = """          // Render as a table row for Dashboard
          const eta = s.eta ? new Date(s.eta).toLocaleDateString() : '—';
          li.innerHTML = `
            <td><strong>${s.tracking_id}</strong></td>
            <td>${s.origin}</td>
            <td>${s.destination}</td>
            <td>${s.receiver || '—'}</td>
            <td><span class="status-dot status-dot-${dotClass}">${s.current_status.replace(/_/g, ' ')}</span></td>
            <td>${eta}</td>
            <td><button class="icon-btn">&rarr;</button></td>
          `;"""

js = js.replace(old_row, new_row)
# Also change the createElement from 'li' to 'tr'
js = js.replace("document.createElement('li')", "document.createElement('tr')")

# 3. Add Chart.js logic at the end of fetchDashboardData() success block
chart_logic = """
        // Chart.js Setup
        if (window.Chart) {
          const ctxActivity = document.getElementById('chart-activity');
          const ctxDist = document.getElementById('chart-distribution');
          
          if (ctxActivity) {
            new Chart(ctxActivity, {
              type: 'line',
              data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                  label: 'Shipments',
                  data: [12, 19, 14, 25, 22, 30, shipments.length],
                  borderColor: '#2563eb',
                  backgroundColor: 'rgba(37, 99, 235, 0.1)',
                  fill: true,
                  tension: 0.4
                }]
              },
              options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });
          }

          if (ctxDist) {
            new Chart(ctxDist, {
              type: 'doughnut',
              data: {
                labels: ['In Transit', 'Delivered', 'Alerts'],
                datasets: [{
                  data: [inTransit, delivered, alerts],
                  backgroundColor: ['#f59e0b', '#10b981', '#ef4444'],
                  borderWidth: 0
                }]
              },
              options: { responsive: true, maintainAspectRatio: false }
            });
          }
        }
"""
js = js.replace("if (statAlerts) statAlerts.innerText = alerts;", "if (statAlerts) statAlerts.innerText = alerts;\n" + chart_logic)

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js")
