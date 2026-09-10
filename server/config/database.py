import os
import mysql.connector
from mysql.connector import pooling
from config.settings import Config

_pool = None


def _build_pool_kwargs() -> dict:
    """Build keyword arguments for MySQLConnectionPool.

    Adds SSL configuration when connecting to Aiven MySQL (free cloud tier).
    Aiven requires SSL and provides a CA cert (ca.pem) for verification.
    SSL is skipped only for plain localhost without any CA cert configured.
    """
    kwargs = dict(
        pool_name="internship_pool",
        pool_size=Config.DB_POOL_SIZE,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        autocommit=False,
        connection_timeout=10,
    )

    is_local = Config.DB_HOST in ("localhost", "127.0.0.1", "::1")

    if Config.DB_SSL_CA:
        # Aiven: CA cert path is relative to the server/ directory
        server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ca_path = os.path.join(server_dir, Config.DB_SSL_CA)
        kwargs["ssl_ca"] = ca_path
        kwargs["ssl_verify_cert"] = True
    elif not is_local:
        # Other cloud hosts without explicit CA — still enable SSL (no cert verification)
        kwargs["ssl_disabled"] = False

    return kwargs


def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(**_build_pool_kwargs())
    return _pool


def get_connection():
    return get_pool().get_connection()
