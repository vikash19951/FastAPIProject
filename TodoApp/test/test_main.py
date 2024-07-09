from fastapi.testclient import TestClient
import main
from fastapi import status


client = TestClient(main.app)


def test_return_health_check():
    resource = client.get("/healthy")
    assert resource.status_code == status.HTTP_200_OK
    assert resource.json() == {'status':'Healthy'}