from twikit import Client, TooManyRequests
from datetime import datetime
from random import randint
from dotenv import load_dotenv
import os
import time
import csv
import asyncio

load_dotenv()
MINIMUM_TWEET = 500
QUERY = "banjir sumatera"

client = Client(
    'id-ID', 
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
email = os.getenv("EMAIL")

async def get_tweet(tweets):
    if tweets is None:
        print(f"Getting tweets...")
        tweets = await client.search_tweet(QUERY, product="Top")
    else:
        wait_time = randint(5, 10)
        print(f"Waiting for {wait_time} seconds...")
        time.sleep(wait_time)
        tweets = await tweets.next()
    
    return tweets

async def main():
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')
    client.load_cookies('cookies.json')

    with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['tweet_count', 'user_id', 'username', 'text', 'created_at'])

    tweets_count = 0
    tweets = None

    while tweets_count < MINIMUM_TWEET:
        try:
            tweets = await get_tweet(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue
        
        if not tweets:
            print("No more tweets found.")
            break

        for tweet in tweets:
            tweets_count += 1
            tweet_data = [
                tweets_count,
                tweet.user.id, 
                tweet.user.name, 
                tweet.text,
                tweet.created_at
            ]
            
            with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f"Total tweets collected: {tweets_count}")

    print("Finished collecting tweets.")

if __name__ == "__main__":
    asyncio.run(main())