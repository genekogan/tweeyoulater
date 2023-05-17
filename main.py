import re
import pymongo
import csv
import os
from dotenv import load_dotenv
load_dotenv()

T_PATH = os.getenv('T_PATH')
MONGO_PATH = os.getenv('MONGO_PATH')
CSV_FILE = os.getenv('CSV_FILE')


client = pymongo.MongoClient(MONGO_PATH)
db = client.eden
collection = db.twit

def save_tweet(row):
    tweet_id, posted_at, screen_name, text = row['ID'], row['Posted at'], row['Screen name'], row['Text']
    if collection.find_one({"tweet_id": tweet_id}):
        print("Document", tweet_id, "already exists")
        return
    document = {"tweet_id": tweet_id, "date": posted_at, "user": screen_name, "text": text, "ack": False}
    result = collection.insert_one(document)
    print(f"Saved tweet {result.inserted_id}")


def update_timeline():
    cmd = f'{T_PATH} timeline -n 500 --csv > {CSV_FILE}'
    os.system(cmd)
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            save_tweet(row)

if __name__ == '__main__':
    update_timeline()