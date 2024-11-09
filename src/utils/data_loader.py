import json
import os
import re

import emoji
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.emoji import Emoji
from models.hashtag import Hashtag
from models.media import Media
from models.mention import Mention
from models.tweet import Tweet
from models.user import User

load_dotenv()

database_url = os.getenv("DATABASE_URL", "")
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()
raw_data_folder = os.path.join(os.path.dirname(__file__), "../../data/raw")


def extract_emojis(text):
    """Extrae todos los emojis de un texto determinado."""
    return [char for char in text if emoji.is_emoji(char)]


def extract_mentions(text):
    """Extrae todas las menciones de un texto dado en el formato"""
    return re.findall(r"@\w+", text)


def extract_hashtags(text):
    """Extrae todos los hashtags de un texto dado en el formato #hashtag."""
    return re.findall(r"#\w+", text)


def process_and_load_data():
    """
    Proceso de carga de datos utilizando inserciones masivas con verificación de duplicados.
    """
    users_data = []
    tweets_data = []
    emojis_data = []
    hashtags_data = []
    media_data = []
    mentions_data = []

    existing_user_ids = {user.user_id for user in session.query(User.user_id).all()}

    for filename in os.listdir(raw_data_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        data = json.loads(line.strip())

                        user_data = data["user"]
                        if user_data["id"] not in existing_user_ids:
                            users_data.append(
                                {
                                    "user_id": user_data["id"],
                                    "username": user_data["username"],
                                    "displayname": user_data.get("displayname", None),
                                    "followers_count": user_data.get(
                                        "followersCount", 0
                                    ),
                                    "friends_count": user_data.get("friendsCount", 0),
                                    "verified": user_data.get("verified", False),
                                    "created_at": user_data.get("created", None),
                                }
                            )
                            existing_user_ids.add(user_data["id"])

                        if (
                            not session.query(Tweet)
                            .filter_by(tweet_id=data["id"])
                            .first()
                        ):
                            tweets_data.append(
                                {
                                    "tweet_id": data["id"],
                                    "url": data["url"],
                                    "content": data["content"],
                                    "date": data["date"],
                                    "lang": data.get("lang", "unknown"),
                                    "source": data.get("source", None),
                                    "user_id": user_data["id"],
                                    "reply_count": data.get("replyCount", 0),
                                    "retweet_count": data.get("retweetCount", 0),
                                    "like_count": data.get("likeCount", 0),
                                    "quote_count": data.get("quoteCount", 0),
                                }
                            )

                        content_fields = [
                            data.get("content", ""),
                            user_data.get("description", ""),
                        ]
                        all_emojis = []
                        all_mentions = []
                        all_hashtags = []
                        for field in content_fields:
                            if field:
                                found_emojis = extract_emojis(field)
                                all_emojis.extend(found_emojis)

                                found_mentions = extract_mentions(field)
                                all_mentions.extend(found_mentions)

                                found_hashtags = extract_hashtags(field)
                                all_hashtags.extend(found_hashtags)

                        if all_emojis:
                            emojis_data.append(
                                {
                                    "tweet_id": data["id"],
                                    "emojis": all_emojis,  # Almacena todos los emojis como un arreglo
                                }
                            )

                        if all_mentions:
                            mentions_data.append(
                                {
                                    "tweet_id": data["id"],
                                    "mentions": all_mentions,  # Almacena todas las menciones como un arreglo
                                }
                            )

                        if all_hashtags:
                            hashtags_data.append(
                                {
                                    "tweet_id": data["id"],
                                    "hashtags": all_hashtags,  # Almacena todos los hashtags como un arreglo
                                }
                            )

                        if "media" in data and data["media"] is not None:
                            for media_entry in data["media"]:
                                media_data.append(
                                    {
                                        "tweet_id": data["id"],
                                        "media_type": media_entry.get(
                                            "type", "unknown"
                                        ),
                                        "media_url": media_entry.get("url", ""),
                                    }
                                )

                    except json.JSONDecodeError as e:
                        print(f"Error al procesar JSON en {filename}: {e}")
                    except Exception as e:
                        print(f"Error al procesar los datos en {filename}: {e}")

    if users_data:
        session.bulk_insert_mappings(User, users_data)
    if tweets_data:
        session.bulk_insert_mappings(Tweet, tweets_data)
    if emojis_data:
        session.bulk_insert_mappings(Emoji, emojis_data)
    if hashtags_data:
        session.bulk_insert_mappings(Hashtag, hashtags_data)
    if media_data:
        session.bulk_insert_mappings(Media, media_data)
    if mentions_data:
        session.bulk_insert_mappings(Mention, mentions_data)

    session.commit()
    print("Datos cargados en la base de datos con éxito.")
