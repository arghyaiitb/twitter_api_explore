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

'''
input:
{
"search_key" : "#BTC", #string
"load_limit" : 99 , #int
"tweet_lang" : "en", # string to search tweets only for a particular language
"tweet_since" : 2018-01-28 #date feild
}

Output:
Status code 200
{
"users_added": 12,
"tweets_added": 10
}


'''
@api_view(['POST'])
def search_keyword(request):
    if request.method == 'POST':
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)

        api = API(auth, wait_on_rate_limit=True)
        search_request_params = request.data
        print(search_request_params)
        search_key = search_request_params['search_key'] + ' -filter:retweets'
        load_limit = int(search_request_params.get('load_limit', 99))
        tweet_language = str(search_request_params.get('tweet_lang', 'en'))
        tweet_since = search_request_params.get('tweet_since', timezone.now().date() - timedelta(days=7))
        # print(search_key,load_limit,tweet_since, tweet_language)
        tweets = Cursor(api.search, q=search_key,
                        count=100, lang=tweet_language,
                        since=tweet_since, tweet_mode='extended').items()
        i = 0
        users_added = 0
        tweets_added = 0
        for tweet in tweets:
            i += 1
            if i >= load_limit:
                break
            if not Tweets.objects.filter(id=tweet.id):
                if process_tweet_data(tweet, search_key):
                    tweets_added +=1
            else:
                print('Tweet already exists')
                pass
            user_id = tweet.author.id
            if not Users.objects.filter(id=user_id):
                if process_user_data(tweet.author):
                    users_added += 1
            else:
                print('user already exists')
                # pass
        return Response(data={'tweets_added': tweets_added, 'users_added': users_added}, status=status.HTTP_201_CREATED)


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
        return True
    else:
        print('ERROR WHILE SAVING NEW TWEET')
        print(new_tweet_serializer.errors)
        return False


def get_hashtags_array(hashtags):
    return [hashtag['text'] for hashtag in hashtags]


def get_user_mention_array(user_mentions):
    return [user_mention['screen_name'] for user_mention in user_mentions]


def get_url_array(mentioned_urls):
    return [mentioned_url['url'] for mentioned_url in mentioned_urls]


def get_tweet_score(tweet_text):
    return 1.0


def process_user_data(twitter_user_object):
    user_object = {}
    user_object['id'] = twitter_user_object.id
    user_object['location'] = twitter_user_object.location
    user_object['name'] = twitter_user_object.name
    user_object['description'] = twitter_user_object.description
    user_object['screen_name'] = twitter_user_object.screen_name
    user_object['verified'] = twitter_user_object.verified
    user_object['created_at'] = twitter_user_object.created_at
    user_object['favourites_count'] = twitter_user_object.favourites_count
    user_object['followers_count'] = twitter_user_object.followers_count
    user_object['friends_count'] = twitter_user_object.friends_count
    user_object['statuses_count'] = twitter_user_object.statuses_count
    user_object['lang'] = twitter_user_object.lang
    user_data_serializer = UsersSerializer(data=user_object)
    if user_data_serializer.is_valid():
        user_data_serializer.save()
        return True
    else:
        print('ERROR WHILE SAVING USER')
        print(user_data_serializer.errors)
        return False
