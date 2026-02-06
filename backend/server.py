import os
import shutil
import time                       # ✅ NEW
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# --------- CORS FIX (REQUIRED FOR REACT) ---------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite React
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- CONFIG ---------
MAX_VIDEO_SIZE_MB = 100
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_VIDEO_TYPES = {
    "video/mp4",
    "video/webm",
    "video/quicktime",
    "video/x-msvideo"
}

# --------- GLOBAL EXCEPTION HANDLER ---------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": str(exc)}
    )

# --------- UPLOAD ENDPOINT ---------
@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):

    # ---- 1) Check file exists ----
    if not video:
        raise HTTPException(status_code=400, detail="No video file received")

    # ---- 2) Validate file type ----
    if video.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid video type: {video.content_type}"
        )

    # ---- 3) Limit file size ----
    video.file.seek(0, os.SEEK_END)
    size_mb = video.file.tell() / (1024 * 1024)
    video.file.seek(0)

    if size_mb > MAX_VIDEO_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large: {size_mb:.2f}MB (limit {MAX_VIDEO_SIZE_MB}MB)"
        )

    # ---- 4) SAFE filename (FIXED BUG HERE) ----
    timestamp = int(time.time())                       # ✅ FIX
    safe_filename = f"kyc_{timestamp}_{video.filename}"
    save_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")

    print(f"Saved video: {save_path}")

    # ---- 5) Call your ML / Deepfake script here ----
    # result = run_your_model(save_path)
    result = "REAL"   # placeholder

    return {
        "message": "Upload successful",
        "filename": safe_filename,
        "size_mb": round(size_mb, 2),
        "result": result
    }
