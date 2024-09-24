import pytest


@pytest.mark.parametrize("route", [
    "/clients",  # Маршрут для получения списка клиентов
    "/clients/1"  # Маршрут для получения списка парковочных логов
])
def test_get_methods_return_200(client, route):
    """Тест для проверки, что все GET-запросы возвращают код 200"""
    response = client.get(route)
    assert response.status_code == 200, f"Failed on {route}"


def test_create_client(client) -> None:
    client_data = {"name": "Никита",
                   "surname": "Нестеренко",
                   "credit_card": "credit_card",
                   "car_number": "car_number"}
    resp = client.post("/clients", json=client_data)

    assert resp.status_code == 201
    assert resp.json == {
        "id": 2,
        "name": "Никита",
        "surname": "Нестеренко",
        "credit_card": "credit_card",
        "car_number": "car_number"
    }


def test_create_parking(client) -> None:
    parking_data = {"address": "Moscow",
                    "count_places": 10}
    resp = client.post("/parkings", json=parking_data)

    assert resp.status_code == 201
    assert  resp.json == {
        "id": 3,
        "address": "Moscow",
        "count_places": 10,
        "count_available_places": 10,
        "opened": True
    }


def test_client_parking_in(client) -> None:
    data = {"client_id": 1,
            "parking_id": 2}
    resp = client.post("/client_parkings", json=data)

    assert resp.status_code == 201


def test_client_parking_out(client) -> None:
    data = {"client_id": 1,
            "parking_id": 1}
    resp = client.delete("/client_parkings", json=data)

    assert resp.status_code == 201