import os
import re

# 1. Fix the broken HTML placeholder and inject search icon
html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken placeholder
html = re.sub(r'placeholder="Search shipments\.\.\."[^"]*"', 'placeholder="Search shipments..."', html)

# Add search icon inside the form if not present, and replace ⏎ with a stylish button
old_search_form_pattern = r'<form[^>]*id="global-search-form"[^>]*>.*?</form>'
new_search_form = """<form id="global-search-form" class="global-search" role="search">
      <div class="search-input-wrapper">
        <i data-lucide="search" class="search-prefix-icon"></i>
        <input type="text" id="global-search-input" placeholder="Search shipments..." aria-label="Global shipment search" />
        <div class="search-kbd-shortcut">
          <kbd>⌘</kbd><kbd>K</kbd>
        </div>
      </div>
    </form>"""

html = re.sub(old_search_form_pattern, new_search_form, html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Updated HTML for 3D search bar")

# 2. Add 3D CSS
css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_search_css = """
/* --- 3D Premium Search Bar --- */
.global-search {
  flex: 1;
  max-width: 400px;
  margin: 0 var(--space-4);
}
.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.search-prefix-icon {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  width: 18px;
  height: 18px;
  pointer-events: none;
}
.search-input-wrapper input {
  width: 100%;
  padding: 10px 40px 10px 38px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  box-shadow: 
    inset 0 2px 4px rgba(15, 23, 42, 0.04), 
    0 2px 5px rgba(15, 23, 42, 0.04),
    0 1px 1px rgba(255, 255, 255, 1) inset;
  color: var(--text-main);
  font-size: 0.95rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.search-input-wrapper input::placeholder {
  color: #94a3b8;
}
.search-input-wrapper input:hover {
  box-shadow: 
    inset 0 2px 4px rgba(15, 23, 42, 0.04), 
    0 4px 8px rgba(15, 23, 42, 0.06),
    0 1px 1px rgba(255, 255, 255, 1) inset;
  transform: translateY(-1px);
}
.search-input-wrapper input:focus {
  outline: none;
  border-color: var(--primary-blue);
  background: #ffffff;
  box-shadow: 
    inset 0 1px 2px rgba(15, 23, 42, 0.02),
    0 0 0 3px rgba(37, 99, 235, 0.2), 
    0 8px 16px rgba(37, 99, 235, 0.1);
  transform: translateY(-1px);
}
.search-kbd-shortcut {
  position: absolute;
  right: 8px;
  display: flex;
  gap: 4px;
  pointer-events: none;
}
.search-kbd-shortcut kbd {
  background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
  border: 1px solid #cbd5e1;
  border-bottom-width: 2px;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 0.7rem;
  font-family: inherit;
  font-weight: 600;
  color: var(--text-muted);
  box-shadow: 0 1px 1px rgba(0,0,0,0.05);
}
"""

if "3D Premium Search Bar" not in css:
    css += "\n" + new_search_css
    
    # We should also remove the old `.global-search input` override if it conflicts
    css = css.replace('.global-search input {\n  width: 250px;\n}', '')

    with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(css)
print("Updated CSS for 3D search bar")
