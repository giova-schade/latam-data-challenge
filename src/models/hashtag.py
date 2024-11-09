from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from .base import SCHEMA_NAME, Base


class Hashtag(Base):
    __tablename__ = "hashtags"
    __table_args__ = {"schema": SCHEMA_NAME}

    hashtag_id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey(f"{SCHEMA_NAME}.tweets.tweet_id"))
    hashtag = Column(String(255))