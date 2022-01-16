from os import access
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import sys
#from app.routers.users import user

sys.path.append("/Users/hardknxcklife-/Documents/building apis/app")

from database import get_db

import schemas

import utils
import models

sys.path.append("/Users/hardknxcklife-/Documents/building apis/app/routers")


import oauth2
router= APIRouter(tags=["Authentication"])

@router.post('/login', response_model= schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm=Depends(), db: Session= Depends(get_db)):

    #outh2paassword request form has two fields; username and password
    
    user = db.query(models.User).filter(models.User.email==user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Credentials")

    if not utils.verify_pass(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")

    access_token= oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token": access_token, "token_type":"bearer"}


    