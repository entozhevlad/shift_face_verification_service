import logging

from app.face_verification import FaceVerificationService


def main():
    """
    Основная функция для выполнения верификации лиц на изображениях.
    """

    service = FaceVerificationService()
    img_path1 = 'src/tests/img/1.jpg'
    img_path2 = 'src/tests/img/2.jpg'
    img_path3 = 'src/tests/img/3.jpg'
    face_vector = service.generate_face_vector(img_path1)
    logging.info('Вектор 1-го изображения')
    logging.info(face_vector)
    face_vector = service.generate_face_vector(img_path2)
    logging.info('Вектор w-го изображения')
    logging.info(face_vector)
    face_vector = service.generate_face_vector(img_path3)
    logging.info('Вектор e-го изображения')
    logging.info(face_vector)


if __name__ == '__main__':
    main()
