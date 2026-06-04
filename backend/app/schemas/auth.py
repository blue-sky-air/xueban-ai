from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    major: Optional[str] = None
    grade: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    username: str
    user_id: int

class UserInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    major: Optional[str] = None
    grade: Optional[str] = None
