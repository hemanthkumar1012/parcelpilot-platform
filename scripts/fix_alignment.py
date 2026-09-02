import os
import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX BRANDING (Sidebar Top)
new_sidebar_top = """<div class="sidebar-top" style="display:flex; justify-content:space-between; align-items:center; padding: 16px 20px 8px;">
    <div class="brand-mark brand-mark-sidebar" style="display:flex; align-items:center; gap:12px; margin:0;">
      <div style="background: linear-gradient(135deg, #2563eb, #3b82f6); color: white; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(37,99,235,0.2);">
        <i data-lucide="package" width="18" height="18"></i>
      </div>
      <div class="brand-text" style="display:flex; flex-direction:column; align-items:flex-start;">
        <span class="brand-title" style="font-weight: 700; font-size: 1.15rem; color: #0f172a; letter-spacing: -0.025em; line-height: 1.2;">ParcelPilot</span>
        <span class="brand-subtitle" style="font-size: 0.75rem; color: #64748b; font-weight: 500;">Logistics Control</span>
      </div>
    </div>
    <button id="sidebar-close-btn" class="sidebar-close-btn" aria-label="Close menu" style="color: #64748b; background: none; border: none; cursor: pointer;">
      <i data-lucide="x" width="20" height="20"></i>
    </button>
  </div>"""

# Find the start of sidebar-top and the start of navigation
start_idx = html.find('<div class="sidebar-top">')
end_idx = html.find('<!-- ============================= NAVIGATION')
if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_sidebar_top + '\n\n  ' + html[end_idx:]

# 2. Fix the Dashboard main header title (if it failed too)
# Let's check if the topbar was actually replaced
if 'Operational overview across every shipment.' in html:
    start_topbar = html.find('<div class="topbar-titles"')
    end_topbar = html.find('<form id="global-search-form"')
    if start_topbar != -1 and end_topbar != -1:
        new_topbar_titles = """<div class="topbar-titles" style="display:flex; flex-direction:column; justify-content:center; flex:1;">
      <h1 id="page-title" style="margin:0; font-size: 1.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.025em; line-height: 1.2;">Dashboard</h1>
      <p id="page-subtitle" style="margin:4px 0 0 0; font-size: 0.875rem; color: #64748b; font-weight: 400;">Operational overview across every shipment.</p>
      <span id="guest-mode-badge" class="guest-mode-badge" style="margin-top: 4px; font-size: 0.7rem; font-weight: 600; color: #d97706; background: #fef3c7; padding: 2px 6px; border-radius: 4px; display:inline-block; width: fit-content;" hidden>DEMO MODE · READ ONLY</span>
    </div>\n\n    """
        html = html[:start_topbar] + new_topbar_titles + html[end_topbar:]

# 3. Add CSS fix for .mobile-menu-btn on desktop
css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

if "@media (min-width: 769px)" not in css:
    css += "\n\n@media (min-width: 769px) {\n  .mobile-menu-btn { display: none !important; }\n}\n"
else:
    # Just append it
    css += "\n@media (min-width: 769px) { .mobile-menu-btn { display: none !important; } }\n"

# 4. Make sure sidebar nav items have text-align left
if ".nav-item {" in css:
    css = css.replace('.nav-item {\n  display: flex;', '.nav-item {\n  display: flex;\n  text-align: left;\n  justify-content: flex-start;')

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)

print("Applied strict alignment and overhaul fixes")
