from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_auth_and_tenant_flow(client: TestClient):
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "owner@example.com", "full_name": "Owner", "password": "strongpass123"},
    )
    assert register.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        data={"username": "owner@example.com", "password": "strongpass123"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    tenant = client.post(
        "/api/v1/tenants",
        json={"name": "Acme", "slug": "acme"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert tenant.status_code == 201
    tenant_id = tenant.json()["id"]

    bot = client.post(
        "/api/v1/bots",
        json={
            "tenant_id": tenant_id,
            "name": "Acme Support Bot",
            "telegram_bot_token": "123:token",
            "webhook_secret": "secret-123",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert bot.status_code == 201

    webhook = client.post(
        "/api/v1/telegram/123:token/webhook",
        json={"update_id": 101, "message": {"text": "hello"}},
        headers={"X-Telegram-Bot-Api-Secret-Token": "secret-123"},
    )
    assert webhook.status_code == 200
    assert webhook.json()["received_update_id"] == 101