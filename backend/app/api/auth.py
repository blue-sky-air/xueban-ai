from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_token, decode_token
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserInfo
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/auth", tags=["认证"])
security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=401, detail="未登录")
    try:
        payload = decode_token(credentials.credentials)
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Token无效或已过期")

@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(
        username=data.username,
        password=hash_password(data.password),
        email=data.email,
        major=data.major,
        grade=data.grade
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(token=create_token(user.id), username=user.username, user_id=user.id)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return TokenResponse(token=create_token(user.id), username=user.username, user_id=user.id)

@router.post("/guest")
def guest_login(db: Session = Depends(get_db)):
    """游客登录 - 自动创建临时账号"""
    import time
    username = f"guest_{int(time.time())}"
    user = User(username=username, password=hash_password("guest"), email=None, major=None, grade=None)
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(token=create_token(user.id), username="游客用户", user_id=user.id)

@router.get("/me", response_model=UserInfo)
def me(user: User = Depends(get_current_user)):
    return UserInfo(id=user.id, username=user.username, email=user.email, major=user.major, grade=user.grade)
