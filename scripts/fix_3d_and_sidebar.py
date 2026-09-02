import os

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

import_statement = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');\n"
if "@import url" not in css:
    css = import_statement + css

# Ensure body uses it
css = css.replace("font-family: 'Inter', system-ui, -apple-system, sans-serif;", "font-family: 'Inter', system-ui, sans-serif;")
if "body {" in css:
    css = css.replace("body {\n  margin: 0;", "body {\n  margin: 0;\n  font-family: 'Inter', system-ui, sans-serif;")

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)

print("Injected Google Fonts via @import")

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Shipments Toolbar properly (since regex failed)
start_idx = html.find('<div class="toolbar">')
end_idx = html.find('<div class="panel data-table">')

if start_idx != -1 and end_idx != -1:
    new_toolbar = """<div class="toolbar" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; margin-bottom:24px;">

        <div class="search-input-wrapper" style="max-width: 400px; flex: 1; position:relative; display:flex; align-items:center;">
          <i data-lucide="search" class="search-prefix-icon" style="position:absolute; left:12px; color:#94a3b8; width:18px; height:18px; pointer-events:none;"></i>
          <input
            type="text"
            id="shipment-search-input"
            placeholder="Search by tracking ID, receiver, origin..." 
            style="width: 100%; padding: 12px 16px 12px 40px; border-radius: 12px; border: 1px solid #e2e8f0; background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%); box-shadow: inset 0 2px 4px rgba(15,23,42,0.02), 0 2px 4px rgba(15,23,42,0.04); font-family: 'Inter', sans-serif; font-size: 0.95rem; color: #0f172a; transition: all 0.2s;" />
        </div>

        <div class="toolbar-actions" style="display:flex; gap:12px;">
          <button id="shipments-refresh-btn" class="btn btn-secondary" style="background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); border: 1px solid #e2e8f0; color: #475569; border-radius: 10px; font-weight: 600; font-family: 'Inter', sans-serif; padding: 10px 16px; box-shadow: 0 1px 2px rgba(15,23,42,0.05); display: flex; align-items: center; gap: 8px; cursor: pointer; transition: all 0.2s;">
            <i data-lucide="refresh-cw" width="16" height="16"></i> Refresh
          </button>

          <button id="new-shipment-btn" class="btn btn-primary" style="background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%); color: white; border: 1px solid #1d4ed8; border-radius: 10px; font-weight: 600; font-family: 'Inter', sans-serif; padding: 10px 18px; box-shadow: 0 4px 6px rgba(37,99,235,0.2), inset 0 1px 0 rgba(255,255,255,0.2); display: flex; align-items: center; gap: 8px; cursor: pointer; transition: all 0.2s; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">
            <i data-lucide="plus" width="18" height="18"></i> New shipment
          </button>
        </div>

      </div>

      """
    html = html[:start_idx] + new_toolbar + html[end_idx:]


# Also let's completely overhaul the Sidebar branding to be absolutely bulletproof layout-wise.
# The issue in the screenshot might be that .brand-mark-sidebar has display:flex AND flex-direction:column from somewhere, or it's wrapped tight.
sidebar_start = html.find('<div class="sidebar-top"')
sidebar_end = html.find('<!-- ============================= NAVIGATION')
if sidebar_start != -1 and sidebar_end != -1:
    perfect_sidebar = """<div class="sidebar-top" style="padding: 20px 24px 12px; border-bottom: 1px solid transparent; display: flex; justify-content: space-between; align-items: center;">
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); color: white; border-radius: 10px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(37,99,235,0.3), inset 0 1px 0 rgba(255,255,255,0.2);">
        <i data-lucide="package" width="20" height="20"></i>
      </div>
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <span style="font-family: 'Inter', sans-serif; font-weight: 800; font-size: 1.25rem; color: #0f172a; letter-spacing: -0.03em; line-height: 1.1;">ParcelPilot</span>
        <span style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">Logistics Control</span>
      </div>
    </div>
    <button id="sidebar-close-btn" class="sidebar-close-btn" aria-label="Close menu" style="background: none; border: none; color: #94a3b8; cursor: pointer; padding: 4px; display: flex; align-items: center; justify-content: center; transition: color 0.2s;">
      <i data-lucide="x" width="20" height="20"></i>
    </button>
  </div>

  """
    html = html[:sidebar_start] + perfect_sidebar + html[sidebar_end:]

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Applied 3D styling and bulletproof sidebar alignment")
