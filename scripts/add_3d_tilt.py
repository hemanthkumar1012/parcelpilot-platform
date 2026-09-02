import os

# Update style.css
css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
/* 3D Tilt and Layered Shadows */
.stat-card, .panel, .login-form-card {
  box-shadow:
    0 1px 2px rgba(15, 23, 42, 0.04),
    0 2px 6px rgba(15, 23, 42, 0.04);
  transition: transform 150ms ease, box-shadow 150ms ease;
  will-change: transform, box-shadow;
}

.stat-card:hover, .panel:hover, .login-form-card:hover {
  box-shadow:
    0 4px 8px rgba(15, 23, 42, 0.06),
    0 12px 24px rgba(37, 99, 235, 0.08);
}
"""

if "3D Tilt and Layered Shadows" not in css:
    css += "\n" + new_css
    with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(css)

# Update app.js
js_path = 'frontend/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

tilt_js = """
// --- 6. TILT EFFECT ---
function initTiltEffect(selector) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  document.querySelectorAll(selector).forEach(card => {
    card.style.transformStyle = 'preserve-3d';
    card.style.transition = 'transform 150ms ease, box-shadow 150ms ease';

    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Keep the tilt subtle: max ~5 degrees
      const rotateX = ((y - centerY) / centerY) * -5;
      const rotateY = ((x - centerX) / centerX) * 5;

      card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    });
  });
}
"""

if "initTiltEffect" not in js:
    # Insert function definition
    js += "\n" + tilt_js
    
    # Insert initialization into DOMContentLoaded
    init_call = "\n  initTiltEffect('.stat-card, .panel, .login-form-card');\n"
    # Find end of DOMContentLoaded
    # Since it might be tricky, just append it before the very last `});` or insert after `renderAuthState();`
    js = js.replace("renderAuthState();", "renderAuthState();" + init_call, 1)

    with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)

print("Updated app.js and style.css for 3D tilt")
