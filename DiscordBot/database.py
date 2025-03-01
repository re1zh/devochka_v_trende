from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

try:
    with open('db_credits.json') as config_file:
        config = json.load(config_file)

    POSTGRES_USER = config.get('POSTGRES_USER')
    POSTGRES_PASS = config.get('POSTGRES_PASS')
    HOST = config.get('HOST')
    PORT = config.get('PORT')
    DATABASE = config.get('DATABASE')

except Exception as e:
    raise ValueError(f"Ошибка при загрузке конфигурации: {str(e)}")

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