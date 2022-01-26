from pydantic import BaseModel, validator, ValidationError
from datetime import datetime

from pydantic.networks import EmailStr
from typing import Optional





#the schema attributes are named according to the database attribute u want for post response models and according to the body for input models

class BaseClass(BaseModel):
    title: str
    content:str
    published: bool=True

    #ratings: int=None


class userout(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:     #convert from orm class to pydantic class. needed when returning data
        orm_mode=True

class userOutfr(BaseModel):
    User: userout
    followers:int

    class Config:     #convert from orm class to pydantic class. needed when returning data
        orm_mode=True


class Post(BaseClass):

    

    


    pass

class PostResponse(BaseClass):
    id: int
    created_at: datetime
    owner_id: int
    owner: userout

    class Config:
        orm_mode=True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode=True


class createuser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: int
    @validator('dir')
    def number_must_equal_0_or_1(cls,dir):
        directions=[0,1]

        if dir not in directions:
            raise ValueError(f'Must be either {directions}')
        return dir


class Follow(BaseModel):
    following: int
    dir: int
    @validator('dir')
    def number_must_equal_0_or_1(cls,dir):
        directions=[0,1]

        if dir not in directions:
            raise ValueError(f'Must be either {directions}')
        return dir



