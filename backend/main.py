from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import RegisterRequest, VerifyRequest
from utils import base64_to_image
from frame_selection import select_best_frame
from embeddings import get_embedding
from face_deduplication import register_face
from face_verification import verify_face

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register(req: RegisterRequest):
    frames = [base64_to_image(f) for f in req.frames]
    best = select_best_frame(frames)
    embedding = get_embedding(best)
    return register_face(req.user_id, embedding)

@app.post("/verify")
def verify(req: VerifyRequest):
    frames = [base64_to_image(f) for f in req.frames]
    best = select_best_frame(frames)
    embedding = get_embedding(best)
    return verify_face(embedding)
