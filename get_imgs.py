"""
Script to get image urls from the hydrated tweets, download and store in /interim-data/imgs/.
Each (set of) image is downloaded in a folder as its tweet id.
Module used:
    urllib.request :  module defines functions and classes which help in opening URLs
"""
import os
import json 
import urllib.request
import twitter_api as tw

def download_images(tweetsfile, img_folder):
    """Download all the media linked in the tweetsfile json
    
    Args:
        tweetsfile: path to hydrated tweets json
        img_folder: path to folder to store all the downloaded images"""
    
    #load json containing all hydrated tweets
    with open(tweetsfile) as file:
        tweets_data = json.load(file)

    #parse through all tweets
    for tid in tweets_data:       
        #get media urls
        tweet = tweets_data[tid]
        media = tw.get_media(tweet)
        
        #create directory tid in img_folder
        dir_path = os.path.join(img_folder, tid)
        try: 
            os.mkdir(dir_path)
        except OSError as error: 
            print(error) 
        
        def _download_img(url, filename):
            with open(filename, 'wb') as file:
                file.write(urllib.request.urlopen(url).read())
                
        if media:
            #save all images in tid folder
            for i, url in enumerate(media):   
                #download image
                filename = str(i) +'.jpg'  
                img_path = os.path.join(dir_path, filename)
                _download_img(url, img_path)

def main():
    """Download images in all the hydrated tweet jsons into the images folder"""
    
    img_folder = '../interim-data/images'
    tweet_folder = '../interim-data/hydrated_tweets/'
    for i in range(7):        
        tweetsfile = tweet_folder + 'hydrated_tweets' + str(i+1) + '.json'
        download_images(tweetsfile, img_folder)
    
if __name__ == '__main__':
    main()
    
