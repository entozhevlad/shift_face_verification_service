from deepface import DeepFace


class FaceVerificationService:
    """Сервис верификации лиц."""

    def __init__(self):
        """Конструктор класса."""
        self.model_name = 'Facenet'
        self.model = DeepFace.build_model(self.model_name)

    def generate_face_vector(self, img: str) -> list:
        """Метод для генерации вектора лица на основе фотографии."""
        model = self.model_name
        try:
            # Метод represent возвращает список, берем первый элемент из списка
            face = DeepFace.represent(
                img,
                model_name=model,
                enforce_detection=True,
            )[0]

        except Exception as exc:
            return 'Ошибка при обработке изображения: {0}'.format(exc)

        return face['embedding']
