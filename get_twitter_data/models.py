from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

# Create your models here.


class Tweets(models.Model):
    id = models.BigIntegerField(primary_key=True)  # tweet id in string is unique
    tweet_search = models.CharField(max_length=280)  # the string on which the search function was executed (generated by me)
    text = models.TextField()  # the original tweet if not full
    full_text = models.TextField() # the full tweet text
    timestamp_ms = models.DateTimeField()  # epoch time when the tweet was done
    user_id = models.CharField(max_length=32)  # match user data to tweet
    favourite_count = models.IntegerField(default=0)  # likes on the tweet
    lang = models.CharField(max_length='10')  # language of the tweet
    geo_location = JSONField()  # location tagged in the tweet
    reply_count = models.IntegerField()  # the total comments on the tweet
    retweet_count = models.IntegerField()  # total retweet on the tweet
    hashtags = ArrayField(models.CharField(max_length=280), default=[], null=True, blank=True)  # all the hastags used
    user_mentions = ArrayField(models.CharField(max_length=280), default=[], null=True, blank=True)  # all the hastags used  # all the users tages using @xyz
    urls = ArrayField(models.CharField(max_length=280), default=[], null=True, blank=True)  # all the hastags used  # all the urls linked to the tweet
    tweet_score = models.FloatField(default=0.0) #tf-idf algorithm


    def __str__(self):
        return self.id


class Users(models.Model):
    id = models.BigIntegerField(primary_key=True)  # user id of a person
    location = models.CharField(max_length=100, default=None, null=True)  # the location of the user
    name = models.CharField(max_length=200, default=None, null=True)  # name of the user
    description = models.TextField()  # description of the user / like bio
    screen_name = models.CharField(max_length=100, default=None, null=True)  # unique user name for using @user name
    verified = models.BooleanField(default=False)  # to see if the user is verified or not
    created_at = models.DateTimeField()  # when the user was created
    favourites_count = models.IntegerField(default=0)  # number of likes
    followers_count = models.IntegerField(default=0)  # people following this user
    friends_count = models.IntegerField(default=0)  # the number of people this user is following
    lang = models.CharField(max_length=20, default=None, null=True) # english
    statuses_count = models.IntegerField(default=0)  # total no. of tweets done by the user

    def __str__(self):
        return self.id