import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from cipher import encrypt_message, decrypt_message

app = FastAPI(title="Transposition Cipher API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CipherRequest(BaseModel):
    text: str
    key: str

class CipherResponse(BaseModel):
    result: str

@app.post("/api/encrypt", response_model=CipherResponse)
def encrypt(request: CipherRequest):
    if not request.key:
        raise HTTPException(status_code=400, detail="Key cannot be empty")
    try:
        encrypted_text = encrypt_message(request.key, request.text)
        return CipherResponse(result=encrypted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/decrypt", response_model=CipherResponse)
def decrypt(request: CipherRequest):
    if not request.key:
        raise HTTPException(status_code=400, detail="Key cannot be empty")
    try:
        decrypted_text = decrypt_message(request.key, request.text)
        return CipherResponse(result=decrypted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# Serve frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
