with open('frontend/style.css', 'a', encoding='utf-8') as f:
    f.write("""

/* ==========================================================================
   MODERN SAAS DASHBOARD OVERRIDES (Step 3: Redesign)
   Targeting REAL HTML classes
   ========================================================================== */

:root {
  /* White & Blue Theme */
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --bg-tertiary: #f1f5f9;
  
  --primary-blue: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-light: #eff6ff;
  --primary-border: #bfdbfe;
  
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  
  --border-light: #e2e8f0;

  /* Spacing Scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 32px;
  
  /* Layout & Shadows */
  --radius-md: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Global Typography & Background */
body, html {
  font-family: 'Inter', system-ui, sans-serif;
  background-color: var(--bg-primary) !important;
  color: var(--text-main) !important;
}

/* Sidebar */
.sidebar {
  background-color: var(--bg-secondary) !important;
  border-right: 1px solid var(--border-light) !important;
}
.brand-text { color: var(--primary-blue) !important; }
.nav-item { color: var(--text-muted) !important; transition: all 150ms ease; }
.nav-item:hover, .nav-item[aria-current="page"] {
  background-color: var(--primary-light) !important;
  color: var(--primary-blue) !important;
}

/* Topbar */
.topbar {
  background-color: var(--bg-secondary) !important;
  border-bottom: 1px solid var(--border-light) !important;
  box-shadow: var(--shadow-sm);
}

/* Cards & Panels (Dashboard elements) */
.stat-card, .panel, .login-form-card {
  background-color: var(--bg-secondary) !important;
  border: 1px solid var(--border-light) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-sm) !important;
  transition: transform 250ms ease, box-shadow 250ms ease;
}
.stat-card:hover, .panel:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md) !important;
}
.stat-value { color: var(--primary-blue) !important; }

/* Buttons */
.btn-primary, .btn-block {
  background-color: var(--primary-blue) !important;
  color: #ffffff !important;
  border-radius: var(--radius-md) !important;
  border: none !important;
  transition: background-color 150ms ease, transform 150ms ease;
}
.btn-primary:hover, .btn-block:hover {
  background-color: var(--primary-hover) !important;
  transform: translateY(-1px);
}
.btn-secondary, .guest-mode-btn {
  background-color: var(--bg-secondary) !important;
  color: var(--text-main) !important;
  border: 1px solid var(--border-light) !important;
}
.btn-secondary:hover, .guest-mode-btn:hover {
  background-color: var(--bg-tertiary) !important;
}

/* Shipment List Items */
.panel-recent {
  background-color: var(--bg-secondary) !important;
  border: 1px solid var(--border-light) !important;
  border-radius: var(--radius-md) !important;
  padding: var(--space-3) !important;
  margin-bottom: var(--space-2) !important;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}
.panel-recent:hover {
  border-color: var(--primary-border) !important;
  box-shadow: var(--shadow-sm) !important;
}

/* Forms & Inputs */
.form-field input, .search-input-wrap input {
  border: 1px solid var(--border-light) !important;
  border-radius: var(--radius-md) !important;
  padding: var(--space-2) var(--space-3) !important;
  background-color: var(--bg-secondary) !important;
  transition: box-shadow 150ms ease;
}
.form-field input:focus, .search-input-wrap input:focus {
  outline: none !important;
  box-shadow: 0 0 0 3px var(--primary-light) !important;
  border-color: var(--primary-blue) !important;
}

/* Banners & Extras */
.guest-demo-banner {
  background-color: var(--primary-light) !important;
  border: 1px solid var(--primary-border) !important;
  color: var(--primary-blue) !important;
  border-radius: var(--radius-md) !important;
}
""")
