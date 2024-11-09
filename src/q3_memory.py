from typing import List, Tuple

from sqlalchemy import text

from utils.db_connection import get_session


def q3_memory() -> List[Tuple[str, int]]:
    """
    Optimiza el uso de memoria al delegar el conteo y agrupación de menciones al motor de la base de datos
    """
    session = get_session()
    query = text(
        """
        SELECT mention, COUNT(*) AS mention_count
        FROM (
            SELECT jsonb_array_elements_text(m.mentions::jsonb) AS mention
            FROM latam.mentions m
        ) subquery
        GROUP BY mention
        ORDER BY mention_count DESC
        LIMIT 10;
        """
    )

    result = session.execute(query).fetchall()
    session.close()

    top_mentions: List[Tuple[str, int]] = [
        (row.mention, row.mention_count) for row in result
    ]

    return top_mentions
