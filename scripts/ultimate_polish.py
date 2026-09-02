import os
import re

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
/* --- ULTIMATE POLISH OVERRIDES --- */

/* Panels */
.panel {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.05), 0 2px 4px -2px rgba(15, 23, 42, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}
.panel:hover {
  box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.05), 0 4px 6px -4px rgba(15, 23, 42, 0.05);
}
.panel-header {
  padding: 24px 24px 16px 24px;
  border-bottom: 1px solid #f1f5f9;
  display: block; /* explicitly override any old flex layouts */
  text-align: left;
}
.panel-header h2 {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px 0;
  letter-spacing: -0.025em;
}
.panel-header p {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

/* Fix Chart Container Padding */
.activity-chart, .status-distribution {
  padding: 24px;
  height: 320px; 
  position: relative;
  width: 100%;
}

/* Stat Cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}
.stat-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
}
.stat-card:nth-child(1)::before { background: #2563eb; }
.stat-card:nth-child(2)::before { background: #f59e0b; }
.stat-card:nth-child(3)::before { background: #10b981; }
.stat-card:nth-child(4)::before { background: #ef4444; }

.stat-card-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 16px 0;
}
.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
  margin: 0 0 8px 0;
  letter-spacing: -0.025em;
}
.stat-desc {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

/* Data Table Polish */
.data-table-wrapper {
  overflow-x: auto;
  width: 100%;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.data-table th {
  padding: 16px 24px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
}
.data-table td {
  padding: 16px 24px;
  font-size: 0.9rem;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}
.data-table tbody tr {
  transition: background-color 0.15s ease;
}
.data-table tbody tr:hover {
  background-color: #f8fafc;
}
"""

if "ULTIMATE POLISH OVERRIDES" not in css:
    css += "\n" + new_css
    with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(css)
print("Polished CSS injected")
