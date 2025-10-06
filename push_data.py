import os
import sys
import json
import pandas as pd
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print("MongoDB URL:", MONGO_DB_URL)

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json_converter(self, file_path):
        """Convert CSV to JSON records"""
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient="records"))
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongodb(self, records, database, collection):
        """Insert JSON records into MongoDB"""
        try:
            mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = mongo_client[database]
            collection_ref = db[collection]
            collection_ref.insert_many(records)
            logging.info(f"Inserted {len(records)} records into {database}.{collection}")
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "ShishirAI"
    COLLECTION = "NetworkData"

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    print(f"Total records: {len(records)}")

    inserted = network_obj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(f" Successfully inserted {inserted} records.")
