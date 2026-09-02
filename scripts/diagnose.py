import os
import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("--- DIAGNOSTICS ---")
for i, line in enumerate(lines):
    if '`' in line:
        print(f"Line {i+1} (Backtick): {line.strip()}")
    # Look for broken tags specifically around guest-demo-banner or missing '<'
    if 'guest-demo-banner' in line and not line.strip().startswith('<') and 'class=' in line:
        print(f"Line {i+1} (Broken tag suspect): {line.strip()}")

# Also check for null bytes in app.js
app_js_path = 'frontend/app.js'
with open(app_js_path, 'rb') as f:
    data = f.read()
    if b'\x00' in data:
        print(f"app.js contains null bytes!")
