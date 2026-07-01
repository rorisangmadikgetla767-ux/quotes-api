import psycopg2
from  dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    print(database_url)
    
    return conn