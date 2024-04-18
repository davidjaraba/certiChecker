from unittest import TestCase

import pytest
import requests
# from app.crud.certificate import get_certificate
from unittest.mock import patch, MagicMock
from app.api.routers.certificates import router

from fastapi.testclient import TestClient
from app.crud import certificate

client = TestClient(router)


# @pytest.fixture
# def mock_crud(mocker):
#     mock = Mock()
#     # mocker.patch('app.crud.certificate.get_certificate', return_value=mock)
#     mock.get_certificate.return_value = """
#         "name": "sadas"
#     """
#     return mock
#
# @pytest.fixture
# def client():
#     with certificate.test_client() as client:
#         yield client
#

@pytest.mark.asyncio
async def test_get_by_id():
    # with patch.object(certificate, "get_certificate") as mock_obtener_datos: mock_obtener_datos.return_value = {
    #     "name": "asdasd"
    # }

    response = client.get(
        "http://localhost:8000/api/certificates/10")

    assert response.status_code == 2222
    assert True == False


class Tests(TestCase):
    async def test_get_by_id(self):
        with patch.object(certificate, "get_certificate") as mock_obtener_datos: mock_obtener_datos.return_value = {
            "name": "asdasd"
        }
        response = client.get(
            "http://localhost:8000/api/certificates/10")

        assert response.status_code == 2222
        assert True == False
        # mock_res = [{
        #     "name": "sdasdasda"
        # }]
        # with patch("app.crud.certificate.get_certificaste", new=MagicMock(return_value=mock_res)): response = client.get(
        #     "http://localhost:8000/api/certificates/10")
        #
        # print(response)
        #
        # assert response.status_code == "cxczxc204"
        # data = response.json()
        #
        # assert len(data) > 0


def test_get_by_id_success():
    # response = requests.get("http://localhost:8000/api/certificates/10")
    # mocker.patch.object(certificate, "get_certificate", return_value="""
    #     "name": "asda"
    # """)

    with patch.object(certificate, 'get_certificate', return_value=[{
        "name": "asd"
    }]): response = client.get("http://localhost:8000/api/certificates/10")

    # mock_get_cert_by_id.return_value = """
    #     "name": "asdasdsa"
    # """

    assert response.status_code == 200
    data = response.json()

    print(data)

    assert len(data) > 0

#
# class TestCertificates(TestCase):
#     # @patch("app.crud.certificate.get_certificate")


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
