from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# config file paramters
from get_twitter_data.models import Tweets, Users
from get_twitter_data.serializers import TweetsSerializer, UsersSerializer


'''
input:
{
	"search_on": "tweets",
	"filter_fields": [
		{
		"field_name": "author_screen_name",
		"options": [
			{
			"key":"startswith",
			"value": "Z"
			},{
			"key":"endswith",
			"value": "a"
			}]
		},
		{
		"field_name": "retweet_count",
		"options": [
			{
			"key":"gte",
			"value": "10"
			}]
		}]
	
}
Output:
Status code 200
{
results_count : 10 #integer of the total count
filtered_data: [USER/TWEET OBJECT ]  #list
}


'''


@api_view(['POST'])
def filtered_search(request):

    if request.method == 'POST':
        search_details = request.data
        total_result = 0
        if search_details['filter_on'] == 'tweets':
            search_results = Tweets.objects.filter()
            for filter_filter in search_details['filter_fields']:
                for field_option in filter_filter['options']:
                    query_field = filter_filter['field_name']+ '__' + field_option['key']
                    query_value = field_option['value']
                    search_results = search_results.filter(**{query_field: query_value})
                    total_result = search_results.count()
            search_data_serialized = TweetsSerializer(search_results, many=True)
            return Response({'results': total_result, 'filtered_data': search_data_serialized.data}, status=status.HTTP_200_OK)
        else:
            search_results = Users.objects.filter()
            for filter_filter in search_details['filter_fields']:
                for field_option in filter_filter['options']:
                    query_field = filter_filter['field_name']+ '__' + field_option['key']
                    query_value = field_option['value']
                    search_results = search_results.filter(**{query_field: query_value})
                    total_result = search_results.count()
            search_data_serialized = UsersSerializer(search_results, many=True)
            return Response({'results': total_result, 'filtered_data': search_data_serialized.data}, status=status.HTTP_200_OK)