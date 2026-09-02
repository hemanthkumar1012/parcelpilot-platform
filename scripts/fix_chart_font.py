import os
import re

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Add Chart default font family
if "Chart.defaults.font.family" not in js:
    # Insert right after `function renderCharts(total, inTransit, delivered, alerts) {`
    old_func = "function renderCharts(total, inTransit, delivered, alerts) {"
    new_func = "function renderCharts(total, inTransit, delivered, alerts) {\n  if (window.Chart) Chart.defaults.font.family = \"'Inter', system-ui, -apple-system, sans-serif\";\n"
    js = js.replace(old_func, new_func)

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js with Chart fonts")
