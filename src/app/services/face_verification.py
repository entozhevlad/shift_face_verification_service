from io import BytesIO

from deepface import DeepFace
from PIL import Image


class FaceVerificationService:
    """Сервис верификации лиц."""

    def __init__(self):
        """Конструктор класса."""
        self.model_name = 'Facenet'
        self.model = DeepFace.build_model(self.model_name)

    def generate_face_vector(self, img_bytes: bytes) -> list:
        """Метод для генерации вектора лица на основе фотографии."""
        model = self.model_name
        try:
            image = Image.open(BytesIO(img_bytes))
            image = image.convert('RGB')
            temp_file_path = '/tmp/temp_image.jpg'
            image.save(temp_file_path)

            # Метод represent возвращает список, берем первый элемент из списка
            face = DeepFace.represent(
                temp_file_path,
                model_name=model,
                enforce_detection=True,
            )[0]

        except Exception as exc:
            return 'Ошибка при обработке изображения: {0}'.format(exc)

        return face['embedding']
