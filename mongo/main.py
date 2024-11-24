import os
import json
import logging
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from bson import ObjectId  # ייבוא ObjectId ממודול bson


def serialize_dates(obj):
    """ convert OBJ and DATE to fit jason file"""
    if isinstance(obj, dict):
        return {k: serialize_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_dates(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

load_dotenv()

def main():
    try:
        mongo_uri = os.getenv('MONGO_URI')
        database_name = os.getenv('DATABASE_NAME')
        collection_name = os.getenv('COLLECTION_NAME')
        folder_path = os.getenv('FOLDER_PATH')
        last_run_filename = os.path.join(folder_path, "last_run.txt")

        #last upd
        with open(last_run_filename, "r") as fo:
                last_run_time = datetime.fromisoformat(fo.read().strip())

        blaksky_query = {"updatedAt": {"$gt": last_run_time}}

        # MongoDB
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # query
        documents = list(collection.find(blaksky_query))

        # add to exist jason file
        documents = serialize_dates(documents)
        json_data = json.dumps(documents, ensure_ascii=False, indent=2)
        data_file_name = os.path.join(folder_path, "data.json")

        with open(data_file_name, "r") as fi:
                existing_data = json.load(fi)
        existing_data.extend(documents)
        
        json_data = json.dumps(existing_data, ensure_ascii=False, indent=2)

        with open(data_file_name, "w") as fo:
            fo.write(json_data)

        with open(data_file_name, "w") as fo:
            fo.write(json_data)
        logging.info(f"Uploaded {data_file_name} to Azure Blob Storage.")

        # rewrite last_run
        last_run_time = datetime.now().isoformat()
        with open(last_run_filename, "w") as fo:
            fo.write(last_run_time)
        logging.info(f"Uploaded {last_run_filename} to Azure Blob Storage.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
