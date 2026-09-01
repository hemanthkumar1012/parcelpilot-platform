import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.db.models import User, Role, CustomerAccount

client = TestClient(app)

def test_guest_chat_flow():
    # Start guest session
    res_guest = client.post("/api/v1/auth/guest")
    assert res_guest.status_code == 200
    token = res_guest.json()["access_token"]
    
    # Send chat
    res_chat = client.post("/api/v1/chat", json={"message": "Where is shipment PP-DEMO-1001?"}, headers={"Authorization": f"Bearer {token}"})
    assert res_chat.status_code == 200
    data = res_chat.json()
    assert "response" in data
    assert "conversation_id" in data
    
    # Continue conversation
    res_chat2 = client.post("/api/v1/chat", json={
        "message": "Thanks!",
        "conversation_id": data["conversation_id"]
    }, headers={"Authorization": f"Bearer {token}"})
    assert res_chat2.status_code == 200

def test_chat_unauthorized():
    res_chat = client.post("/api/v1/chat", json={"message": "Hello"})
    assert res_chat.status_code == 401
