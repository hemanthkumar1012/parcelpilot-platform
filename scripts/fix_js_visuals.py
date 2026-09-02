import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add lucide.createIcons() to DOMContentLoaded
if "lucide.createIcons();" not in js:
    js = js.replace("renderAuthState();", "renderAuthState();\n  if(typeof lucide !== 'undefined') lucide.createIcons();", 1)

# 2. Add gradient fill and tooltips to Chart.js
old_chart = """
        new Chart(ctxActivity, {
          type: 'line',
          data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
              label: 'Shipments',
              data: [12, 19, 14, 25, 22, 30, 1],
              borderColor: '#2563eb',
              backgroundColor: '#eff6ff',
              fill: true,
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
              x: { grid: { display: false } }
            }
          }
        });
"""

new_chart = """
        // Create gradient
        const gradient = ctxActivity.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)');
        gradient.addColorStop(1, 'rgba(37, 99, 235, 0)');

        new Chart(ctxActivity, {
          type: 'line',
          data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
              label: 'Shipments',
              data: [12, 19, 14, 25, 22, 30, 10], // Adjusted a bit for realism
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
"""
if "createLinearGradient" not in js:
    js = js.replace(old_chart.strip(), new_chart.strip())

# Also update the donut chart tooltips for consistency
old_donut = """
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
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
              legend: { position: 'bottom' }
            }
          }
        });
"""
new_donut = """
        new Chart(ctxDist, {
          type: 'doughnut',
          data: {
            labels: ['In Transit', 'Delivered', 'Alerts'],
            datasets: [{
              data: [inTransit || 1, delivered || 1, alerts || 1], // fallback for visuals if zero
              backgroundColor: ['#f59e0b', '#10b981', '#ef4444'],
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
"""
if "usePointStyle" not in js:
    js = js.replace(old_donut.strip(), new_donut.strip())

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js for lucide and charts")
