from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import oauth2

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix= "/user")

@router.post("/create",response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #if user already exists
    existing_user = db.query(models.Users).filter(models.Users.id == user.id).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)
    
    new_user = user.model_dump(exclude={"password"})
    hashed_pass = utils.hash(user.password)
    db_user = models.Users(**new_user, password = hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.Users).all()
    
    return users

@router.get("/{id}", response_model=schemas.UserOut, status_code=status.HTTP_302_FOUND)
def get_single_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    else:
        return user
    

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int , db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user_key)):

    user = db.query(models.Users).filter(models.Users.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id {id} not found")
    
    if user.first().id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Entered Invalid Credentials")

    user.delete(synchronize_session = False)
    db.commit()

    return status.HTTP_204_NO_CONTENT
