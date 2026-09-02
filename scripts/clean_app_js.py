import os
import re

js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the duplicate block
bad_block = """
  // Logout Button
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('parcelpilot_token');
      renderAuthState();
    });
  }

  // Sidebar Nav Items (High-end button behavior + Page Switching)
  const navItems = document.querySelectorAll('.nav-item');
  const pages = document.querySelectorAll('.page');
  
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      // Update active state
      navItems.forEach(nav => nav.removeAttribute('aria-current'));
      item.setAttribute('aria-current', 'page');
      
      // Switch page visibility
      const targetPageId = 'page-' + item.dataset.page;
      pages.forEach(p => {
        if (p.id === targetPageId) {
          p.classList.remove('hidden');
          p.removeAttribute('hidden');
        } else {
          p.classList.add('hidden');
          p.setAttribute('hidden', '');
        }
      });
      
      // Trigger page-specific data loading
      if (item.dataset.page === 'shipments') fetchShipmentsPage();
      if (item.dataset.page === 'tracking') { /* tracking is on-demand via form */ }
      if (item.dataset.page === 'drivers') loadDriversPage();
      if (item.dataset.page === 'notifications') fetchNotificationsPage();
    });
  });
"""

# Let's just find the first occurrence of this block and keep it, then remove the rest.
# Or better, just rewrite the DOMContentLoaded completely.
dom_content_loaded_start = js.find("document.addEventListener('DOMContentLoaded', () => {")
js_before = js[:dom_content_loaded_start]
js_after = js[js.find("// --- 5. PAGE-SPECIFIC FETCHING ---"):]

new_dom_content = """document.addEventListener('DOMContentLoaded', () => {
  renderAuthState();

  // Logout Button
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('parcelpilot_token');
      renderAuthState();
    });
  }

  // Sidebar Nav Items
  const navItems = document.querySelectorAll('.nav-item');
  const pages = document.querySelectorAll('.page');
  
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(nav => nav.removeAttribute('aria-current'));
      item.setAttribute('aria-current', 'page');
      
      const targetPageId = 'page-' + item.dataset.page;
      pages.forEach(p => {
        if (p.id === targetPageId) {
          p.classList.remove('hidden');
          p.removeAttribute('hidden');
        } else {
          p.classList.add('hidden');
          p.setAttribute('hidden', '');
        }
      });
      
      if (item.dataset.page === 'shipments') fetchShipmentsPage();
      if (item.dataset.page === 'drivers') loadDriversPage();
      if (item.dataset.page === 'notifications') fetchNotificationsPage();
    });
  });

  // Login Form Submission
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      try {
        const res = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData
        });
        if (!res.ok) throw new Error('Login failed');
        const data = await res.json();
        localStorage.setItem('parcelpilot_token', data.access_token);
        renderAuthState();
      } catch (err) {
        alert('Login failed: Check credentials');
      }
    });
  }

  // Guest Demo Login
  const guestBtnClass = document.querySelector('.guest-mode-btn');
  if (guestBtnClass) {
    guestBtnClass.addEventListener('click', async () => {
      try {
        const res = await fetch('/api/v1/auth/guest', { method: 'POST' });
        if (!res.ok) throw new Error('Guest login failed');
        const data = await res.json();
        localStorage.setItem('parcelpilot_token', data.access_token);
        renderAuthState();
      } catch (err) {
        alert('Demo login failed');
      }
    });
  }

  // AI Widget logic
  const aiFloatingBtn = document.getElementById('ai-floating-btn');
  const aiWidget = document.getElementById('ai-assistant-widget');
  const aiCloseBtn = document.getElementById('ai-close-btn');
  
  if (aiFloatingBtn && aiWidget && aiCloseBtn) {
    aiFloatingBtn.addEventListener('click', () => {
      aiWidget.classList.remove('hidden');
    });
    aiCloseBtn.addEventListener('click', () => {
      aiWidget.classList.add('hidden');
    });
  }

  const aiForm = document.getElementById('ai-form');
  const aiMessages = document.getElementById('ai-messages');
  if (aiForm) {
    aiForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('ai-input');
      const text = input.value.trim();
      if (!text) return;

      const userMsg = document.createElement('div');
      userMsg.className = 'ai-message ai-message-user';
      userMsg.textContent = text;
      aiMessages.appendChild(userMsg);
      input.value = '';
      aiMessages.scrollTop = aiMessages.scrollHeight;

      try {
        const token = localStorage.getItem('parcelpilot_token');
        const res = await fetch('/api/v1/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
          },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        
        const aiMsg = document.createElement('div');
        aiMsg.className = 'ai-message ai-message-assistant';
        aiMsg.textContent = data.response || "Sorry, I couldn't process that.";
        aiMessages.appendChild(aiMsg);
        aiMessages.scrollTop = aiMessages.scrollHeight;
      } catch (err) {
        const aiMsg = document.createElement('div');
        aiMsg.className = 'ai-message ai-message-assistant';
        aiMsg.textContent = "Connection error.";
        aiMessages.appendChild(aiMsg);
        aiMessages.scrollTop = aiMessages.scrollHeight;
      }
    });
  }
});

"""

# Stitch it back together
final_js = js_before + new_dom_content + "\n" + js_after

with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(final_js)
print("app.js cleaned up")
