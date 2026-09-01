import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Testing application at", BASE_URL)
    
    # 1. Health and Frontend
    try:
        r = httpx.get(f"{BASE_URL}/health")
        print(f"[HEALTH] {r.status_code}")
        
        r = httpx.get(f"{BASE_URL}/")
        print(f"[FRONTEND HTML] {r.status_code}, contains 'ParcelPilot': {'ParcelPilot' in r.text}")
    except Exception as e:
        print("Failed to reach server:", e)
        return

    # 2. Guest Login
    print("\n[TEST] Guest Login")
    r = httpx.post(f"{BASE_URL}/api/v1/auth/guest")
    print(f"Status: {r.status_code}")
    if r.status_code != 200:
        print("Guest login failed", r.text)
        return
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. View Shipments as Guest
    print("\n[TEST] View Shipments")
    r = httpx.get(f"{BASE_URL}/api/v1/shipments", headers=headers)
    print(f"Status: {r.status_code}")
    shipments = r.json().get("items", [])
    print(f"Guest Shipments found: {len(shipments)}")
    if shipments:
        print("First shipment:", shipments[0].get("tracking_id"))

    # 4. Chat with AI Agent
    print("\n[TEST] AI Chat - Multi-turn Conversation")
    chat_payload = {"message": "Where is my shipment PP-DEMO-1001?"}
    r = httpx.post(f"{BASE_URL}/api/v1/chat", json=chat_payload, headers=headers)
    print(f"Chat Response Status: {r.status_code}")
    chat_data = r.json()
    print("AI Response:", chat_data.get("response"))
    
    conv_id = chat_data.get("conversation_id")
    print("\n[TEST] AI Chat - Continuing conversation")
    chat_payload_2 = {"message": "Why is it delayed?", "conversation_id": conv_id}
    r2 = httpx.post(f"{BASE_URL}/api/v1/chat", json=chat_payload_2, headers=headers)
    print(f"Chat Response 2 Status: {r2.status_code}")
    print("AI Response 2:", r2.json().get("response"))

    # 5. Security - Try to lookup an arbitrary user's shipment
    print("\n[TEST] Security - Guest Accessing Unauthorized Order")
    # TBD: Need a shipment ID that doesn't belong to the guest. 
    # ORD-1001 was seeded for Northstar in seed_ai_data.py
    # But wait, we'd need to hit a direct endpoint if we want to test direct API.
    # The frontend AI tool lookup_shipment enforces it, but let's test the endpoint directly.
    r3 = httpx.get(f"{BASE_URL}/api/v1/shipments/tracking/ORD-1001", headers=headers)
    print(f"Status for ORD-1001: {r3.status_code}")
    print("Response for ORD-1001:", r3.text)

if __name__ == "__main__":
    # Give server a moment to start
    time.sleep(2)
    run_tests()
