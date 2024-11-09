from sqlalchemy import JSON, BigInteger, Column, ForeignKey, Integer

from .base import SCHEMA_NAME, Base


class Emoji(Base):
    __tablename__ = "emojis"
    __table_args__ = {"schema": SCHEMA_NAME}

    emoji_id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey(f"{SCHEMA_NAME}.tweets.tweet_id"))
    emojis = Column(JSON)
    count = Column(Integer)
