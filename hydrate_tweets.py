"""
Parses through the json and uses twitter API to hydrate (get full JSON) 
of the tweets mentioned as sources.
The script requires the raw json files to be stored in ../raw-data/
"""
import json
import twitter_api as tw

def _hydrate_tweets(rawfile, outfile='tweet_data.json', idsfile='ids.txt'):
    """Hydrate all the twitter links in the rawfile sources, and store json in outfile.
    
    Calls twitter API to get the full json from the tweet ID (hydration). Stores the ids hydrated in idsfile.
    Args:
         rawfile: filepath to the input rawdata json
         outfile: filepath to save the hydrated tweets json, default = 'tweet_data.json'
         idsfile: [optional] path to save the ids to the tweets hydrated.     
    Note: tweet links to a page are ignored. 
    Bad Links like "https://twitter.com/rajeshtope11" are present in the raw data
    """
    #open raw data file
    with open(rawfile) as f:
        raw_data = json.load(f)

    #Get the set of twitter IDS
    twitter_ids = []
    for data in raw_data['raw_data']:
        if 'twitter.com' in data['source1']:
            twitter_ids.append(tw.get_id(data['source1']))
        if 'twitter.com' in data['source2']:
            twitter_ids.append(tw.get_id(data['source2']))
        if 'twitter.com' in data['source3']:
            twitter_ids.append(tw.get_id(data['source3']))

    twitter_ids_set = list(set(twitter_ids))

    #write the ids to file
    with open(idsfile, 'w') as f:
        for item in twitter_ids_set:
            f.write("%s\n" % item)

    #authenticate twitter API
    tapi = tw.TwitterAPI()
    t = tapi.twarc

    #hydrate tweets (results in a generator object)
    hydrated_tweets = t.hydrate(open(idsfile))

    #store the full tweets in json object
    tweet_data = {}
    for tweet in hydrated_tweets:
        tid = tweet['id']
        tweet_data[tid] = tweet

    #save to json file
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(tweet_data, f, ensure_ascii=False, indent=4)

def main():
    """call hydrate_tweets for all the rawdata files."""
    
    raw = '../raw-data/raw_data'
    out = '../interim-data/hydrated_tweets/hydrated_tweets'
    ids = '../interim-data/ids/id'
    for i in range(7):
        rawfile = raw + str(i+1) + '.json'
        outfile = out + str(i+1) + '.json'
        idsfile = ids + str(i+1) +'.txt'
        _hydrate_tweets(rawfile, outfile, idsfile)

if __name__ == '__main__':
    main()
