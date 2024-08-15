from kafka import KafkaConsumer
import logging
import json

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'face_verification',
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='face_verification_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume_messages(self):
        for message in self.consumer:
            user_id = message.key.decode('utf-8')
            photo_path = message.value.get('photo_path')
            logging.info(f"Processing face verification for user {user_id} with photo {photo_path}")
            # Обработка фото и запись векторов лица в логи
