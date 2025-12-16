
from pymongo import MongoClient
from app.core.config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client['portfolio']

# ╔══════════════════════════════╗ #
# ║         COLLECTIONS          ║ #
# ╚══════════════════════════════╝ #
myinfo_collection = db['personal-info']
experiences_collection = db['experience']
skills_collection = db['skills']
projects_collection = db['projects']
