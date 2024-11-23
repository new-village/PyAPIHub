from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_strptime():
    response = client.post("/jpdate/strptime", json={"date_str": "令和3年12月31日"})
    assert response.status_code == 200
    assert response.json() == {"date_str": "2021-12-31"}

def test_strftime():
    response = client.post("/jpdate/strftime", json={"date_str": "2021-12-31"})
    assert response.status_code == 200
    assert response.json() == {"date_str": "令和3年12月31日"}
