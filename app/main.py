import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session
import time  # eita ami apadoto use kortesina as ami loop use kortesina
from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):  # Schema
    title: str
    content: str
    published: bool = True


# Ami ei ekta jaigai video theke ektu different korlam j ami ekhane while loop add korinai and timer korinai for the failed database connection if needed i can do it later
try:
    conn = psycopg2.connect(host='localhost', database='fastapi',
                            user='postgres', password='12345', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connection was succesful")

except Exception as error:
    print("Failed")


class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of the post 1", "content": "content of post 1", "id": 1}, {
    "title": "favourite food", "content": " I like Pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")  # GET REQUEST
def root():
    return {"message": "Hello Sivan!"}


@app.get("/posts")  # GET REQUEST
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # POST REQUEST
def create_posts(post: Post,db:Session=Depends(get_db)):
    #cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *""",
     #              (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}


@app.get("/posts/{id}")  # {id} hocche path parameter
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * from posts where id=%s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"post_details": post}

# Just for testing SQLALCHEMY


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data": posts}

# Delete Posts


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""Delete from posts where id=%s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    # deleting posts
    # find the index in the array that has the specific id and delete it
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesnot exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""Update posts SET title=%s,content=%s,published=%s where id=%s RETURNING*""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesnot exist")

    return {'message': updated_post}
