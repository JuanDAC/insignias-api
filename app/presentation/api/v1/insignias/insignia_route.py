from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session
from botocore.exceptions import ClientError

from .insignia_dto import InsigniaCreate

from .....core.entities.insignia.insignia_entity import Insignia
from .....core.entities.user.user_entity import User
from .....core.entities.base_entity import ID

from .....infra.adapters.aws.s3.upload_file_to_s3 import upload_file_to_s3
from .....infra.adapters.db.session import get_db
from .....infra.adapters.db.users.user_security import get_current_user

from .....core.use_cases.insignia.create_insignia import create_insignia
from .....core.use_cases.insignia.get_insignias import get_insignias
from .....core.use_cases.insignia.get_insignia_by_id import get_insignia_by_id
from .....core.use_cases.insignia.assign_insignia_to_user import assign_insignia_to_user
from .....core.use_cases.insignia.upload_insignia_image import upload_insignia_image

router = APIRouter(
  prefix="/insignias",
  tags=["insignias"]
)

@router.post("/", response_model=Insignia, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
def create_new_insignia(insignia: InsigniaCreate, db: Session = Depends(get_db)):
  return create_insignia(db=db, insignia=insignia)

@router.get("/", response_model=list[Insignia], dependencies=[Depends(get_current_user)])
def read_insignias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  insignias = get_insignias(db, skip=skip, limit=limit)
  return insignias

@router.get("/{insignia_id}", response_model=Insignia, dependencies=[Depends(get_current_user)])
def read_insignia(insignia_id: ID, db: Session = Depends(get_db)):
  db_insignia = get_insignia_by_id(db, insignia_id=insignia_id)
  if db_insignia is None:
    raise HTTPException(status_code=404, detail="Insignia not found")
  return db_insignia

@router.get("/{insignia_id}/asignar", response_model=Insignia, dependencies=[Depends(get_current_user)])
def read_insignia(insignia_id: ID, db: Session = Depends(get_db), user: User  = Depends(get_current_user)):
  db_insignia = assign_insignia_to_user(db, insignia_id=insignia_id, user=user)
  if db_insignia is None:
    raise HTTPException(status_code=404, detail="Insignia not found")
  return db_insignia

@router.put("/{insignia_id}/imagen", dependencies=[Depends(get_current_user)])
async def upload_insignia_image(insignia_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
  try:
    if not image.content_type.startswith("image/"):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format")

    image_url = await upload_file_to_s3(image.filename, await image.read())

    insignia = upload_insignia_image(db, insignia_id=insignia_id, image_url=image_url)

    if insignia is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insignia not found")

  except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'AccessDenied':
      raise HTTPException(status_code=403, detail="You do not have permission to upload files to S3")
    elif error_code == 'InvalidBucketName':
      raise HTTPException(status_code=400, detail="Invalid bucket name")
    elif error_code == 'NoSuchBucket':
      raise HTTPException(status_code=404, detail="Bucket does not exist")
    else:
      raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")
  except HTTPException as e:
    raise e
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="An unexpected error occurred while uploading the image."
    )
