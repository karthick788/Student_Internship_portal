import gridfs
from pymongo import MongoClient
from config.settings import Config

_client = None
_db = None
_fs = None


def get_mongo_db():
    """Lazy Mongo connection for resume files only. Never used by login."""
    global _client, _db
    if not Config.MONGO_URI:
        raise RuntimeError("MONGO_URI is not set. Resume upload needs MongoDB Atlas.")
    if _db is None:
        _client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=8000,
            connectTimeoutMS=8000,
        )
        _db = _client[Config.MONGO_DB_NAME]
        _client.admin.command("ping")
    return _db


def get_gridfs():
    global _fs
    if _fs is None:
        _fs = gridfs.GridFS(get_mongo_db())
    return _fs
