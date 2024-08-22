from fastapi import APIRouter, File, HTTPException, UploadFile

from src.app.services.face_verification import FaceVerificationService

router = APIRouter()

face_service = FaceVerificationService()

@router.post('/generate_face_vector')
async def generate_face_vector(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        vector = face_service.generate_face_vector(contents)
        if isinstance(vector, str):
            raise HTTPException(status_code=400, detail=vector)
        return {'vector': vector}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
