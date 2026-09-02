css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  /* White & Blue Theme */
  --bg-app: #f4f7fb;
  --bg-surface: #ffffff;
  
  --primary-blue: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-light: #eff6ff;
  --primary-border: #bfdbfe;
  
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  
  --border-light: #e2e8f0;

  /* Status Colors */
  --status-ok: #10b981;
  --status-ok-bg: #d1fae5;
  --status-warning: #f59e0b;
  --status-warning-bg: #fef3c7;
  --status-error: #ef4444;
  --status-error-bg: #fee2e2;
  --status-info: #3b82f6;
  --status-info-bg: #dbeafe;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 32px;
  --space-6: 48px;
  
  /* Radius & Shadows */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

* { box-sizing: border-box; }
body, html {
  margin: 0; padding: 0;
  font-family: 'Inter', system-ui, sans-serif;
  background-color: var(--bg-app);
  color: var(--text-main);
  height: 100%;
}

.hidden { display: none !important; }

/* Typography */
h1, h2, h3, h4, h5, h6 { margin: 0; color: var(--text-main); font-weight: 600; }
p { margin: 0; color: var(--text-muted); }
a { color: var(--primary-blue); text-decoration: none; }
ul, li { list-style: none; margin: 0; padding: 0; }

/* -------------------------------------------------------------
   LAYOUT
------------------------------------------------------------- */
.app-screen {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.page {
  flex: 1;
  padding: var(--space-4);
  overflow-y: auto;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background-color: var(--bg-surface);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  z-index: 50;
}
.sidebar-top { padding: var(--space-4) var(--space-4) var(--space-2); }
.brand-mark-sidebar {
  display: flex; align-items: center; gap: var(--space-2);
  font-size: 20px; font-weight: 800; color: var(--primary-blue);
  margin-bottom: var(--space-4);
}
.sidebar-nav { flex: 1; overflow-y: auto; padding: 0 var(--space-2); }
.nav-item {
  display: flex; align-items: center; gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  margin-bottom: var(--space-1);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  font-weight: 500;
  cursor: pointer;
}
.nav-item:hover, .nav-item[aria-current="page"] {
  background-color: var(--primary-light);
  color: var(--primary-blue);
}
.nav-badge {
  background-color: var(--primary-blue);
  color: white; padding: 2px 6px; border-radius: 999px;
  font-size: 12px; margin-left: auto;
}
.sidebar-bottom { padding: var(--space-4); border-top: 1px solid var(--border-light); }
.sidebar-user { display: flex; align-items: center; gap: var(--space-2); }
.user-avatar { width: 40px; height: 40px; border-radius: 50%; background-color: var(--primary-blue); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; }
.user-name { font-size: 14px; font-weight: 600; }
.user-email, .user-meta { font-size: 12px; color: var(--text-muted); }

/* Topbar */
.topbar {
  height: 64px;
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-light);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 var(--space-4);
}
.topbar-titles h2 { font-size: 18px; }
.topbar-actions { display: flex; align-items: center; gap: var(--space-3); }

/* -------------------------------------------------------------
   DASHBOARD GRIDS & CARDS
------------------------------------------------------------- */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}
.dashboard-grid-lower {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.stat-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  box-shadow: var(--shadow-sm);
  display: flex; flex-direction: column;
}
.stat-label { font-size: 14px; color: var(--text-muted); margin-bottom: var(--space-2); font-weight: 500;}
.stat-value { font-size: 32px; font-weight: 700; color: var(--text-main); margin-bottom: var(--space-1); }
.stat-foot { font-size: 12px; color: var(--text-light); }

.panel {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  display: flex; flex-direction: column;
  overflow: hidden;
}
.panel-header {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-light);
  display: flex; align-items: center; justify-content: space-between;
}
.panel-header h3 { font-size: 16px; }

/* Dashboard lists */
.panel-recent {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--border-light);
  display: flex; align-items: center; justify-content: space-between;
}
.panel-recent:last-child { border-bottom: none; }
.panel-recent strong { font-size: 14px; display: block; margin-bottom: 2px;}

.status-dot {
  font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 999px;
  background-color: var(--border-light); color: var(--text-muted);
}
.status-dot-ok { background-color: var(--status-ok-bg); color: var(--status-ok); }
.status-dot-warning, .status-dot-pending { background-color: var(--status-warning-bg); color: var(--status-warning); }
.status-dot-error { background-color: var(--status-error-bg); color: var(--status-error); }
.status-dot-info { background-color: var(--status-info-bg); color: var(--status-info); }


/* -------------------------------------------------------------
   LOGIN SCREEN
------------------------------------------------------------- */
.login-screen {
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100vh;
  background-color: var(--bg-app);
}
.login-brand {
  background-color: var(--primary-blue);
  color: white;
  padding: var(--space-6);
  display: flex; flex-direction: column; justify-content: center;
}
.login-brand-inner { max-width: 400px; margin: 0 auto; }
.brand-title { font-size: 32px; font-weight: 800; margin-bottom: var(--space-2); }
.brand-subtitle { font-size: 18px; font-weight: 500; opacity: 0.9; margin-bottom: var(--space-6); }
.login-features { margin-top: var(--space-6); }
.login-features li { display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-3); font-size: 15px;}
.feature-dot { width: 8px; height: 8px; background-color: white; border-radius: 50%; opacity: 0.8; }
.login-route-signature { margin-top: var(--space-6); opacity: 0.5; max-width: 300px; }

.login-form-panel {
  display: flex; align-items: center; justify-content: center;
  padding: var(--space-6);
  background-color: var(--bg-surface);
}
.login-form-card {
  width: 100%; max-width: 400px;
}
.login-form-header { text-align: center; margin-bottom: var(--space-5); }
.login-form-header h2 { font-size: 28px; margin-bottom: var(--space-2); }

.guest-demo-banner {
  background-color: var(--primary-light);
  border: 1px solid var(--primary-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  display: flex; align-items: flex-start; gap: var(--space-3);
  margin-bottom: var(--space-4);
}
.guest-demo-banner-icon { font-size: 20px; }
.guest-demo-banner-title { font-weight: 700; color: var(--primary-blue); margin-bottom: 4px; font-size: 14px;}
.guest-mode-btn { width: 100%; margin-top: var(--space-2); }
.login-divider { text-align: center; margin: var(--space-4) 0; color: var(--text-light); font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }

/* -------------------------------------------------------------
   FORMS & BUTTONS
------------------------------------------------------------- */
.form-field { margin-bottom: var(--space-3); }
.form-field label { display: block; font-size: 14px; font-weight: 500; margin-bottom: var(--space-1); }
.form-field input {
  width: 100%; padding: 10px 14px; border: 1px solid var(--border-light);
  border-radius: var(--radius-md); font-family: inherit; font-size: 14px;
}
.form-field input:focus { outline: none; border-color: var(--primary-blue); box-shadow: 0 0 0 3px var(--primary-light); }

.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 10px 16px; border-radius: var(--radius-md); font-weight: 500;
  cursor: pointer; border: none; font-size: 14px; font-family: inherit;
  transition: all 0.2s;
}
.btn-primary { background-color: var(--primary-blue); color: white; }
.btn-secondary { background-color: white; border: 1px solid var(--border-light); color: var(--text-main); }
.btn-block { width: 100%; }

/* -------------------------------------------------------------
   AI WIDGET
------------------------------------------------------------- */
.ai-floating-btn {
  position: fixed; bottom: var(--space-4); right: var(--space-4);
  background-color: var(--primary-blue); color: white;
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  box-shadow: var(--shadow-lg); cursor: pointer; border: none; z-index: 100;
}
.ai-widget {
  position: fixed; bottom: 90px; right: var(--space-4);
  width: 350px; height: 500px;
  background-color: var(--bg-surface); border: 1px solid var(--border-light);
  border-radius: var(--radius-xl); box-shadow: var(--shadow-xl);
  display: flex; flex-direction: column; overflow: hidden; z-index: 100;
}
.ai-header {
  background-color: var(--primary-blue); color: white; padding: var(--space-3);
  display: flex; justify-content: space-between; align-items: center;
}
.ai-close-btn { background: none; border: none; color: white; cursor: pointer; }
.ai-messages { flex: 1; overflow-y: auto; padding: var(--space-3); display: flex; flex-direction: column; gap: var(--space-2); background: var(--bg-app); }
.ai-message { max-width: 80%; padding: 10px 14px; border-radius: var(--radius-md); font-size: 14px; }
.ai-message-assistant { background-color: white; border: 1px solid var(--border-light); align-self: flex-start; border-bottom-left-radius: 0; }
.ai-message-user { background-color: var(--primary-blue); color: white; align-self: flex-end; border-bottom-right-radius: 0; }
.ai-input-area { padding: var(--space-3); border-top: 1px solid var(--border-light); display: flex; gap: var(--space-2); }
.ai-input-area input { flex: 1; padding: 10px; border: 1px solid var(--border-light); border-radius: var(--radius-md); outline: none; }

/* -------------------------------------------------------------
   MEDIA QUERIES
------------------------------------------------------------- */
@media (max-width: 1024px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .login-screen { grid-template-columns: 1fr; }
  .login-brand { display: none; }
  .sidebar { display: none; }
  .stats-grid { grid-template-columns: 1fr; }
  .dashboard-grid-lower { grid-template-columns: 1fr; }
}

/* -------------------------------------------------------------
   MOTION (STAGE 2)
------------------------------------------------------------- */
@keyframes skeletonLoading {
  0% { background-color: var(--border-light); }
  50% { background-color: var(--bg-app); }
  100% { background-color: var(--border-light); }
}

.skeleton, .skeleton * {
  animation: skeletonLoading 1.5s infinite ease-in-out !important;
  color: transparent !important;
  border-color: transparent !important;
  pointer-events: none;
}

.animate-on-scroll {
  opacity: 0;
  transform: translateY(15px);
  transition: opacity 0.4s ease-out, transform 0.4s ease-out;
}
.animate-on-scroll.is-visible { opacity: 1; transform: translateY(0); }

@keyframes pageLoad {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.page-enter { animation: pageLoad 0.4s ease-out forwards; }

.btn:hover, .stat-card:hover, .panel-recent:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .animate-on-scroll { opacity: 1; transform: none; }
}
"""

with open('frontend/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
