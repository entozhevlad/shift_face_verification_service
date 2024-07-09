from deepface import DeepFace

class FaceVerificationService:
    """
    Сервис верификации лиц.
    """

    def __init__(self):
        """
        Конструктор класса.
        """

        self.model_name = 'Facenet'
        self.model = DeepFace.build_model(self.model_name)

    def generate_face_vector(self, img_path: str) -> list:
        """
        Метод для генерации вектора лица на основе фотографии.
        """

        try:
            # Метод represent возвращает список, берем первый элемент из списка
            face = DeepFace.represent(
                img_path, model_name=self.model_name, enforce_detection=True)[0]
            vectors = face['embedding']

            return vectors

        except Exception as e:
            return f'Ошибка при обработке изображения: {e}'
