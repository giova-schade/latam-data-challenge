import json
import os

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

                        if "emojis" in data and data["emojis"] is not None:
                            for emoji_entry in data["emojis"]:
                                emojis_data.append(
                                    {
                                        "tweet_id": data["id"],
                                        "emoji": emoji_entry["emoji"],
                                        "count": emoji_entry.get("count", 1),
                                    }
                                )

                        if "hashtags" in data and data["hashtags"] is not None:
                            for hashtag_entry in data["hashtags"]:
                                hashtags_data.append(
                                    {"tweet_id": data["id"], "hashtag": hashtag_entry}
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

                        if (
                            "mentionedUsers" in data
                            and data["mentionedUsers"] is not None
                        ):
                            for mention_entry in data["mentionedUsers"]:
                                mentioned_user_id = mention_entry["id"]
                                if mentioned_user_id in existing_user_ids:
                                    mentions_data.append(
                                        {
                                            "tweet_id": data["id"],
                                            "mentioned_user_id": mentioned_user_id,
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
