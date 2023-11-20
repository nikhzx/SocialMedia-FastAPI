from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix = '/users',
    tags = ["Users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db :Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/', response_model=List[schemas.UserOut])
def fetch_all_users(db :Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{id}', response_model= schemas.UserOut)
def fetch_user(id: int, db :Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id: {id} was not found.")
    return user