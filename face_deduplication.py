from face_store import get_all_faces, store_face
from similarity import cosine_similarity
from config import SIMILARITY_THRESHOLD

def register_face(user_id, embedding):
    for stored_user, stored_emb in get_all_faces():
        score = cosine_similarity(embedding, stored_emb)
        if score > SIMILARITY_THRESHOLD:
            return {
                "identity_status": "DUPLICATE",
                "matched_user": stored_user,
                "similarity_score": float(score)
            }

    store_face(user_id, embedding)
    return {
        "identity_status": "UNIQUE",
        "user_id": user_id,
        "similarity_score": 1.0
    }
