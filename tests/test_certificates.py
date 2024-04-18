import pytest
import requests


def make_request(path: str):
    base_url = "http://localhost:8000/api"
    response = requests.get(f'{base_url + path}')
    return response


def make_post(path: str, body):
    base_url = "http://localhost:8000/api"
    response = requests.post(f'{base_url + path}', json=body)
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


def test_create():
    body = {'name': "prueba"}
    response = make_post("/certificates", body)
    assert response.status_code == 201
    assert response.json()["name"] == "prueba"


def test_create_error_badrequest():
    body = {'namjhjje': "prueba"}
    response = make_post("/certificates", body)
    assert response.status_code == 400


def test_create_error_confict():
    body = {'name': "prueba"}
    make_post("/certificates", body)
    response = make_post("/certificates", body)
    assert response.status_code == 409



