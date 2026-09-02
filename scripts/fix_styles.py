import os

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Sidebar Navigation (Step 3)
new_nav_css = """
/* Sidebar Nav */
.sidebar-nav { flex: 1; overflow-y: auto; padding: var(--space-2) 0; }
.nav-item {
  display: flex; align-items: center; gap: var(--space-3);
  padding: 12px var(--space-4);
  color: var(--text-muted);
  font-weight: 500;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
}
.nav-item:hover {
  background-color: var(--primary-light);
  color: var(--primary-blue);
}
.nav-item[aria-current="page"] {
  background-color: var(--primary-light);
  color: var(--primary-blue);
  border-left-color: var(--primary-blue);
}
.nav-item svg { width: 20px; height: 20px; }
"""

# Replace old nav-item
import re
css = re.sub(r'\.sidebar-nav\s*\{.*?\}.*?\.nav-badge\s*\{', new_nav_css + '\n.nav-badge {', css, flags=re.DOTALL)

# Icon buttons (Step 2)
# "The hamburger menu icon, the X close button, the diamond icon, and the ? help icon... restyle all of them as clean icon buttons"
# Let's add an .icon-btn class
icon_btn_css = """
/* Icon Buttons */
.icon-btn, .sidebar-close-btn, .mobile-menu-btn {
  display: flex; align-items: center; justify-content: center;
  width: 36px; height: 36px;
  border: none; background: transparent;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
}
.icon-btn:hover, .sidebar-close-btn:hover, .mobile-menu-btn:hover {
  background-color: var(--primary-light);
  color: var(--primary-blue);
}
.icon-btn svg { width: 20px; height: 20px; }
"""
css += "\n" + icon_btn_css

# Stat cards (Step 4)
# Add small icon badge tinted colors
stat_badge_css = """
/* Stat Card Badges */
.stat-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: var(--space-2);
}
.stat-icon {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.stat-icon svg { width: 18px; height: 18px; }
.stat-icon-total { background-color: var(--status-info-bg); color: var(--status-info); }
.stat-icon-transit { background-color: #fef3c7; color: #d97706; }
.stat-icon-delivered { background-color: var(--status-ok-bg); color: var(--status-ok); }
.stat-icon-alerts { background-color: var(--status-error-bg); color: var(--status-error); }
"""
css += "\n" + stat_badge_css

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print("Updated style.css")
