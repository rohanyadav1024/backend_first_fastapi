from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing_extensions import Annotated

from . import schemas, database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# settings: Annotated[config.Settings, Depends(database.get_Settings)]


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_MINUTES = settings.expiry_time_taken


def create_access_token(data : dict):
    to_encode = data.copy()
    exp_time = int((datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)).timestamp())

    to_encode.update({'expiry' : exp_time})
    encoded_jwt = jwt.encode(claims=to_encode, algorithm=ALGORITHM, key=SECRET_KEY)
    return encoded_jwt



def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id is None:
            print('from oauth side')
            raise credential_exception

        token_data = schemas.TokenData(id=id)
        return token_data
    
    except JWTError:
        raise credential_exception
    

    
def get_current_user_key(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials for getting user")

    user_token = verify_access_token(token=token, credential_exception=credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == user_token.id).first()
    return user