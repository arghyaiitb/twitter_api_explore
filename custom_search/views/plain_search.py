from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings

from tweepy import OAuthHandler
from tweepy import Cursor, API

# config file paramters
from get_twitter_data.models import Tweets, Users
from get_twitter_data.serializers import TweetsSerializer, UsersSerializer

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
def plain_search(request):
    if request.method == 'POST':
        search_details = request.data
        sort_by = search_details['sort_by']
        search_key = search_details['search_key']
        if search_details['search_on'] == 'tweets':
            search_results = Tweets.objects.filter(full_text__search=search_key).order_by(*sort_by)
            search_data_serialized = TweetsSerializer(search_results, many=True)
            return Response(search_data_serialized.data, status=status.HTTP_200_OK)
        else:
            search_results = Users.objects.filter(name__search=search_key).order_by(*sort_by)
            search_data_serialized = UsersSerializer(search_results, many=True)
            return Response(search_data_serialized.data, status=status.HTTP_200_OK)