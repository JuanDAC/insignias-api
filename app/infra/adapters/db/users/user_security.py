from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.infra.adapters.db.session import get_db
from sqlmodel import Session, select
from jwt import decode, ExpiredSignatureError, InvalidTokenError, encode
from app.infra.adapters.db.users.user_orm import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
from uuid import uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def decode_token(token, secret_key):
  try:
    payload = decode(token, secret_key, algorithms=['HS256'])
    return payload
  except ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expirado")
  except InvalidTokenError:
    raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales incorrectas",
    headers={"WWW-Authenticate": "Bearer"},
  )

  user_token = User

  try:
    user_token = decode_token(token)
  except Exception as e:
    raise credentials_exception from e

  user = db.exec(select(User).filter(User.id == user_token.id)).first()

  if not user:
    raise credentials_exception

  return user

secret_key = settings.SECRET_KEY or uuid4()
algorithm = settings.JWT_ALGORITHM or "HS256"
access_token_expire_minutes = int(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(datetime.UTC) + timedelta(minutes=access_token_expire_minutes)
  to_encode.update({"exp": expire.timestamp()})
  encoded_jwt = encode(to_encode, secret_key, algorithm=algorithm)
  return encoded_jwt