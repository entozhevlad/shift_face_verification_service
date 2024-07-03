import logging
from app.face_verification import FaceVerificationService

def get_greetings() -> str:
    """Возвращает строку приветствия."""
    return 'Hello World!'


if __name__ == '__main__':
    service = FaceVerificationService()
    img_path_1 = "src/tests/img/1.jpg"
    img_path_2 = "src/tests/img/2.jpg"
    img_path_3 = "src/tests/img/3.jpg"
    face_vector = service.generate_face_vector(img_path_1)
    print(face_vector)
    face_vector = service.generate_face_vector(img_path_2)
    print(face_vector)
    face_vector = service.generate_face_vector(img_path_3)
    print(face_vector)
