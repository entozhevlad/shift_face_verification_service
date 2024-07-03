import os
from deepface import DeepFace

class FaceVerificationService:
    def __init__(self):
        self.model_name = "Facenet"
        self.model = DeepFace.build_model(self.model_name)

    def generate_face_vector(self, img_path: str):
        """
        Метод для генерации вектора лица на основе фотографии
        """
        try:
            face = DeepFace.represent(
                img_path, model_name=self.model_name, enforce_detection=True)[0]
            vectors = face["embedding"]

            return vectors

        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            return None

