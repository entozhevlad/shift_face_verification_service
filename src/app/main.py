from fastapi import FastAPI

from src.app.routers import face_verification

app = FastAPI()

@app.get('/')
def read_main():
    return {'message': 'Welcome to the Face Verification API'}

app.include_router(face_verification.router, prefix='/face_verification', tags=['face_verification'])
