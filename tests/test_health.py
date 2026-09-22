# Runtime verification marker: exercise the complete automated suite in CI.

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "ParcelPilot API is running healthy",
    }


def test_readiness_check(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Database is ready",
    }


def test_request_id_is_returned(client):
    response = client.get("/health", headers={"X-Request-ID": "test-request-123"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"
