import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Include Chart.js
if 'chart.js' not in html:
    html = html.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>')

# 2. Add canvas to activity-chart and status-distribution
if 'id="chart-activity"' not in html:
    html = re.sub(r'(<div\s+id="activity-chart"[^>]*>)', r'\1\n  <canvas id="chart-activity"></canvas>', html)
if 'id="chart-distribution"' not in html:
    html = re.sub(r'(<div\s+id="status-distribution"[^>]*>)', r'\1\n  <canvas id="chart-distribution"></canvas>', html)

# 3. Stat Cards Icons
svg_total = '<div class="stat-icon stat-icon-total"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg></div>'
svg_transit = '<div class="stat-icon stat-icon-transit"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg></div>'
svg_delivered = '<div class="stat-icon stat-icon-delivered"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div>'
svg_alerts = '<div class="stat-icon stat-icon-alerts"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg></div>'

def add_stat_header(label, html_content, svg):
    # wrap stat-label and add the stat-icon in a stat-header div
    pattern = rf'<div class="stat-label">[\s]*{label}[\s]*</div>'
    replacement = f'<div class="stat-header"><div class="stat-label">{label}</div>{svg}</div>'
    return re.sub(pattern, replacement, html_content)

html = add_stat_header('Total shipments', html, svg_total)
html = add_stat_header('In transit', html, svg_transit)
html = add_stat_header('Delivered', html, svg_delivered)
html = add_stat_header('Operational alerts', html, svg_alerts)

# Ensure toolbar buttons have icon-btn class
# Replace <button class="btn btn-ghost icon-btn" ...> or just add icon-btn if missing.
html = re.sub(r'class="btn btn-ghost([^"]*)"', r'class="icon-btn\1"', html)

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Updated index.html")
