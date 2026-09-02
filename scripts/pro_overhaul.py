import os
import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD GOOGLE FONTS TO HEAD
if "fonts.googleapis.com" not in html:
    font_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n  <link rel="stylesheet"'
    html = html.replace('<link rel="stylesheet"', font_link)

# 2. FIX BRANDING (Sidebar Top)
new_sidebar_top = """<div class="sidebar-top">
    <div class="brand-mark brand-mark-sidebar" style="display:flex; align-items:center; gap:12px; padding: 8px 0;">
      <div style="background: linear-gradient(135deg, #2563eb, #3b82f6); color: white; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(37,99,235,0.2);">
        <i data-lucide="package" width="18" height="18"></i>
      </div>
      <div class="brand-text" style="display:flex; flex-direction:column;">
        <span class="brand-title" style="font-weight: 700; font-size: 1.15rem; color: #0f172a; letter-spacing: -0.025em; line-height: 1.2;">ParcelPilot</span>
        <span class="brand-subtitle" style="font-size: 0.75rem; color: #64748b; font-weight: 500;">Logistics Control</span>
      </div>
    </div>
    <button id="sidebar-close-btn" class="sidebar-close-btn" aria-label="Close menu" style="color: #64748b; background: none; border: none; cursor: pointer;">
      <i data-lucide="x" width="20" height="20"></i>
    </button>
  </div>"""
html = re.sub(r'<div class="sidebar-top">.*?</div>\s*<!-- ============================= NAVIGATION', new_sidebar_top + '\n\n  <!-- ============================= NAVIGATION', html, flags=re.DOTALL)

# 3. FIX NAV ITEMS (Replace Unicode with Lucide)
html = html.replace('<span\n        class="nav-icon"\n        aria-hidden="true">\n        ◇\n      </span>', '<i data-lucide="layout-dashboard" class="nav-icon" width="18" height="18"></i>')
html = html.replace('<span\n        class="nav-icon"\n        aria-hidden="true">\n        ▤\n      </span>', '<i data-lucide="boxes" class="nav-icon" width="18" height="18"></i>')
html = html.replace('<span\n        class="nav-icon"\n        aria-hidden="true">\n        ◎\n      </span>', '<i data-lucide="map" class="nav-icon" width="18" height="18"></i>')
html = html.replace('<span\n        class="nav-icon"\n        aria-hidden="true">\n        ▣\n      </span>', '<i data-lucide="users" class="nav-icon" width="18" height="18"></i>')
html = html.replace('<span\n        class="nav-icon"\n        aria-hidden="true">\n        ◈\n      </span>', '<i data-lucide="bell" class="nav-icon" width="18" height="18"></i>')

# Also catch potential single-line versions if formatter squashed them
html = html.replace('◇', '<i data-lucide="layout-dashboard" class="nav-icon" width="18" height="18"></i>')
html = html.replace('▤', '<i data-lucide="boxes" class="nav-icon" width="18" height="18"></i>')
html = html.replace('◎', '<i data-lucide="map" class="nav-icon" width="18" height="18"></i>')
html = html.replace('▣', '<i data-lucide="users" class="nav-icon" width="18" height="18"></i>')
html = html.replace('◈', '<i data-lucide="bell" class="nav-icon" width="18" height="18"></i>')

# 4. FIX SIDEBAR FOOTER
new_sidebar_bottom = """<div class="sidebar-bottom" style="border-top: 1px solid #e2e8f0; padding-top: 16px; margin-top: auto;">
    <div class="system-status" style="display:flex; align-items:center; gap:8px; margin-bottom: 16px; font-size: 0.8rem; color: #64748b; font-weight: 500;">
      <span style="width: 8px; height: 8px; border-radius: 50%; background-color: #10b981; display:inline-block; box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);"></span>
      All systems operational
    </div>
    <div class="sidebar-user" style="display:flex; align-items:center; gap:12px; margin-bottom: 16px;">
      <div class="user-avatar" id="sidebar-user-avatar" style="width: 36px; height: 36px; border-radius: 50%; background: #e2e8f0; color: #475569; display:flex; align-items:center; justify-content:center; font-weight: 600; font-size: 0.9rem;">
        <i data-lucide="user" width="18" height="18"></i>
      </div>
      <div class="user-meta" style="display:flex; flex-direction:column; overflow:hidden;">
        <span id="sidebar-user-name" class="user-name" style="font-weight: 600; font-size: 0.85rem; color: #0f172a; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">Guest Account</span>
        <span id="sidebar-user-email" class="user-email" style="font-size: 0.75rem; color: #64748b; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">Read-only demo access</span>
      </div>
    </div>
    <button id="logout-btn" class="icon-btn" style="width: 100%; display:flex; align-items:center; justify-content:center; gap:8px; padding: 8px; border: 1px solid #e2e8f0; background: #f8fafc; border-radius: 8px; color: #475569; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.2s;">
      <i data-lucide="log-out" width="16" height="16"></i> Log out
    </button>
  </div>"""
html = re.sub(r'<div class="sidebar-bottom">.*?</aside>', new_sidebar_bottom + '\n</aside>', html, flags=re.DOTALL)

# 5. FIX MAIN HEADER TITLE AND MOBILE MENU BTN
html = html.replace('aria-label="Open menu">\n      ☰\n    </button>', 'aria-label="Open menu" style="background:none; border:none; color:#0f172a; cursor:pointer;">\n      <i data-lucide="menu" width="24" height="24"></i>\n    </button>')
# Handle topbar-titles
new_topbar_titles = """<div class="topbar-titles" style="display:flex; flex-direction:column; justify-content:center;">
      <h1 id="page-title" style="margin:0; font-size: 1.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.025em; line-height: 1.2;">Dashboard</h1>
      <p id="page-subtitle" style="margin:4px 0 0 0; font-size: 0.875rem; color: #64748b; font-weight: 400;">Operational overview across every shipment.</p>
      <span id="guest-mode-badge" class="guest-mode-badge" style="margin-top: 4px; font-size: 0.7rem; font-weight: 600; color: #d97706; background: #fef3c7; padding: 2px 6px; border-radius: 4px; display:inline-block; width: fit-content;" hidden>DEMO MODE · READ ONLY</span>
    </div>"""
html = re.sub(r'<div class="topbar-titles">.*?</div>', new_topbar_titles, html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Updated index.html formatting")


css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# 1. APPLY GLOBAL FONT
if "font-family: 'Inter'" not in css:
    css = css.replace('font-family: system-ui, -apple-system, sans-serif;', "font-family: 'Inter', system-ui, -apple-system, sans-serif;")
    css = css.replace('font-family: inherit;', "font-family: 'Inter', system-ui, -apple-system, sans-serif;")

# 2. OVERHAUL SIDEBAR NAV ITEMS
# Strip out old nav-item borders if any
new_nav_item_css = """
/* Modern Nav Items */
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 14px;
  margin-bottom: 4px;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #475569;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}
.nav-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}
.nav-item[aria-current="page"] {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
}
.nav-item[aria-current="page"] .nav-icon {
  color: #2563eb;
}
.nav-icon {
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
}
"""
css += "\n" + new_nav_item_css

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print("Updated style.css formatting")
