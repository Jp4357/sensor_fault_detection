import pymongo
import pandas as pd
import json

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH = r"C:\Users\LENOVO\Desktop\sensor_fault_detection\aps_failure_training_set1.csv"
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"



if __name__ =="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

## convert dataframe to json so that we can dump these records to mongodb

    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    # print(json_record[0])

# insert converted json records to mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
