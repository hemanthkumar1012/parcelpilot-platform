import os

css_path = 'frontend/style.css'
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("\n#logout-btn:hover { background: #f1f5f9 !important; border-color: #cbd5e1 !important; color: #0f172a !important; }\n")
print("Added logout hover")
