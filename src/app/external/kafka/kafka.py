import json
import logging
import os

from kafka import KafkaConsumer

from src.app.services.face_verification import FaceVerificationService


class KafkaConsumerService:
    """Класс для потребления сообщений из Kafka и обработки изображений лиц."""

    def __init__(self):
        """Инициализация Kafka Consumer и сервиса верификации лиц."""
        self.consumer = KafkaConsumer(
            'face_verification',
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='face_verification_group',
            value_deserializer=lambda key: json.loads(key.decode('utf-8')),
            key_deserializer=lambda key: key.decode('utf-8'),
        )
        self.face_service = FaceVerificationService()

    def consume_messages(self):
        """Потребление сообщений из Kafka и обработка изображений лиц."""
        for message in self.consumer:
            user_id = message.key
            photo_path = message.value.get('photo_path')
            logging.info(
                'Верификация пользователя {0}'.format(user_id),
            )

            try:
                with open(photo_path, 'rb') as photo_file:
                    img_bytes = photo_file.read()
                vector = self.face_service.generate_face_vector(img_bytes)
                logging.info('Сгенерирован вектор {0}'.format(vector))
            except Exception as exc:
                logging.error(
                    'Ошибка при обработке {0}: {1}'.format(user_id, exc),
                )
