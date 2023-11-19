from typing import List
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(post, "Published Status:", post.published)
    # post_dict = post.model_dump()
    # post_dict['id']=randrange(0, 10000)
    # my_post.append(post_dict)

    return new_post
    # return {"new_post": f"title: {payLoad['title']}, content: {payLoad['content']}"}


@router.get('/posts/{id}', response_model=schemas.Post)
# def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # post = find_post(id)
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', str(id))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id: {id} was not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with id: {id} was not found."}
    return post

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    # index = find_index_post(id)

    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not Present.")
    deleted_post.delete()
    db.commit()
    # my_post.pop(index)
    # return {'message': f"post with id {id} Deleted."}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/posts/{id}', response_model=schemas.Post)
def updatePost(id: int, post: schemas.PostUpdate, db :Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # index = find_index_post(id)
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', 
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not Present.")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_post[index]=post_dict
    return post_query.first()

