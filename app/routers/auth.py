from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database, models, schemas, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_creds: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()
   
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Invalid Creds")
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Creds")

    return {"Token":"Sample_Token"}