from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Column, Integer, String, Text

from .base import SCHEMA_NAME, Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA_NAME}

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    displayname = Column(Text)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    verified = Column(Boolean)
    created_at = Column(TIMESTAMP)
