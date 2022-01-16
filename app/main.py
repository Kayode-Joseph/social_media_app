from typing import Counter
from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

import psycopg2

from psycopg2.extras import DictCursor, RealDictCursor

from random import randrange

while True:
    try:
        conn= psycopg2.connect(host='localhost',database='fastapi' ,user='postgres',password='MOSADMKO', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("successfully connected")
        break

    except Exception as err:
        print("error", err)
        


my_posts=[{"ID":1, "title":"food", "content":"i like food"}, {"ID":2, "title":"sex", "body":"I like 2 fok"}]

class Post(BaseModel):
    title: str
    body:str
    published: bool=True
    ratings: int=None


def get_postf(id, flag=False):
    for dict in my_posts:
        if dict["ID"]==id:
            flag=True
            return dict
        
    if not flag:
        return False

def delete_post(id, flag=False):
    for dict in my_posts:
        if dict["ID"]==id:
            flag=True
            my_posts.pop(my_posts.index(dict))
            return "post has been deleted", my_posts
    if not flag:
        return False

def update_post(id, flag=False):
    for dict in my_posts:
        if dict["ID"]==id:
            print(dict)
            flag=True
            return my_posts.index(dict)
    if flag==False:
        return False

        



app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello dlow"}


@app.get("/posts")
def root():
    #cursor.execute(""" SELECT * FROM posts""")
    #post= cursor.fetchall()
    #print(post)
    #return(post) 
    pass

@app.post("/posts")
def root(read: Post):

    cursor.execute("""INSERT INTO posts (title , content, published) values(%s,%s,%s) RETURNING *""", (read.title,read.body,read.published))
    post=cursor.fetchone()

    conn.commit()

    
    return{"new_post": post}





@app.get("/posts/{id}")
def root(id: int):

    cursor.execute("SELECT * FROM posts WHERE id= %s", (str(id)))
    
    
    
    post= cursor.fetchone()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")

    return{"The post is": post}

@app.delete("/posts/{id}")

def root(id:int, status_code=status.HTTP_204_NO_CONTENT):
     
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id)))

    
    de= cursor.fetchone()

    conn.commit()

    

    if not de:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


    
@app.put("/posts/{id}")

def root(id:int, post:Post):

    cursor.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *",(post.title,post.body,post.published,str(id)))

    up=cursor.fetchone()
    conn.commit()

    #print(up)

    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")

    else:
        
        return {"updated post":up}
    







