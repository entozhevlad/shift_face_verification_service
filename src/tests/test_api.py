import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

@pytest.fixture(scope='module')
def image_path():
    """Фикстура для пути к изображению"""
    return 'src/tests/img/1.jpg'

def test_generate_face_vector(image_path):
    with open(image_path, 'rb') as f:
        response = client.post("/face_verification/generate_face_vector", files={"file": f})
    assert response.status_code == 200
    result = response.json()
    assert "vector" in result
    assert isinstance(result["vector"], list)
    assert len(result["vector"]) == 128

def test_generate_face_vector_invalid():
    invalid_data = b'invalid data'
    response = client.post("/face_verification/generate_face_vector", files={"file": ("invalid.jpg", invalid_data, "image/jpeg")})
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Ошибка при обработке изображения" in result["detail"]
