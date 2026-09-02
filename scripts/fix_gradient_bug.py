import os

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the gradient call
old_code = "const gradient = ctxActivity.createLinearGradient(0, 0, 0, 300);"
new_code = "const gradient = ctxActivity.getContext('2d').createLinearGradient(0, 0, 0, 300);"
js = js.replace(old_code, new_code)

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Fixed JS gradient error")
