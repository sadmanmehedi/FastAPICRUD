from fastapi import FastAPI,Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()

class Post(BaseModel):#Schema
    title: str 
    content: str
    published: bool = True 
    rating: Optional[int]=None 

my_posts=[{"title":"title of the post 1","content":"content of post 1","id":1},{"title":"favourite food","content":" I like Pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

@app.get("/")#GET REQUEST
def root():
    return {"message":"Hello Sivan!"}

@app.get("/posts")#GET REQUEST
def get_posts():
    return {"data":my_posts}
    

@app.post("/posts")#POST REQUEST
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
        response.status_code=404
    return{"post_details":post}
