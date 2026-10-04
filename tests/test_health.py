from fastapi.testclient import TestClient

from app.main import app

# Cliente de pruebas que llama a la app sin levantar un servidor real
client = TestClient(app)


def test_health():
    """/health debe responder 200 y {"status": "ok"}."""
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}
