import os
import re

html_path = 'frontend/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the toolbar in shipments page
old_toolbar_regex = r'<div class="toolbar">.*?</div>\s*<div class="panel data-table">'
new_toolbar = """<div class="toolbar" style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:16px; margin-bottom:24px;">

        <div class="search-input-wrapper" style="max-width: 400px; flex: 1;">
          <i data-lucide="search" class="search-prefix-icon"></i>
          <input
            type="text"
            id="shipment-search-input"
            placeholder="Search by tracking ID, receiver, origin..." />
        </div>

        <div class="toolbar-actions" style="display:flex; gap:12px;">
          <button id="shipments-refresh-btn" class="btn btn-secondary" style="background:#ffffff; border:1px solid #e2e8f0; color:#475569; border-radius:8px; font-weight:600; padding:8px 16px; box-shadow:0 1px 2px rgba(0,0,0,0.05); display:flex; align-items:center; gap:8px; cursor:pointer;">
            <i data-lucide="refresh-cw" width="16" height="16"></i> Refresh
          </button>

          <button id="new-shipment-btn" class="btn btn-primary" style="background:#2563eb; color:white; border:none; border-radius:8px; font-weight:600; padding:8px 16px; box-shadow:0 4px 6px rgba(37,99,235,0.2); display:flex; align-items:center; gap:8px; cursor:pointer;">
            <i data-lucide="plus" width="16" height="16"></i> New shipment
          </button>
        </div>

      </div>

      <div class="panel data-table">"""

html = re.sub(old_toolbar_regex, new_toolbar, html, flags=re.DOTALL)

# Insert the modal just before </body>
modal_html = """
  <!-- New Shipment Modal -->
  <div id="new-shipment-modal" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15,23,42,0.5); z-index:9999; display:flex; align-items:center; justify-content:center; backdrop-filter:blur(4px);">
    <div class="modal-content" style="background:white; border-radius:12px; padding:24px; width:90%; max-width:450px; box-shadow:0 20px 25px -5px rgba(0,0,0,0.1);">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <h2 style="margin:0; font-size:1.25rem; font-weight:700; color:#0f172a;">Create New Shipment</h2>
        <button id="close-modal-btn" style="background:none; border:none; color:#64748b; cursor:pointer; padding:4px;"><i data-lucide="x"></i></button>
      </div>
      <form id="new-shipment-form" style="display:flex; flex-direction:column; gap:16px;">
        <div style="display:flex; gap:16px;">
          <div style="flex:1;">
            <label style="display:block; font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:4px;">Origin</label>
            <input type="text" id="ns-origin" required placeholder="e.g. New York, NY" style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:8px; font-family:inherit; outline:none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#cbd5e1'">
          </div>
          <div style="flex:1;">
            <label style="display:block; font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:4px;">Destination</label>
            <input type="text" id="ns-destination" required placeholder="e.g. London, UK" style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:8px; font-family:inherit; outline:none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#cbd5e1'">
          </div>
        </div>
        <div>
          <label style="display:block; font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:4px;">Receiver Name</label>
          <input type="text" id="ns-receiver" required placeholder="e.g. Acme Corp" style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:8px; font-family:inherit; outline:none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#cbd5e1'">
        </div>
        <button type="submit" id="ns-submit-btn" style="background:#2563eb; color:white; border:none; border-radius:8px; font-weight:600; padding:12px; margin-top:8px; cursor:pointer; font-family:inherit; transition:opacity 0.2s;">Create Shipment</button>
      </form>
    </div>
  </div>
</body>
"""

html = html.replace("</body>", modal_html)

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print("Updated index.html with modal and fixed toolbar")


# Update app.js
js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

new_js = """
  // SHIPMENTS PAGE LOGIC
  const searchInput = document.getElementById('shipment-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase();
      const rows = document.querySelectorAll('#shipments-table-body tr');
      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }

  const refreshBtn = document.getElementById('shipments-refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', async () => {
      const icon = refreshBtn.querySelector('svg');
      if (icon) icon.style.transform = 'rotate(180deg)';
      if (icon) icon.style.transition = 'transform 0.3s ease';
      await fetchShipmentsPage();
      setTimeout(() => { if(icon) icon.style.transform = 'rotate(0deg)'; }, 300);
    });
  }

  const newShipmentBtn = document.getElementById('new-shipment-btn');
  const modal = document.getElementById('new-shipment-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const nsForm = document.getElementById('new-shipment-form');

  if (newShipmentBtn && modal) {
    newShipmentBtn.addEventListener('click', () => {
      modal.classList.remove('hidden');
    });
  }
  if (closeModalBtn && modal) {
    closeModalBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
    });
  }
  if (nsForm) {
    nsForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const origin = document.getElementById('ns-origin').value;
      const destination = document.getElementById('ns-destination').value;
      const receiver = document.getElementById('ns-receiver').value;
      
      const token = localStorage.getItem('parcelpilot_token');
      const submitBtn = document.getElementById('ns-submit-btn');
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.7';
      submitBtn.textContent = 'Creating...';

      try {
        const payload = { origin, destination, receiver_name: receiver };
        const res = await fetch('/api/v1/shipments', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify(payload)
        });
        
        if (res.ok) {
          modal.classList.add('hidden');
          nsForm.reset();
          await fetchShipmentsPage();
          if (typeof fetchDashboardData === 'function') fetchDashboardData(); // Update dashboard too
        } else {
          alert('Failed to create shipment. Please try again.');
        }
      } catch (err) {
        console.error(err);
        alert('Connection error.');
      } finally {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.textContent = 'Create Shipment';
      }
    });
  }
"""

if "SHIPMENTS PAGE LOGIC" not in js:
    # insert before `// AI CHAT INTEGRATION` or at the end
    js = js.replace('const logoutBtn = document.getElementById(\'logout-btn\');', new_js + '\n  const logoutBtn = document.getElementById(\'logout-btn\');')
    with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)
print("Updated app.js with functionality")
