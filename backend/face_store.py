import sqlite3
from config import DB_PATH
import numpy as np
import pickle

def get_db():
    return sqlite3.connect(DB_PATH, timeout=10.0)

def store_face(user_id, embedding):
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO faces (user_id, embedding) VALUES (?, ?)",
            (user_id, pickle.dumps(embedding))
        )
        conn.commit()
    finally:
        conn.close()

def get_all_faces():
    conn = get_db()
    try:
        rows = conn.execute("SELECT user_id, embedding FROM faces").fetchall()
        return [(r[0], pickle.loads(r[1])) for r in rows]
    finally:
        conn.close()