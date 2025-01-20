from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from .user_dto import UserCreate

from app.core.entities.user.user_entity import User

from app.infra.adapters.db.session import get_db
from app.infra.adapters.db.users.user_security import pwd_context, verify_password, create_access_token, get_current_user

from app.core.use_cases.user.get_user_level import get_user_level
from app.core.use_cases.user.update_user_experience import update_user_experience
from app.core.use_cases.user.user_register import user_register
from app.core.use_cases.user.user_log import user_log

router = APIRouter(
  prefix="/usuarios",
  tags=["usuarios"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
  hashed_password = pwd_context.hash(user.password)
  user.password = None
  user.password_hash = hashed_password

  userResponse = user_register(db, user=user)

  return userResponse

@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):

  user = user_log(db, username=username, password=password)

  if not user:
    raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

  if not await verify_password(password, user.password):
    raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

  token = create_access_token(data={ "sub": user.id })

  return {"token": token}

@router.get("/{user_id}/nivel/", response_model=User, dependencies=[Depends(get_current_user)])
async def get_user_level_by_id(user_id: int, db: Session = Depends(get_db)):
  user_level = get_user_level(db, user_id=user_id)
  if user_level is None:
      raise HTTPException(status_code=404, detail="User level not found")
  return user_level

@router.post("/{user_id}/experiencia/", status_code=status.HTTP_200_CREATED, dependencies=[Depends(get_current_user)])
async def update_user_experience(user_id: int, experience: int, db: Session = Depends(get_db)):
  updated_user_level = update_user_experience(db, user_id=user_id, experience_delta=experience)
  if updated_user_level is None:
      raise HTTPException(status_code=404, detail="User not found")
  return {"message": "Experience updated successfully"}
