from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, Integer, String, Text

from .base import SCHEMA_NAME, Base


class Tweet(Base):
    __tablename__ = "tweets"
    __table_args__ = {"schema": SCHEMA_NAME}

    tweet_id = Column(BigInteger, primary_key=True)
    url = Column(Text)
    content = Column(Text)
    date = Column(TIMESTAMP)
    lang = Column(String(10))
    source = Column(Text)
    user_id = Column(BigInteger, ForeignKey(f"{SCHEMA_NAME}.users.user_id"))
    reply_count = Column(Integer)
    retweet_count = Column(Integer)
    like_count = Column(Integer)
    quote_count = Column(Integer)
