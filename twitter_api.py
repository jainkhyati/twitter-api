"""
Implements key modules to use twitter API.

Extracts tweet IDs from url. Extract media, text and hashtags from the json
Modules used:
    dotenv - used to load environment variables which are the API key
    twarc - Module used to "hydrate" the tweets, that is fetching the full tweet jsons from the tweet ids
            twarc takes into account the rate limits set by twitter API
    tweepy - Python client library to fetch tweets
"""
import os
import re
import json
import tweepy
from twarc import Twarc
from dotenv import load_dotenv

class TwitterAPI:
    """Module to authenticate twitter API. Provides get_status functionality."""   
    
    def __init__(self):
        """Inits with authenticating tweepy."""
        
        #load keys
        load_dotenv('../.env')
        api_key = os.environ.get("TWITTER_API_KEY")
        api_secret_key = os.environ.get("TWITTER_API_KEY_SECRET")
        access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")        
        #authenticate tweepy
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)        
        self.api = tweepy.API(auth) 
        #authenticate twarc
        self.twarc = Twarc(api_key, api_secret_key, access_token, access_token_secret)
        
    def get_status(self, tweet_id):
        """ Call API to get extended tweet."""
        
        tweet = self.api.get_status(tweet_id, tweet_mode='extended')
        tweet_json = tweet._json
        return tweet_json
    
def get_id(tweet_url):
    """ Extracts tweet ID from the tweet url."""
    
    try:
        tweet_id = re.search('/status/(\d+)', tweet_url).group(1)
    except AttributeError: 
        tweet_id = None   
    return tweet_id

def get_media(tweet_json):
    """Extracts media links from the full tweet json.  
    Returns: List of image urls"""
    
    try:
        media_dict = tweet_json['extended_entities']['media']
        media = [m['media_url'] for m in media_dict]
    except KeyError:
        media = None
    return media

def get_text(tweet_json):
    """Get full tweet text."""
    
    text = tweet_json['full_text']
    return text

def get_hashtags(tweet_json):
    """Extracts the hashtags from tweet json.   
    Returns: List of hashtags"""
    
    h_dict = tweet_json['entities']['hashtags']
    hashtags = [h['text'] for h in h_dict]
    return hashtags

def get_user(tweet_json):
    """Get user name of the account."""
    
    user = tweet_json['user']['name']
    return user


def main():
    """Test twitter API (smoke test)."""
    
    tweet_url = 'https://twitter.com/mikeswatimayu/status/1280515672771039233'
    tweet_id = get_id(tweet_url)
    print("tweet id ", tweet_id)
    
    #authenticate API
    api = TwitterAPI()
    tweet = api.get_status(tweet_id)

    media = get_media(tweet)
    text = get_text(tweet)
    hashtags = get_hashtags(tweet)
    user = get_user(tweet)

    print("tweet media: ", media)
    print("tweet text: ", text)
    print("tweet hashtags: ", hashtags)
    print("user: ", user)

    with open('tweet.json', 'w') as outfile:
        json.dump(tweet, outfile)

if __name__ == '__main__':
    main()
