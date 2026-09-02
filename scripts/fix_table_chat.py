import os
import re

# 1. Update app.js to fix ETA and Receiver mappings
js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# fetchDashboardData mapping
js = js.replace("<td>${s.receiver || '—'}</td>", "<td>${s.receiver_name || '—'}</td>")
js = js.replace("const eta = s.eta ? new Date(s.eta).toLocaleDateString() : '—';", 
                "const eta = s.estimated_delivery ? new Date(s.estimated_delivery).toLocaleDateString() : '—';")
js = js.replace("<td>${s.receiver_name || '—'}</td>\n            <td><span class=\"status-dot status-dot-${dotClass}\">${s.current_status.replace(/_/g, ' ')}</span></td>\n            <td>${eta}</td>",
                "<td>${s.receiver_name || '—'}</td>\n            <td><span class=\"status-dot status-dot-${dotClass}\">${s.current_status.replace(/_/g, ' ')}</span></td>\n            <td>${eta}</td>")

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js fields")

# 2. Update style.css for data-table and ai-widget
css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Check if data-table is already present
if ".data-table {" not in css:
    table_css = """
/* Data Table Styles */
.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.data-table th {
  padding: var(--space-3) var(--space-4);
  font-weight: 600;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-light);
  background-color: var(--bg-app);
}
.data-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--border-light);
  color: var(--text-main);
  vertical-align: middle;
}
.data-table tr:hover td {
  background-color: var(--primary-light);
}
"""
    css += "\n" + table_css

# Add mobile media query for ai-widget
mobile_css = """
@media (max-width: 480px) {
  .ai-widget {
    bottom: 0; right: 0; left: 0;
    width: 100%; 
    height: 85vh;
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
    border: none;
    border-top: 1px solid var(--border-light);
    box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
  }
}
"""
if "@media (max-width: 480px)" not in css:
    css += "\n" + mobile_css

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print("Updated style.css for tables and mobile widget")

# 3. Update app/services/ai.py for the mock message
py_path = 'app/services/ai.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py = f.read()

old_msg = '"This is a mock AI response since OPENAI_API_KEY is not set. I see you asked: " + user_message'
new_msg = '"AI assistant is running in demo mode right now — responses are simulated."'

py = py.replace(old_msg, new_msg)
with open(py_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(py)
print("Updated ai.py mock message")
