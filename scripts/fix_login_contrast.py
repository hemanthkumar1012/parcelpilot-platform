import os

css_path = 'frontend/style.css'
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("""
/* --- LOGIN POLISH OVERRIDES --- */

/* Fix text contrast on the blue left panel */
.login-headline {
  color: #ffffff !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 2.5rem;
  line-height: 1.2;
}
.login-copy {
  color: rgba(255, 255, 255, 0.95) !important;
  font-size: 1.1rem;
  line-height: 1.5;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.login-features li {
  color: #ffffff;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* 3D styling for the Login Form Card */
.login-form-panel {
  background-color: #f8fafc;
}
.login-form-card {
  background: #ffffff;
  padding: 40px;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.05), 0 8px 10px -6px rgba(15, 23, 42, 0.01), 0 0 0 1px rgba(15, 23, 42, 0.02);
}
.login-form-header h2 {
  color: #0f172a;
  font-weight: 800;
  letter-spacing: -0.025em;
}
.login-form-header p {
  color: #475569 !important; /* darker gray for better readability */
  font-weight: 500;
}

/* 3D Dynamic Inputs */
.login-form input {
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  border: 1px solid #cbd5e1;
  box-shadow: inset 0 2px 4px rgba(15,23,42,0.02), 0 1px 2px rgba(15,23,42,0.02);
  border-radius: 10px;
  padding: 12px 16px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', system-ui, sans-serif;
  color: #0f172a;
  font-size: 0.95rem;
}
.login-form input:focus {
  outline: none;
  border-color: #3b82f6 !important;
  background: #ffffff;
  box-shadow: inset 0 1px 2px rgba(15,23,42,0.02), 0 0 0 3px rgba(59,130,246,0.2), 0 4px 12px rgba(59,130,246,0.1) !important;
  transform: translateY(-1px);
}

/* 3D Dynamic Buttons */
.login-form .btn-primary {
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important;
  border: 1px solid #1d4ed8 !important;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(37,99,235,0.2), inset 0 1px 0 rgba(255,255,255,0.2) !important;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
  font-weight: 600;
  letter-spacing: 0.025em;
  padding: 12px;
  transition: all 0.2s;
}
.login-form .btn-primary:hover {
  background: linear-gradient(180deg, #60a5fa 0%, #3b82f6 100%) !important;
  box-shadow: 0 6px 12px rgba(37,99,235,0.25), inset 0 1px 0 rgba(255,255,255,0.3) !important;
  transform: translateY(-1px);
}
.login-form .btn-primary:active {
  background: #2563eb !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
  transform: translateY(0);
}

.login-form .btn-secondary {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
  border: 1px solid #e2e8f0 !important;
  color: #475569 !important;
  border-radius: 10px;
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(15,23,42,0.05) !important;
  padding: 12px;
  transition: all 0.2s;
}
.login-form .btn-secondary:hover {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 2px 4px rgba(15,23,42,0.08) !important;
  transform: translateY(-1px);
}
.login-form .btn-secondary:active {
  background: #f1f5f9 !important;
  box-shadow: inset 0 2px 4px rgba(15,23,42,0.05) !important;
  transform: translateY(0);
}
""")
print("Added login UI polish and contrast fixes")
