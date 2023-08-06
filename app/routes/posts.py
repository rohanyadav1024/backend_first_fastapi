from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from .. import oauth2
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix= "/post", tags=["Post"])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db)):
    
    posts_vote_query = db.query(models.Posts, func.count(models.Votes.post_id).label("votes"), models.Users).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).join(models.Users, models.Posts.owner_id == models.Users.id,  isouter=True).group_by(models.Posts.id).all()
        
    posts = [
        {
            **post.__dict__,
                "owner" : {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
            "votes" : votes
        }
        for post, votes, user in posts_vote_query
    ]
    return posts


@router.post("/create", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost,db : Session = Depends(get_db), current_user : models.Users = Depends(oauth2.get_current_user_key)):
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} not found")
    
    existing_post = db.query(models.Posts).filter(models.Posts.id == post.id).first()
    if existing_post:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)
   
    new_post = post.model_dump()
    user_post = models.Posts(**new_post, owner_id=current_user.id)
    
    db.add(user_post)
    db.commit()
    db.refresh(user_post)

    return user_post

@router.get("/user", response_model=List[schemas.PostOut], status_code=status.HTTP_302_FOUND)

def get_user_all_posts( db: Session = Depends(get_db), current_user :models.Users = Depends(oauth2.get_current_user_key)):

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No post, you are not registered")

    post = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} has no post")
    else:
        posts_vote_query = db.query(models.Posts, func.count(models.Votes.post_id).label("votes"), models.Users).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).join(models.Users, models.Posts.owner_id == models.Users.id,  isouter=True).filter(models.Posts.owner_id == current_user.id).group_by(models.Posts.id).all()
        
        posts = [
            {
                **post.__dict__,
                "owner" : {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                },
                "votes" : votes
            }
            
            
            for post, votes, user in posts_vote_query
        ]

        return posts
    

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int , db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user_key)):

    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with post id {id} not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Entered Invalid Credentials")

    post.delete(synchronize_session = False)
    db.commit()

    return status.HTTP_204_NO_CONTENT