from face_store import get_all_faces
from similarity import cosine_similarity
from config import SIMILARITY_THRESHOLD

def verify_face(embedding):
    best_user, best_score = None, 0

    for user, stored_emb in get_all_faces():
        score = cosine_similarity(embedding, stored_emb)
        if score > best_score:
            best_user, best_score = user, score

    return {
        "verified": best_score > SIMILARITY_THRESHOLD,
        "matched_user": best_user,
        "similarity_score": float(best_score)
    }
