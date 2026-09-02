import re

html_content = open('frontend/index.html', encoding='utf-8', errors='ignore').read()
html_classes = set()
for match in re.findall(r'class="([^"]+)"', html_content):
    html_classes.update(match.split())

css_content = open('frontend/style.css', encoding='utf-8', errors='ignore').read()
css_classes = set(re.findall(r'\.([a-zA-Z0-9_-]+)[,\s\{:>]', css_content))

# Exclude generic animation classes or classes injected by JS dynamically
html_only = html_classes - css_classes
css_only = css_classes - html_classes

print("In HTML but not CSS:", sorted(list(html_only)))
print("In CSS but not HTML:", sorted(list(css_only)))
