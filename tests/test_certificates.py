from unittest import TestCase

import pytest
import requests
# from app.crud.certificate import get_certificate
from unittest.mock import patch, MagicMock
from app.api.routers.certificates import router

from fastapi.testclient import TestClient
from app.crud import certificate

client = TestClient(router)




class Tests(TestCase):
    def test_get_by_id(self):
        mock_return_value = {"id": 10, "name": "asd"}

        with patch('app.api.routers.certificates.get_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.get("http://localhost:8000/api/certificates/10")

        mock_get_certificate.assert_called_once()

        assert response.status_code == 200
        data = response.json()

        assert len(data) > 0
        assert data["name"] == "asd"



# class TestCertificates(TestCase):

# def make_request(path: str):
#     base_url = "http://localhost:8000/api"
#     response = requests.get(f'{base_url + path}')
#     return response
#
# def make_post(path: str, body):
#     base_url = "http://localhost:8000/api"
#     response = requests.post(f'{base_url + path}', json=body)
#     return response


# def test_get_by_id_not_found(self):
#     response = make_request("/certificates/-1")
#
#     assert response.status_code == 404
#
# def test_get_by_id_error():
#     response = make_request("/certificates/asdasdasd")
#
#     assert response.status_code == 422
#
# def test_create():
#     body = {'name': "prueba"}
#     response = make_post("/certificates", body)
#     assert response.status_code == 201
#     assert response.json()["name"] == "prueba"
#
# def test_create_error_badrequest():
#     body = {'namjhjje': "prueba"}
#     response = make_post("/certificates", body)
#     assert response.status_code == 400
#
# def test_create_error_confict():
#     body = {'name': "prueba"}
#     make_post("/certificates", body)
#     response = make_post("/certificates", body)
#     assert response.status_code == 409
