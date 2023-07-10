import psycopg2
from  psycopg2.extras import RealDictCursor
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time

app=FastAPI()

class Post(BaseModel):#Schema
    title: str 
    content: str
    published: bool = True 
#Ami ei ekta jaigai video theke ektu different korlam j ami ekhane while loop add korinai and timer korinai for the failed database connection if needed i can do it later
try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='12345',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database Connection was succesful")
        
except Exception as error:
        print("Connecting to database was failed")


class UpdatePost(BaseModel):
     title: str 
     content: str
     published: bool = True 
     rating: Optional[int]=None 

my_posts=[{"title":"title of the post 1","content":"content of post 1","id":1},{"title":"favourite food","content":" I like Pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")#GET REQUEST
def root():
    return {"message":"Hello Sivan!"}

@app.get("/posts")#GET REQUEST
def get_posts():
    return {"data":my_posts}
    

@app.post("/posts",status_code=status.HTTP_201_CREATED)#POST REQUEST
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,100000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return{"details":post}

@app.get("/posts/{id}")#{id} hocche path parameter
def get_post(id:int,response:Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return{"post_details":post}

#Delete Posts
@app.delete("/posts/{id}",status_code=
            status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #deleting posts
    #find the index in the array that has the specific id and delete it
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnot exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#UPDATE
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesnot exist")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return{'message':'update post'}