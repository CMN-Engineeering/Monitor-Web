from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi # 1. Import certifi

# REMEMBER: Replace with your NEW password!
uri = "mongodb+srv://phandinhcuong02:Cuong123@cluster0.udg5k.mongodb.net/?appName=Cluster0"

# 2. Add tlsCAFile=certifi.where() to your client parameters
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)