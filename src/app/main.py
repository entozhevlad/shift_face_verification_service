import logging

from app.face_verification import FaceVerificationService


def main():
    """Основная функция для выполнения верификации лиц на изображениях."""
    # Настраиваем логгер
    logging.basicConfig(level=logging.DEBUG)

    service = FaceVerificationService()
    img = ['src/tests/img/1.jpg', 'src/tests/img/2.jpg', 'src/tests/img/3.jpg']

    face_vector = service.generate_face_vector(img[0])
    logging.info('Вектор {0}-го изображения: {1}'.format(1, face_vector))
    face_vector = service.generate_face_vector(img[1])
    logging.info('Вектор {0}-го изображения: {1}'.format(2, face_vector))
    face_vector = service.generate_face_vector(img[2])
    logging.info('Вектор {0}-го изображения: {1}'.format(3, face_vector))


if __name__ == '__main__':
    main()
