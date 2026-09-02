import os
import re

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
/* Quick Track Input 3D Polish */
.quick-track-form {
  display: flex;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}
#quick-track-input {
  flex: 1;
  padding: 10px 16px;
  border-radius: 10px;
  border: 1px solid var(--border-light);
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  box-shadow: 
    inset 0 2px 4px rgba(15, 23, 42, 0.04), 
    0 1px 2px rgba(15, 23, 42, 0.02),
    0 1px 1px rgba(255, 255, 255, 1) inset;
  color: var(--text-main);
  font-size: 0.95rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
#quick-track-input:focus {
  outline: none;
  border-color: var(--primary-blue);
  background: #ffffff;
  box-shadow: 
    inset 0 1px 2px rgba(15, 23, 42, 0.02),
    0 0 0 3px rgba(37, 99, 235, 0.2), 
    0 4px 12px rgba(37, 99, 235, 0.1);
}
"""

if "Quick Track Input 3D Polish" not in css:
    css += "\n" + new_css
    with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(css)

print("Quick track polished")
