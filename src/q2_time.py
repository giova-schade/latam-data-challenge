from collections import Counter
from typing import List, Tuple

from sqlalchemy import text

from utils.db_connection import get_session


def q2_time() -> List[Tuple[str, int]]:
    """
    Recupera y procesa los emojis almacenados en la base de datos para contar su frecuencia
    """
    session = get_session()
    query = text(
        """
        SELECT e.emojis
        FROM latam.emojis e;
    """
    )

    result = session.execute(query).fetchall()
    session.close()

    emoji_counter: Counter[str] = Counter()

    for row in result:
        emojis = row.emojis
        emoji_counter.update(emojis)

    top_emojis = emoji_counter.most_common(10)

    return top_emojis
