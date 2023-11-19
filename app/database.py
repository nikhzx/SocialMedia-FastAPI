from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
engine = create_engine("postgresql://postgres:%s@localhost/postgres" % quote_plus("Nikhil@123"))

# password = 'Nikhil@123'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Nikhil%40@localhost/postgres"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


