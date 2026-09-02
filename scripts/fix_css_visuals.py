import os

css_path = 'frontend/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
/* -----------------------------------------
   VISUAL POLISH & HIERARCHY OVERRIDES
   ----------------------------------------- */
/* 1. Stat Cards Typography & Accents */
.stat-card {
  position: relative;
  padding-top: var(--space-5);
  border-top: 4px solid var(--border-light);
}
.stat-card:nth-child(1) { border-top-color: var(--primary-blue); }
.stat-card:nth-child(2) { border-top-color: var(--status-pending); }
.stat-card:nth-child(3) { border-top-color: var(--status-ok); }
.stat-card:nth-child(4) { border-top-color: var(--status-error); }

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.1;
  margin-top: var(--space-2);
  margin-bottom: var(--space-1);
}

.stat-label {
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.stat-foot {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* 2. Panel Header Stacking */
.panel-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-1);
  margin-bottom: var(--space-4);
}
.panel-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}
.panel-header p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.9rem;
}

/* 3. Whitespace / Breathing Room */
.stats-grid {
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}
.dashboard-grid {
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}
.page {
  padding: var(--space-6) var(--space-6) 100px;
}

/* 4. Global Search Input */
.global-search input {
  width: 250px;
}
@media (max-width: 768px) {
  .global-search input { width: 100%; }
}

/* 5. Lucide Icon styling */
[data-lucide] {
  vertical-align: middle;
}
"""

if "VISUAL POLISH & HIERARCHY OVERRIDES" not in css:
    css += "\n" + new_css
    with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(css)

print("Updated style.css")
