from collections import Counter
from typing import List, Tuple

from sqlalchemy import text

from utils.db_connection import get_session


def q2_memory() -> List[Tuple[str, int]]:
    """
    Procesa los emojis almacenados en la base de datos en lotes para optimizar el uso de la memoria
    """
    session = get_session()
    batch_size = 1000
    emoji_counter: Counter[str] = Counter()

    query = text(
        """
        SELECT e.emojis
        FROM latam.emojis e;
    """
    )

    result = session.execute(query)

    batch = []
    for row in result:
        batch.append(row.emojis)
        if len(batch) >= batch_size:
            process_batch(batch, emoji_counter)
            batch = []

    if batch:
        process_batch(batch, emoji_counter)

    session.close()

    top_emojis = emoji_counter.most_common(10)

    return top_emojis


def process_batch(batch: List[List[str]], emoji_counter: Counter) -> None:
    for emojis in batch:
        if isinstance(emojis, list):
            emoji_counter.update(emojis)
