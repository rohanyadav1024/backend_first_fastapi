from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from .. import oauth2

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix= "/vote", tags=["Votes"])

@router.post("/")
def vote_on_post( vote: schemas.Vote, db:Session = Depends(get_db), current_user : models.Users = Depends(oauth2.get_current_user_key) ):
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.id , models.Votes.user_id == current_user.id )
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)
        
        db_vote = models.Votes(user_id=current_user.id, post_id=vote.id)
        db.add(db_vote)   
        db.commit()
        db.refresh(db_vote)

        return {"message" : "successfully voted"}
    
    else:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message" : "Vote removed successfully"}
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 