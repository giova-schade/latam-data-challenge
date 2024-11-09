import json
from collections import Counter
from typing import List, Tuple

from sqlalchemy import text

from utils.db_connection import get_session


def q3_time() -> List[Tuple[str, int]]:
    """
    Recupera y procesa los datos de la base de datos para obtener el top 10 de usuarios más influyentes
    en función del conteo de las menciones.
    """
    session = get_session()
    query = text(
        """
        SELECT m.mentions
        FROM latam.mentions m;
        """
    )

    result = session.execute(query).fetchall()
    session.close()

    mention_counter: Counter[str] = Counter()

    for row in result:
        mentions = row.mentions
        if isinstance(mentions, str):
            mentions = json.loads(mentions)

        if isinstance(mentions, list):
            mention_counter.update(mentions)

    top_mentions: List[Tuple[str, int]] = mention_counter.most_common(10)

    return top_mentions
