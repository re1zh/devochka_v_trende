from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)