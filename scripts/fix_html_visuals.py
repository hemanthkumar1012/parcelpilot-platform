import os
import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Lucide script
if "lucide" not in html.lower():
    html = html.replace('</head>', '  <script src="https://unpkg.com/lucide@latest"></script>\n</head>')

# 2. Fix search placeholder
html = html.replace('placeholder="Search tracking ID, receiver, origin, destination…"', 'placeholder="Search shipments..."')
html = html.replace('placeholder="Search tracking ID, receiver,', 'placeholder="Search shipments..."') # Just in case

# 3. Replace icons with Lucide icons
# Hamburger
html = re.sub(r'<button class="mobile-menu-btn".*?>.*?</button>', '<button class="mobile-menu-btn"><i data-lucide="menu"></i></button>', html, flags=re.DOTALL)
# Close sidebar
html = re.sub(r'<button class="sidebar-close-btn".*?>.*?</button>', '<button class="sidebar-close-btn"><i data-lucide="x"></i></button>', html, flags=re.DOTALL)
# Search icons
html = re.sub(r'<span\s+class="search-icon"[^>]*>.*?</span>', '<span class="search-icon"><i data-lucide="search" width="16" height="16"></i></span>', html, flags=re.DOTALL)
# Nav icons (if any hardcoded)
# Let's replace the diamond icon in the dashboard nav
html = re.sub(r'<span class="nav-icon">.*?</span>\s*Dashboard', '<span class="nav-icon"><i data-lucide="layout-dashboard" width="18" height="18"></i></span> Dashboard', html, flags=re.DOTALL)
html = re.sub(r'<span class="nav-icon">.*?</span>\s*Shipments', '<span class="nav-icon"><i data-lucide="package" width="18" height="18"></i></span> Shipments', html, flags=re.DOTALL)
html = re.sub(r'<span class="nav-icon">.*?</span>\s*Tracking', '<span class="nav-icon"><i data-lucide="map-pin" width="18" height="18"></i></span> Tracking', html, flags=re.DOTALL)
html = re.sub(r'<span class="nav-icon">.*?</span>\s*Drivers', '<span class="nav-icon"><i data-lucide="truck" width="18" height="18"></i></span> Drivers', html, flags=re.DOTALL)
html = re.sub(r'<span class="nav-icon">.*?</span>\s*Notifications', '<span class="nav-icon"><i data-lucide="bell" width="18" height="18"></i></span> Notifications', html, flags=re.DOTALL)

# Modal close btn
html = re.sub(r'<button class="modal-close-btn"[^>]*>.*?</button>', '<button class="modal-close-btn"><i data-lucide="x"></i></button>', html, flags=re.DOTALL)
# AI widget close
html = re.sub(r'<button id="ai-close-btn"[^>]*>.*?</button>', '<button id="ai-close-btn" class="ai-close-btn"><i data-lucide="x"></i></button>', html, flags=re.DOTALL)

# 4. Fix "Status distribution" header collision
# Currently it's likely `<div class="panel-header panel-header-inline">` inside `.panel-distribution`
dist_header_pattern = r'<div class="panel-header panel-header-inline">\s*<h2>\s*Status distribution\s*</h2>\s*<p>\s*Share of shipments by current status.\s*</p>\s*</div>'
new_dist_header = """<div class="panel-header">
            <h2>Status distribution</h2>
            <p>Share of shipments by current status.</p>
          </div>"""
html = re.sub(dist_header_pattern, new_dist_header, html, flags=re.DOTALL)

# Fix Shipment activity header as well if it's inline
act_header_pattern = r'<div class="panel-header panel-header-inline">\s*<h2>\s*Shipment activity\s*</h2>\s*<p>\s*Route flow across the network, live-refreshed.\s*</p>\s*</div>'
new_act_header = """<div class="panel-header">
            <h2>Shipment activity</h2>
            <p>Route flow across the network, live-refreshed.</p>
          </div>"""
html = re.sub(act_header_pattern, new_act_header, html, flags=re.DOTALL)


with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Updated index.html")
