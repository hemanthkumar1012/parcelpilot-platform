import os
import re

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Change .nav-item to be a box-structured high-end button
new_nav_item = """
/* Sidebar Nav - Box Structured Buttons */
.sidebar-nav { flex: 1; overflow-y: auto; padding: var(--space-3) var(--space-3); display: flex; flex-direction: column; gap: 8px; }
.nav-item {
  display: flex; align-items: center; gap: var(--space-3);
  padding: 12px 16px;
  color: var(--text-muted);
  font-weight: 500;
  cursor: pointer;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}
.nav-item:hover {
  background-color: var(--bg-app);
  border-color: #cbd5e1;
  color: var(--text-main);
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}
.nav-item[aria-current="page"] {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}
.nav-item svg { width: 20px; height: 20px; }

/* Fix logout button to match */
#logout-btn {
  display: flex; align-items: center; justify-content: center;
  padding: 10px 16px;
  background-color: white;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  color: var(--text-main);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  width: 100%;
}
#logout-btn:hover {
  background-color: #fef2f2;
  border-color: #fecaca;
  color: #ef4444;
}
"""

css = re.sub(r'/\* Sidebar Nav \*/.*?(?=\.nav-badge)', new_nav_item, css, flags=re.DOTALL)

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
