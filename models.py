from pydantic import BaseModel
from typing import List, Optional

class RegisterRequest(BaseModel):
    user_id: str
    frames: List[str]

class VerifyRequest(BaseModel):
    frames: List[str]

class RegisterResponse(BaseModel):
    identity_status: str
    user_id: Optional[str]
    matched_user: Optional[str]
    similarity_score: Optional[float]

class VerifyResponse(BaseModel):
    verified: bool
    matched_user: Optional[str]
    similarity_score: float
