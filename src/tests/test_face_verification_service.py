import pytest

from src.app.services.face_verification import FaceVerificationService


@pytest.fixture(scope='module')
def face_service():
    """Фикстура для создания экземпляра FaceVerificationService"""
    return FaceVerificationService()


@pytest.fixture(scope='module')
def img_paths():
    """Фикстура для путей к изображениям"""
    return [
        'src/tests/img/1.jpg',
        'src/tests/img/2.jpg',
        'src/tests/img/3.jpg',
    ]


@pytest.mark.parametrize("img_path", [
    'src/tests/img/1.jpg',
    'src/tests/img/2.jpg',
    'src/tests/img/3.jpg',
])
def test_generate_face_vector(face_service, img_path):
    """
    Тестирование метода generate_face_vector с использованием параметризации
    """
    result = face_service.generate_face_vector(img_path)
    assert isinstance(result, list), f"Expected list but got {type(result)}"
    assert len(result) > 0, "The returned face vector should not be empty"


def test_generate_face_vector_exception(face_service):
    """
    Тестирование метода generate_face_vector с некорректным путем изображения
    """
    img_path = 'non_existent.jpg'
    result = face_service.generate_face_vector(img_path)
    assert isinstance(result, str), f"Expected string but got {type(result)}"
    assert result.startswith(
        'Ошибка при обработке изображения'), "Expected error message for invalid image path"
