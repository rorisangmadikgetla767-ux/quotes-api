import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL enviroment variable is not set")
    conn = psycopg2.connect(database_url)
    return conn