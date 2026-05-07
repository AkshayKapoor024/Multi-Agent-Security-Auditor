from pymongo import MongoClient
import os 
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGODB_URL')

# Adding Atlas URL
client = MongoClient(MONGO_URI)

# Creating or using Database vantaguard
db = client["vantaguard"]

# Creating or using users collection
users= db["users"]

# Creating or using sessions
sessions=db['sessions']

# Chat history collection
chat_history=db['chat_history']