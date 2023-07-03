from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app=FastAPI()

@app.get("/")#GET REQUEST
def root():
    return {"message":"Hello Sivan!"}

@app.post("/createposts")
def create_posts(payLoad: dict= Body(...)):
    print(payLoad)
    return {"new_post":f"title {payLoad['title']} content: {payLoad['content']}"}