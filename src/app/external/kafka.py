from kafka import KafkaConsumer
import logging
import json
import os
from src.app.services.face_verification import FaceVerificationService

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'face_verification',
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='face_verification_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            key_deserializer=lambda x: x.decode('utf-8')  # Десериализация ключа
        )
        self.face_service = FaceVerificationService()

    def consume_messages(self):
        for message in self.consumer:
            user_id = message.key
            photo_path = message.value.get('photo_path')
            logging.info(f"Процесс верификации пользователя {user_id} с фото {photo_path}")
            
            try:
                # Загрузка изображения и его обработка
                with open(photo_path, 'rb') as file:
                    img_bytes = file.read()
                vector = self.face_service.generate_face_vector(img_bytes)
                logging.info(f"Сгенерирован вектор для пользователя {user_id}: {vector}")
            except Exception as e:
                logging.error(f"Ошибка при обработке изображения пользователя {user_id}: {e}")

