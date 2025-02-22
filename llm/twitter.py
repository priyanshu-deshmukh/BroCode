import asyncio
from twikit import Client

from dotenv import find_dotenv,load_dotenv
import os


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Load Auth0 application settings into memory
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

async def twitter_scrape(query):
    USERNAME = TWITTER_USERNAME
    EMAIL = TWITTER_EMAIL
    PASSWORD = TWITTER_PASSWORD

    # Initialize client
    client = Client('en-US')
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )
    tweets = await client.search_tweet(query, 'Latest')
    a = []
    for tweet in tweets:
        a.append(tweet.text)
    return a

