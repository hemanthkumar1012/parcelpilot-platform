def auth_headers(client, email="chat@example.com"):
    register = client.post(
        "/api/auth/register",
        json={"name": "Chat User", "email": email, "password": "password"},
    )
    assert register.status_code == 201
    login = client.post(
        "/api/auth/login",
        data={"username": email, "password": "password"},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_chat_demo_mode_and_history(client):
    headers = auth_headers(client)

    response = client.post(
        "/api/v1/chat",
        json={"message": "Where is my shipment?"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] > 0
    assert "response" in data

    history = client.get(
        f"/api/v1/chat/{data['conversation_id']}",
        headers=headers,
    )
    assert history.status_code == 200
    messages = history.json()
    assert [m["role"] for m in messages] == ["user", "assistant"]


def test_chat_rejects_empty_message(client):
    headers = auth_headers(client, "chat-empty@example.com")
    response = client.post(
        "/api/v1/chat",
        json={"message": "   "},
        headers=headers,
    )
    assert response.status_code == 400


def test_chat_conversation_isolation(client):
    h1 = auth_headers(client, "chat-one@example.com")
    h2 = auth_headers(client, "chat-two@example.com")

    created = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
        headers=h1,
    )
    conversation_id = created.json()["conversation_id"]

    forbidden = client.get(
        f"/api/v1/chat/{conversation_id}",
        headers=h2,
    )
    assert forbidden.status_code == 404


def test_chat_requires_authentication(client):
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"},
    )
    assert response.status_code == 401
