import pytest
import logging
from unittest.mock import MagicMock, patch
from io import BytesIO
from src.app.services.face_verification import FaceVerificationService
from src.app.external.kafka.kafka import KafkaConsumerService

@pytest.fixture(scope='module')
def face_service():
    """Фикстура для создания экземпляра FaceVerificationService."""
    return FaceVerificationService()

@pytest.fixture(scope='module')
def kafka_consumer_service(face_service):
    """Фикстура для создания экземпляра KafkaConsumerService."""
    with patch('src.app.external.kafka.kafka.KafkaConsumer') as MockKafkaConsumer:
        consumer_instance = MockKafkaConsumer.return_value
        consumer_instance.__iter__.return_value = iter([])  # Используем итератор
        service = KafkaConsumerService()
        service.face_service = face_service
        return service

def test_kafka_consumer_service_process_message(kafka_consumer_service, caplog):
    """
    Тестирование KafkaConsumerService и проверка записи результатов в логи.
    """
    with patch.object(kafka_consumer_service.consumer, '__iter__', return_value=iter([MagicMock(key='user123', value={'photo_path': 'fake_path.jpg'})])):
        with patch('builtins.open', MagicMock(return_value=BytesIO(b'test_image_bytes'))):
            with caplog.at_level(logging.INFO):
                kafka_consumer_service.consume_messages()

            # Проверяем, что в логи записаны ожидаемые сообщения
            assert "Верификация пользователя user123" in caplog.text
            assert "Сгенерирован вектор" in caplog.text

def test_kafka_consumer_service_error_handling(kafka_consumer_service, caplog):
    """
    Тестирование обработки ошибок в KafkaConsumerService и проверка записи ошибок в логи.
    """
    with patch.object(kafka_consumer_service.consumer, '__iter__', return_value=iter([MagicMock(key='user123', value={'photo_path': 'non_existent_path.jpg'})])):
        with patch('builtins.open', side_effect=FileNotFoundError('File not found')):
            with caplog.at_level(logging.ERROR):
                kafka_consumer_service.consume_messages()

            # Проверяем, что ошибка записана в логи
            assert "Ошибка при обработке user123" in caplog.text
            assert "File not found" in caplog.text
