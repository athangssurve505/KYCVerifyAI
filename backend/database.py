import sqlite3
import pickle
from config import DB_PATH

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faces (
    user_id TEXT PRIMARY KEY,
    embedding BLOB
)
""")
conn.commit()

def save_face(user_id, embedding):
    cursor.execute(
        "INSERT OR REPLACE INTO faces VALUES (?, ?)",
        (user_id, pickle.dumps(embedding))
    )
    conn.commit()

def load_faces():
    cursor.execute("SELECT user_id, embedding FROM faces")
    return {
        user_id: pickle.loads(emb)
        for user_id, emb in cursor.fetchall()
    }
