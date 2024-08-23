from fastapi import APIRouter, File, HTTPException, UploadFile

from src.app.services.face_verification import FaceVerificationService

router = APIRouter()

face_service = FaceVerificationService()


@router.post('/generate_face_vector')
async def generate_face_vector(photo_file: UploadFile = File(...)):
    """Хэндлер генерации вектора лица."""
    try:
        photo_contents = await photo_file.read()
        vector = face_service.generate_face_vector(photo_contents)
        if isinstance(vector, str):
            raise HTTPException(status_code=400, detail=vector)
        return {'vector': vector}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
