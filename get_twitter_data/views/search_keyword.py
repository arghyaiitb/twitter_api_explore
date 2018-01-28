from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import *
from django.conf import settings

from tweepy import OAuthHandler
from tweepy import Cursor, API


# config file paramters
atoken = settings.TWITTER_ATOKEN
asecret = settings.TWITTER_ASECRET
ckey = settings.TWITTER_CKEY
csecret = settings.TWITTER_CSECRET



@api_view(['POST'])
def search_keyword(request):

    if request.method == 'POST':
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)

        api = API(auth, wait_on_rate_limit=True)
        search_request_params = request.data
        print(search_request_params)
        search_key = search_request_params['search_key'] + ' -filter:retweets'
        load_limit = int(search_request_params.get('load_limit',99))
        tweet_language = str(search_request_params.get('tweet_lang', 'en'))
        tweet_since = search_request_params.get('tweet_since', timezone.now().date() - timedelta(days=7))
        # print(search_key,load_limit,tweet_since, tweet_language)
        tweets = Cursor(api.search, q=search_key,
                        count=100, lang=tweet_language,
                        since=tweet_since, tweet_mode='extended').items()
        i = 0
        for tweet in tweets:
            i+=1
            if i>=load_limit:
                break
            process_tweet_data(tweet, search_key)
            # if not Users.objects.filter(id=tweet.author['id']).count():
            #     process_user_data(tweet.author)
        return Response(status=status.HTTP_200_OK)


def process_tweet_data(tweet, twitter_search_term):
    new_tweet = {}
    new_tweet['id'] = tweet.id
    new_tweet['tweet_search'] = twitter_search_term
    new_tweet['full_text'] = tweet.full_text
    new_tweet['created_at'] = tweet.created_at
    new_tweet['author_id'] = tweet.author.id
    new_tweet['author_screen_name'] = tweet.author.screen_name
    new_tweet['favorite_count'] = tweet.favorite_count
    new_tweet['lang'] = tweet.lang
    new_tweet['geo_location'] = tweet.geo
    new_tweet['retweet_count'] = tweet.retweet_count
    new_tweet['hashtags'] = get_hashtags_array(tweet.entities['hashtags'])
    new_tweet['user_mentions'] = get_user_mention_array(tweet.entities['user_mentions'])
    new_tweet['urls'] = get_url_array(tweet.entities['urls'])
    new_tweet['tweet_score'] = get_tweet_score(tweet.full_text)
    new_tweet_serializer = TweetsSerializer(data=new_tweet)
    if new_tweet_serializer.is_valid():
        new_tweet_serializer.save()


def get_hashtags_array(hashtags):
    return [hashtag['text'] for hashtag in hashtags]

def get_user_mention_array(user_mentions):
    return [user_mention['screen_name'] for user_mention in user_mentions]

def get_url_array(mentioned_urls):
    return [mentioned_url['url'] for mentioned_url in mentioned_urls]

def get_tweet_score(tweet_text):
    return 1.0


def process_user_data(user_object):
    pass