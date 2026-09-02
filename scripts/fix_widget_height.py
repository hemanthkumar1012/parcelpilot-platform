import os
import re

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

old_css = """@media (max-width: 480px) {
  .ai-widget {
    bottom: 0; right: 0; left: 0;
    width: 100%; 
    height: 85vh;
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
    border: none;
    border-top: 1px solid var(--border-light);
    box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
  }
}"""

new_css = """@media (max-width: 480px) {
  .ai-widget {
    top: 0; bottom: 0; right: 0; left: 0;
    width: 100%; 
    height: 100vh;
    border-radius: 0;
    border: none;
    box-shadow: none;
  }
}"""

css = css.replace(old_css, new_css)
with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print("Updated style.css for 100vh widget")
