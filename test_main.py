from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Expense Tracker API"}


def test_create_expense():
    response = client.post(
        "/expenses",
        json={
            "description": "Test expense",
            "amount": 10.5,
            "category": "Test",
            "spent_on": "2026-10-15"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test expense"
    assert "id" in data


def test_negative_amount_is_rejected():
    response = client.post(
        "/expenses",
        json={
            "description": "Negative expense",
            "amount": -10,
            "category": "Test",
            "spent_on": "2026-10-19",
        },
    )
    assert response.status_code == 422


def test_get_missing_expense_returns_404():
    response = client.get("/expenses/999999")
    assert response.status_code == 404
