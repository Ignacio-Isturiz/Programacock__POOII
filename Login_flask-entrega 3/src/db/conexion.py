import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from urllib.parse import urlparse

def get_connection():
    url = urlparse(Config.SQLALCHEMY_DATABASE_URI)

    return psycopg2.connect(
        dbname=url.path[1:],  
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        cursor_factory=RealDictCursor
    )
