import os

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
SCHEMA_NAME = os.getenv("SCHEMA_NAME", "latam")
