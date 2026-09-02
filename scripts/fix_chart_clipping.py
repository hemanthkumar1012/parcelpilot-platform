import os

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Fix donut chart and other chart containers
new_css = """
#activity-chart, #status-distribution {
  position: relative;
  height: 280px;
  width: 100%;
}
.panel-distribution, .activity-chart-panel {
  height: auto; 
  padding: var(--space-4);
}
"""
css += "\n" + new_css

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)
print("Updated style.css for chart clipping")
