from unittest import TestCase
from unittest.mock import patch
from fastapi import Response
from fastapi.exceptions import RequestValidationError
from app.api.routers.certificates import router
from fastapi.testclient import TestClient

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

    def test_get_by_id_not_found(self):
        mock_return_value = Response(status_code=404)

        with patch('app.api.routers.certificates.get_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.get("http://localhost:8000/api/certificates/10")

        mock_get_certificate.assert_called_once()

        assert response.status_code == 404

    def test_get_all(self):
        mock_return_value = [{"id": 10, "name": "asd"}, {"id": 11, "name": "222"}]

        with patch('app.api.routers.certificates.get_certificates',
                   return_value=mock_return_value) as mock_get_certificates:
            response = client.get("http://localhost:8000/api/certificates/")

        assert response.status_code == 200

        assert len(response.json()) == 2

    def test_create(self):
        mock_return_value = {"id": 10, "name": "PRUEBA"}

        with patch('app.api.routers.certificates.create_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.post("http://localhost:8000/api/certificates/",
                                   json={"name": "PRUEBA"}
                                   )

        mock_get_certificate.assert_called_once()

        assert response.status_code == 201
        data = response.json()

        assert len(data) > 0
        assert data["name"] == "PRUEBA"

    def test_create_conflict(self):
        mock_return_value = Response(status_code=409)

        with patch('app.api.routers.certificates.create_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.post("http://localhost:8000/api/certificates/",
                                   json={"name": "PRUEBA"}
                                   )

        mock_get_certificate.assert_called_once()

        assert response.status_code == 409

    def test_create_with_errors(self):
        mock_return_value = {"name": "PRUEBA"}

        with patch('app.api.routers.certificates.create_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            try:
                response = client.post("http://localhost:8000/api/certificates/",
                                       json={"namee": "PRUEBA"}
                                       )
            except RequestValidationError as e:
                assert True
            else:
                assert False

    def test_update(self):
        mock_return_value = {"id": 10, "name": "PRUEBA"}

        with patch('app.api.routers.certificates.update_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.put("http://localhost:8000/api/certificates/2",
                                  json={"name": "PRUEBA"}
                                  )

        mock_get_certificate.assert_called_once()

        assert response.status_code == 200
        data = response.json()

        assert len(data) > 0
        assert data["name"] == "PRUEBA"

    def test_update_conflict(self):
        mock_return_value = Response(status_code=409)

        with patch('app.api.routers.certificates.update_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.put("http://localhost:8000/api/certificates/2",
                                  json={"name": "PRUEBA"}
                                  )

        mock_get_certificate.assert_called_once()

        assert response.status_code == 409

    def test_update_with_errors(self):
        mock_return_value = {"name": "PRUEBA"}

        with patch('app.api.routers.certificates.update_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            try:
                response = client.put("http://localhost:8000/api/certificates/2",
                                      json={"namee": "PRUEBA"}
                                      )
            except RequestValidationError as e:
                assert True
            else:
                assert False

    def test_delete(self):
        mock_return_value = Response(status_code=204)
        with patch('app.api.routers.certificates.delete_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.delete("http://localhost:8000/api/certificates/2")

        mock_get_certificate.assert_called_once()

        assert response.status_code == 204

    def test_delete_not_found(self):
        mock_return_value = Response(status_code=404)
        with patch('app.api.routers.certificates.delete_certificate',
                   return_value=mock_return_value) as mock_get_certificate:
            response = client.delete("http://localhost:8000/api/certificates/2")

        mock_get_certificate.assert_called_once()

        assert response.status_code == 404


    