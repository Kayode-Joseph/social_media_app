from typing import Counter, List, Optional
import sys
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body, Depends
#from fastapi.security import oauth2
from passlib.utils.decor import deprecated_function
from pydantic import BaseModel

from sqlalchemy import func


from sqlalchemy.orm import Session
import psycopg2

from psycopg2.extras import DictCursor, RealDictCursor

from random import randrange


sys.path.append("/Users/hardknxcklife-/Documents/building apis/app")

import models

import schemas

from database import engine, get_db

import utils

sys.path.append("/Users/hardknxcklife-/Documents/building apis/app/routers")


import oauth2

models.Base.metadata.create_all(bind=engine)

router = APIRouter( prefix= "/posts",
tags=["Posts"])


@router.get("/" ,status_code=status.HTTP_200_OK ) #response_model=List[schemas.PostOut])
def get_post(db: Session= Depends(get_db), limit: int= 10, skip:int =0, search: Optional[str]= ""):

   # print("EROOR:" , models.Post) 
    
    post= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute(""" SELECT * FROM posts""")
    #post= cursor.fetchall()
    #print(post)

    results= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()#, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    print (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())
    return results


@router.post("/", response_model=schemas.PostResponse)
def create_post(read: schemas.Post, db: Session= Depends(get_db), current_user= Depends(oauth2.get_current_user)):

    print(current_user.email)

    #cursor.execute("""INSERT INTO posts (title , content, published) values(%s,%s,%s) RETURNING *""", (read.title,read.body,read.published))
    #post=cursor.fetchone()

    #conn.commit()
    

    #posts= models.Post(title=read.title, content=read.body, published=read.published) #orignial format
    posts= models.Post(owner_id=current_user.id, **read.dict()) #pydantic unpacked dict format
    db.add(posts)
    db.commit()
    db.refresh(posts)


    
    return posts

@router.get("/sqlalchemy")

def test_posts(db: Session= Depends(get_db)):

    

    posts= db.query(models.Post).filter(models.Post.id==2).all()
    
    
    return {'posts':posts}








@router.get("/{id}", response_model=schemas.PostOut)
def root(id: int, db: Session= Depends(get_db)):

    #cursor.execute("SELECT * FROM posts WHERE id= %s", (str(id)))
    # #post= cursor.fetchone()

    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")

    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
     
    #cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id)))

    
    #de= cursor.fetchone()

    #conn.commit()

    de= db.query(models.Post).filter(models.Post.id==id)

    

    if de.first()==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")

    if de.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are forbidden from performing this request")

    
    else:
        de.delete(synchronize_session=False)
        db.commit()

    
@router.put("/{id}", response_model=schemas.PostResponse)

def update_post(id:int, read:schemas.BaseClass, db: Session= Depends(get_db), current_user= Depends(oauth2.get_current_user)):

    #cursor.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *",(post.title,post.body,post.published,str(id)))

    #up=cursor.fetchone()
    #conn.commit()

    #print(up)

    

    post_query= db.query(models.Post).filter(models.Post.id==id)

    post=post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are forbidden from performing this request")

    else:
        post_query.update(read.dict(), synchronize_session=False)
        db.commit()
        
        
        #v=v.dict()
        
        return post_query.first()



