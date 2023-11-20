from fastapi import FastAPI
import psycopg2, time
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine
from app.routers import post, user, auth


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'postgres', user = 'postgres',
                                password = 'Nikhil@123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Databse Connection was Succesfull")
        break
    except Exception as error:
        print("connection to Databse Failed")
        print("Error", error)
        time.sleep(3)

# my_post = [{'title':"Title for post 1", 'Content':"Content for post 1", 'id':1}, {'title':"Title for post2", 'content':"content for post 2", 'id':2}]

# def find_post(id):
#     for post in my_post:
#         if post['id']==id:
#             return post

# def find_index_post(id):
#     for index, post in enumerate(my_post):
#         if post['id'] == id:
#             return index

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello!": "API Is Working Fine -_- "}

# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'data': posts}