from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

class Post(BaseModel):#Schema
    title: str 
    content: str
    published: bool = True 
    rating: Optional[int]=None 


@app.get("/")#GET REQUEST
def root():
    return {"message":"Hello Sivan!"}

@app.get("/posts")#GET REQUEST
def get_posts():
    return {"data":"This is yours posts"}
    

@app.post("/posts")#POST REQUEST
def create_posts(post:Post):
    print(post)
    print(post.dict)
    return {"data":post}