import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from models.base import Base

load_dotenv()


def create_schema_and_tables():
    """
    Crea el esquema y las tablas del proceso.
    """
    database_url = os.getenv("DATABASE_URL", "")
    schema_name = os.getenv("SCHEMA_NAME", "")

    if not database_url or not schema_name:
        print("Error: 'DATABASE_URL' o 'SCHEMA_NAME' no están configuradas.")
        return

    engine = create_engine(database_url, echo=True)

    try:
        with engine.begin() as connection:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))

        print(f"Esquema '{schema_name}' creado con éxito.")

        Base.metadata.create_all(engine)
        print("Tablas creadas con éxito.")

    except Exception as e:
        print(f"Error al crear el esquema o las tablas: {e}")
