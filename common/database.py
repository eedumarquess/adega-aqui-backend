from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DB_CLIENT = os.getenv("DB_CLIENT")
DB_DATABASE = os.getenv("DB_DATABASE")

client = MongoClient(DB_CLIENT)
db = client[DB_DATABASE]


