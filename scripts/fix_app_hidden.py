import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace p.hidden logic with classList logic
old_logic = "pages.forEach(p => p.hidden = p.id !== targetPageId);"
new_logic = """pages.forEach(p => {
        if (p.id === targetPageId) {
          p.classList.remove('hidden');
          p.removeAttribute('hidden');
        } else {
          p.classList.add('hidden');
          p.setAttribute('hidden', '');
        }
      });"""

js = js.replace(old_logic, new_logic)

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated app.js for hidden class")
