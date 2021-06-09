
#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py


import tweepy
import logging
from config import create_api
import time
import re
from googlesearch import search
import sys
import io


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, since_id):

    logger.info("Collecting info")

    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():

        new_since_id = max(tweet.id, new_since_id)


        if tweet.in_reply_to_status_id is not None:
            in_reply_to_status_id = tweet.id
            status_id = tweet.in_reply_to_status_id
            tweet_u = api.get_status(status_id,tweet_mode='extended')

        logger.info(f"Answering to {tweet.user.name}")
        

        # remove words between 1 and 3
        shortword = re.compile(r'\W*\b\w{1,3}\b')

        keywords_search = str(shortword.sub('', tweet_u.full_text))

        print(keywords_search)

        if keywords_search is not None:

                mystring = search(keywords_search, num_results=50)
        else:
                mystring = search("error", num_results=1)

        print(mystring)

        output_info=[]
        for word in mystring:
                if "harvard" in word or "cornell" in word or "researchgate" in word or "yale" in word or "rutgers" in word or "caltech" in word or "upenn" in word or "princeton" in word or "columbia" in word or "journal" in word or "mit" in word or "stanford" in word or "gov" in word or "pubmed" in word or "theguardian" in word or "aaas" in word or "bbc" in word or "rice" in word or "ams" in word or "sciencemag" in word or "research" in word or "article" in word or "publication" in word or "nationalgeographic" in word or "ngenes" in word:
                                output_info.append(word)
                                infostring = ' '.join(output_info)
        print(infostring)


        if infostring is not None:
                output_info4 = output_info[:5]
                infostring = ' '.join(output_info4)
                print(infostring)
                status = "Hi there! This may be what you're looking for " + infostring
                len(status) <= 280
                api.update_status(status, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)

        else:
                status = "Sorry, I cannot help you with that :(. You might want to try again with a distinctly sourced Tweet"
                api.update_status(status, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)

        print(status)

        return new_since_id
    return check_mentions





def main():
    api = create_api()
    since_id = 1 #the last mention you have.
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(15)

if __name__ == "__main__":
    main()





