import datetime
from typing import List, Tuple

from sqlalchemy import desc, func

from models.tweet import Tweet
from models.user import User
from utils.db_connection import get_session


def q1_time() -> List[Tuple[datetime.date, str]]:
    session = get_session()

    # Consulta SQL para obtener las 10 fechas con más tweets y el usuario con más tweets en cada fecha
    subquery = (
        session.query(
            func.date(Tweet.date).label("tweet_date"),
            User.username,
            func.count(Tweet.tweet_id).label("tweet_count"),
        )
        .join(User, Tweet.user_id == User.user_id)
        .group_by(func.date(Tweet.date), User.username)
        .subquery()
    )

    result = (
        session.query(subquery.c.tweet_date, subquery.c.username)
        .order_by(desc(subquery.c.tweet_count))
        .limit(10)
        .all()
    )

    session.close()

    return [(row.tweet_date, row.username) for row in result]
