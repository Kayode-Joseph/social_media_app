

from pyexpat import model
from fastapi import  status, HTTPException, Depends, APIRouter
from fastapi.params import Depends


from sqlalchemy import func

from sqlalchemy.orm import Session




#from app.schemas import Post

#sys.path.append("/Users/hardknxcklife-/Documents/building apis/app")

#import models

#import schemas

#from database import engine, get_db

#import utils

from .. import models, schemas, utils
from ..database import get_db, engine

models.Base.metadata.create_all(bind=engine)

#app = FastAPI()

router= APIRouter(tags=["Users"])








@router.post("/user", response_model= schemas.userout)
def create_user( read: schemas.createuser, db: Session= Depends(get_db)):
    
    #hash password- read.passwrd

    hashed_password = utils.hash_pass(read.password)

    read.password= hashed_password
    
    
    new_user= models.User(**read.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user




@router.get('/user/{id}' , response_model= schemas.userOutfr)

def get_user(id:int, db: Session= Depends(get_db) ):



    user= db.query(models.User, func.count(models.Follow.following).label("followers")).join(models.Follow, models.User.id==models.Follow.following, isouter=True).group_by(models.Follow.follower, models.User.id).filter(models.User.id==id)
    
    print(user)
    if not user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with this {id} deos not exist" )

    return user.first()
