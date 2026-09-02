import os
import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add sender name to form
old_receiver_html = """        <div>
          <label style="display:block; font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:4px;">Receiver Name</label>
          <input type="text" id="ns-receiver" required placeholder="e.g. Acme Corp" style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:8px; font-family:inherit; outline:none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#cbd5e1'">
        </div>"""
        
new_receiver_html = """        <div style="display:flex; gap:16px;">
          <div style="flex:1;">
            <label style="display:block; font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:4px;">Sender Name</label>
            <input type="text" id="ns-sender" required placeholder="e.g. Your Company" style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:8px; font-family:inherit; outline:none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#cbd5e1'">
          </div>
          <div style="flex:1;">
            <label style="display:block; font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:4px;">Receiver Name</label>
            <input type="text" id="ns-receiver" required placeholder="e.g. Acme Corp" style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:8px; font-family:inherit; outline:none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#cbd5e1'">
          </div>
        </div>"""

html = html.replace(old_receiver_html, new_receiver_html)
with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("const receiver = document.getElementById('ns-receiver').value;", "const receiver = document.getElementById('ns-receiver').value;\n      const sender = document.getElementById('ns-sender').value;")
js = js.replace("const payload = { origin, destination, receiver_name: receiver };", "const payload = { origin, destination, receiver_name: receiver, sender_name: sender };")

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print("Updated form with Sender Name")
