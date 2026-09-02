import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the IDs used to initialize Chart.js
js = js.replace("const distCanvas = document.getElementById('status-distribution');", "const distCanvas = document.getElementById('chart-distribution');")
js = js.replace("const actCanvas = document.getElementById('activity-chart');", "const actCanvas = document.getElementById('chart-activity');")

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated chart canvas IDs in app.js")
