import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'codesense.db')
DB_URI = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
    from . import analysis
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()
