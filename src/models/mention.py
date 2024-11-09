from sqlalchemy import JSON, BigInteger, Column, ForeignKey, Integer

from .base import SCHEMA_NAME, Base


class Mention(Base):
    __tablename__ = "mentions"
    __table_args__ = {"schema": SCHEMA_NAME}

    mention_id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey(f"{SCHEMA_NAME}.tweets.tweet_id"))
    mentions = Column(JSON)
