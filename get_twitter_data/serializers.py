from rest_framework import serializers

from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class TweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = '__all__'

