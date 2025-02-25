from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.settings import Settings

settings = Settings().load_settings()
db_username = settings.MONGODB_DATABASE_USERNAME
db_password = settings.MONGODB_DATABASE_PASSWORD
uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.v0mjb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)