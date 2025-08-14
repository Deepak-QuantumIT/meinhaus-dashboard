import os
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient

def get_voicemails():
    client = MongoClient("MONGO_URI")
    db = client["meinhaus"]
    return list(db["voicemails"].find().sort("metadata.creationTime", -1))
