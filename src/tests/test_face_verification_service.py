import pytest
from PIL import Image
import numpy as np
from io import BytesIO

from src.app.services.face_verification import FaceVerificationService
@pytest.fixture(scope='module')
def face_service():
    """Фикстура для создания экземпляра FaceVerificationService"""
    return FaceVerificationService()

@pytest.fixture(scope='module')
def image_bytes():
    """Фикстура для байтов изображений"""
    def _read_image(image_path):
        with open(image_path, 'rb') as f:
            return f.read()

    return {
        '1': _read_image('src/tests/img/1.jpg'),
        '2': _read_image('src/tests/img/2.jpg'),
        '3': _read_image('src/tests/img/3.jpg'),
    }

@pytest.mark.parametrize("image_key", ['1', '2', '3'])
def test_generate_face_vector(face_service, image_bytes, image_key):
    """
    Тестирование метода generate_face_vector с использованием параметризации
    """
    image_data = image_bytes[image_key]
    result = face_service.generate_face_vector(image_data)
    assert isinstance(result, list), f"Expected list but got {type(result)}"
    assert len(result) > 0, "The returned face vector should not be empty"
    assert len(result) == 128, "The returned face vector should have length 128"

def test_generate_face_vector_exception(face_service):
    """
    Тестирование метода generate_face_vector с некорректными данными
    """
    invalid_image_data = b'invalid data'  # Некорректные данные для теста
    result = face_service.generate_face_vector(invalid_image_data)
    assert isinstance(result, str), f"Expected string but got {type(result)}"
    assert result.startswith("Ошибка при обработке изображения"), "Expected error message for invalid image data"
