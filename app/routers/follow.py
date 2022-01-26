from re import S
from fastapi import  status, HTTPException, Depends, APIRouter
from fastapi.params import  Depends
from sqlalchemy import null

from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db,engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter( prefix= "/follow",
tags=["Follow"])

@router.post("/")

def follow(fol: schemas.Follow,  db: Session= Depends(get_db), current_user= Depends(oauth2.get_current_user)):

    user= db.query(models.User).filter(models.User.id==fol.following).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= "User not found")

    follow_query= db.query(models.Follow).filter(models.Follow.following==fol.following, models.Follow.follower==current_user.id)
    
    if not follow_query.first():
        if fol.dir==1:
            new_follower= models.Follow(follower= current_user.id, following=fol.following)
            
            db.add(new_follower)
            db.commit()
            return{"Message": f"succesfully followed {fol.following}"}
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"You are not following {fol.following}")
    else:
        if fol.dir==1:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"You are already following {fol.following}")
        else:
            follow_query.delete(synchronize_session=False)
            db.commit()
            return {"Message": f"succesfully unfollowed {fol.following}"}




            
            
   




    
