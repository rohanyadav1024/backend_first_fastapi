from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2, database

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def user_login(user_credential : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    
    db_user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
        
    if not utils.verify(plain_password=user_credential.password,hashed_password= db_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    token = oauth2.create_access_token(data={"user_id" : db_user.id})
    return schemas.Token(access_token=token, token_type="bearer")
