import datetime
from typing import List, Tuple

from sqlalchemy import text

from utils.db_connection import get_session


def q1_memory() -> List[Tuple[datetime.date, str]]:
    session = get_session()
    #  Consulta SQL directa para obtener las 10 fechas con más tweets y el usuario con más tweets en cada una
    query = text(
        """
        SELECT date_trunc('day', t.date) AS tweet_date, u.username, COUNT(t.tweet_id) AS tweet_count
        FROM latam.tweets t
        JOIN latam.users u ON t.user_id = u.user_id
        GROUP BY tweet_date, u.username
        ORDER BY tweet_count DESC
        LIMIT 10
    """
    )

    result = session.execute(query).fetchall()
    session.close()

    # Formatear el resultado en una lista de tuplas
    top_dates = [(row.tweet_date.date(), row.username) for row in result]

    return top_dates
