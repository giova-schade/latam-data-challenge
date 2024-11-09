from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Text

from .base import SCHEMA_NAME, Base


class Media(Base):
    __tablename__ = "media"
    __table_args__ = {"schema": SCHEMA_NAME}

    media_id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey(f"{SCHEMA_NAME}.tweets.tweet_id"))
    media_type = Column(String(50))
    media_url = Column(Text)
