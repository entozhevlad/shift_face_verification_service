from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from redis import Redis
from src.app.services.face_verification import FaceVerificationService
import hashlib
import json

router = APIRouter()

# Инициализация сервиса верификации лиц
face_service = FaceVerificationService()

# Функция зависимости для получения Redis клиента
def get_redis() -> Redis:
    return Redis(host='redis', port=6379, db=0, decode_responses=True)


@router.post('/generate_face_vector')
async def generate_face_vector(
    photo_file: UploadFile = File(...),
    redis_client: Redis = Depends(get_redis)  # Добавляем Redis в зависимости
):
    """Хэндлер для генерации вектора лица с кэшированием результата в Redis."""
    try:
        # Чтение содержимого загруженного файла
        photo_contents = await photo_file.read()

        # Генерация уникального ключа для кэша на основе хеша файла
        file_hash = hashlib.sha256(photo_contents).hexdigest()
        cache_key = f"face_vector:{file_hash}"

        # Проверка кэша
        cached_vector = redis_client.get(cache_key)
        if cached_vector:
            # Если вектор уже есть в кэше, возвращаем его
            return {'vector': json.loads(cached_vector)}

        # Генерация вектора лица через сервис
        vector = face_service.generate_face_vector(photo_contents)

        # Проверка результата на ошибку
        if isinstance(vector, str):
            raise HTTPException(status_code=400, detail=vector)

        # Кэширование результата на 60 секунд
        redis_client.setex(cache_key, 60, json.dumps(vector))

        # Возвращаем результат
        return {'vector': vector}

    except Exception as exc:
        # Обработка ошибок и возврат сообщения
        raise HTTPException(status_code=400, detail=str(exc))
