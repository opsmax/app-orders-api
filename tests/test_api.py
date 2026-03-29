"""Tests for all API endpoints (mock data, no database required)."""


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "orders-api"
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
    assert data["database"] == "using mock data"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "unavailable"


def test_list_orders(client):
    response = client.get("/api/orders")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)
    assert len(orders) == 10
    assert orders[0]["customer"] == "Acme Corp"


def test_get_order(client):
    response = client.get("/api/orders/1")
    assert response.status_code == 200
    order = response.json()
    assert order["id"] == 1
    assert order["customer"] == "Acme Corp"
    assert order["product"] == "Cloud Platform License"


def test_get_order_not_found(client):
    response = client.get("/api/orders/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_orders"] == 10
    assert data["total_revenue"] > 0
    assert data["average_order_value"] > 0
    assert isinstance(data["orders_by_status"], dict)
    assert isinstance(data["top_products"], list)
    assert len(data["top_products"]) > 0


def test_openapi_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
