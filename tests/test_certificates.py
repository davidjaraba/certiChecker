import pytest
import requests


def make_request(path: str):
    base_url = "http://localhost:8000/api"
    response = requests.get(f'{base_url + path}')
    return response


def test_get_by_id_success():
    response = make_request("/certificates/1")

    assert response.status_code == 200
    data = response.json()

    print(data)

    assert len(data) > 0


def test_get_by_id_not_found():
    response = make_request("/certificates/-1")

    assert response.status_code == 404


def test_get_by_id_error():
    response = make_request("/certificates/asdasdasd")

    assert response.status_code == 422
