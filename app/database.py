from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SQLALCHEMY_DATABASE_URL='postgresql://postgres:12345@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()