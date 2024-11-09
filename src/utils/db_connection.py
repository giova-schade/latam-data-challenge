import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

database_url = os.getenv("DATABASE_URL", "")

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)


def get_session():
    """Devuelve una nueva sesión de base de datos"""
    return Session()
