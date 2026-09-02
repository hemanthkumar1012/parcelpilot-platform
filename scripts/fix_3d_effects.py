import os

css_path = 'frontend/style.css'
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("""
/* --- 3D and Dynamic Effects --- */
#shipment-search-input:focus {
  outline: none;
  border-color: #3b82f6 !important;
  box-shadow: inset 0 1px 2px rgba(15,23,42,0.02), 0 0 0 3px rgba(59,130,246,0.2), 0 4px 12px rgba(59,130,246,0.1) !important;
  transform: translateY(-1px);
}
#shipment-search-input:hover {
  box-shadow: inset 0 2px 4px rgba(15,23,42,0.02), 0 4px 8px rgba(15,23,42,0.04) !important;
}

#shipments-refresh-btn:hover {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 2px 4px rgba(15,23,42,0.08) !important;
  transform: translateY(-1px);
}
#shipments-refresh-btn:active {
  background: #f1f5f9 !important;
  box-shadow: inset 0 2px 4px rgba(15,23,42,0.05) !important;
  transform: translateY(0);
}

#new-shipment-btn:hover {
  background: linear-gradient(180deg, #60a5fa 0%, #3b82f6 100%) !important;
  border-color: #2563eb !important;
  box-shadow: 0 6px 12px rgba(37,99,235,0.25), inset 0 1px 0 rgba(255,255,255,0.3) !important;
  transform: translateY(-1px);
}
#new-shipment-btn:active {
  background: #2563eb !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
  transform: translateY(0);
}
""")
print("Added 3D dynamic hover states to Shipments toolbar")
