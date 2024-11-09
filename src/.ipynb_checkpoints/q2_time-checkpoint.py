from collections import Counter
from typing import List, Tuple

from sqlalchemy import func

from models.emoji import Emoji
from utils.db_connection import get_session


def q2_time() -> List[Tuple[str, int]]:
    session = get_session()

    # Inicializar un contador para los emojis
    emoji_counter = Counter()

    # Procesar los registros en bloques de 1000
    batch_size = 1000
    offset = 0

    while True:
        # Consultar los registros en bloques
        result = (
            session.query(Emoji.emoji, func.sum(Emoji.count).label("total_count"))
            .group_by(Emoji.emoji)
            .offset(offset)
            .limit(batch_size)
            .all()
        )

        if not result:
            break

        # Contar los emojis en el bloque actual
        for row in result:
            emoji_counter[row.emoji] += row.total_count

        offset += batch_size

    session.close()

    # Obtener los 10 emojis más frecuentes
    top_emojis = emoji_counter.most_common(10)

    return top_emojis
