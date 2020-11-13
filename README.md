# Twitter API
Scripts to download tweet content using twitter API, and using beautifulsoup (without API).

## Using twitter API
TwitterAPI() authenticates [tweepy api](http://docs.tweepy.org/en/latest/api.html) and [twarc](https://github.com/DocNow/twarc). Get functions extract relevant entities from the tweet json. Twarc is a very useful command line that allows to get the tweet JSON object for a list of tweet ids.

*tweepy:* used to get_status of a given tweed_id

*twarc:* to hydrate a list of tweets. It takes account of the access limits set by twitter

**Authentication:**
A twitter developer account is required, to get the access keys. Add the keys to the .env file in home folder

TWITTER_API_KEY = 'your-key'

TWITTER_API_KEY_SECRET = 'your-key'

TWITTER_ACCESS_TOKEN = 'your-key'

TWITTER_ACCESS_TOKEN_SECRET = 'your-key'

**Running :**

run `twitter_api.py`
output: tweet information including the text, ID, user, and media link

Example:

`tweet id  1278900800530472960

tweet media:  ['http://pbs.twimg.com/media/Eb-RJoNVcAEwk44.jpg', 'http://pbs.twimg.com/media/Eb-RXCdUEAEwg9c.jpg', 'http://pbs.twimg.com/media/Eb-RaIzU4AAGEJw.jpg']

tweet text:  This is a letter which has been sent out by the ICMR DG yesterday. Now that multiple folks have confirmed genuineness, let me raise some issues with this letter on #vaccine #trials during a pandemic, in this case #COVID19
What are the ethical issues in this letter? Read on. https://t.co/EaJkeaHjmV

tweet hashtags:  ['vaccine', 'trials', 'COVID19']

user:  Anant Bhan`

## Hydrate tweets

Module to parse through the json and uses twitter API to hydrate (get full JSON) of the tweets mentioned as sources.

**Setup**
The script requires the raw json files to be stored in ../raw-data/
The expected names of files are: raw_data1.json, raw_data2.json, raw_data3.json, raw_data4.json, raw_data5.json, raw_data6.json, raw_data7.json

**Running**

run `hydrate_tweets.py`

Desired output: 

Hydrated tweets get stored in the folder  `interim-data/hydrated_tweets/`

The tweet ids get stored in `interim-data/ids/`

## Download Images

Script to get image urls from the hydrated tweets, download and store in `interim-data/imgs/`.


**Running**
1. Store hydrated tweets in the folder `interim-data/hydrated_tweets/`, by running `hydrate_tweets.py`
2. run `get_imgs.py`

Expected Result : Each (set of) image is downloaded in the folder `interim-data/imgs/` as its tweet id.
