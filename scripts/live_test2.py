import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Testing application at", BASE_URL)
    
    # 2. Guest Login
    print("\n[TEST] Guest Login")
    r = httpx.post(f"{BASE_URL}/api/v1/auth/guest")
    if r.status_code != 200:
        print("Guest login failed")
        return
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. View Shipments as Guest (GET /api/v1/shipments)
    print("\n[TEST] View Shipments as Guest")
    r = httpx.get(f"{BASE_URL}/api/v1/shipments", headers=headers)
    print(f"Status: {r.status_code}")
    items = r.json().get("items", [])
    print(f"Guest Shipments found: {len(items)}")
    
    # Let's try to get shipment_id = 1 (likely Demo, or Northstar).
    # Since we seeded Northstar first in seed_ai_data.py, shipment_id=1 is Northstar.
    # Demo shipment is usually higher ID.
    print("\n[TEST] Security - Guest Accessing Unauthorized Shipment ID 1")
    r_auth_deny = httpx.get(f"{BASE_URL}/api/v1/shipments/1", headers=headers)
    print(f"Status for ID 1: {r_auth_deny.status_code}")
    print("Response for ID 1:", r_auth_deny.text)

if __name__ == "__main__":
    run_tests()
