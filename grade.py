import re
import pymongo
import csv
import os
import openai
from dotenv import load_dotenv
load_dotenv()

MONGO_PATH = os.getenv('MONGO_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

client = pymongo.MongoClient(MONGO_PATH)
db = client.eden
collection = db.twit


prompt = '''
I am looking for tweets about research into generative AI. That may include research papers, blog posts, or other resources about text-to-image models and large language models. I am particularly interested in tweets that have insights or resources (like code) for practioners.

On a scale of 1-5, with 1 being not interesting at all and 5 being very interesting to me, please grade the following tweet. Be concise, just give me the number.

Tweet: {tweet}
Grade:'''

def grade_tweet(tweet):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt.format(tweet=tweet),
        temperature=0.1,
        max_tokens=12,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    grade = int(response.choices[0].text.strip())
    return grade

def grade_new_tweets():
    for doc in collection.find({"ack": False}):
        text = doc['text']
        tweet = re.sub(r"http\S+", "", text).strip()
        if len(tweet) < 5:
            grade = 1
        else:
            grade = grade_tweet(text)
        update = {"$set": {"grade": grade, "ack": True}}
        collection.update_one({"_id": doc["_id"]}, update)

def export_best_tweet_ids():
    with open('viewer/public/tweets.txt', 'w') as f:
        # for doc in collection.find({"ack": True, "grade": 5}):
        for doc in collection.find({"grade": 5}):
            f.write(doc['tweet_id'] + '\n')


if __name__ == '__main__':
    #grade_new_tweets()
    print(MONGO_PATH)
    export_best_tweet_ids()