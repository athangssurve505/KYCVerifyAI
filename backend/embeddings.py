from deepface import DeepFace

MODEL_NAME = "ArcFace"

def get_embedding(img):
    result = DeepFace.represent(
        img_path=img,
        model_name=MODEL_NAME,
        enforce_detection=False
    )
    return result[0]["embedding"]
