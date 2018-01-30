from django.db.models import Count
from django.db.models.functions import TruncDay, TruncDate, TruncMonth, TruncQuarter, TruncYear
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# config file paramters
from custom_search.serializers import GroupSearchSerializer
from get_twitter_data.models import Tweets, Users
from get_twitter_data.serializers import TweetsSerializer, UsersSerializer

'''
input:
{
	"group_by": ["lang", "author_screen_name"],
	"order_by": ["-count"],
	"date_group": {
		"start_date" : "2018-01-20",
		"end_date" : "2018-01-30",
		"bucket_by": "quarter"
	}
}

Output:
Status code 200
{
results_count : 10 #integer of the total count
filtered_data: [USER/TWEET OBJECT ]  #list
}


'''


@api_view(['POST'])
def group_search(request):
    if request.method == 'POST':
        search_details = request.data
        group_by = search_details['group_by']
        order_by = search_details['order_by']
        if not search_details.get('date_group'):
            search_results = Tweets.objects.all().values(*group_by).annotate(count=Count(group_by[0])).order_by(*order_by)
            response_serializer = GroupSearchSerializer(search_results, fields=(*group_by, 'count'), many=True)
            print(response_serializer.data)
            return Response(response_serializer.data,status=status.HTTP_200_OK)
        else:
            bucket_by = TruncDay('created_at')
            if search_details['date_group']['bucket_by'] == 'quarter':
                bucket_by = TruncQuarter('created_at')
            elif search_details['date_group']['bucket_by'] == 'month':
                bucket_by = TruncMonth('created_at')
            elif search_details['date_group']['bucket_by'] == 'year':
                bucket_by = TruncYear('created_at')

            search_results = Tweets.objects.filter(created_at__gte=search_details['date_group']['start_date'],
                                                   created_at__lte=search_details['date_group']['end_date'])\
                .annotate(date=bucket_by).values("date", *group_by)\
                .annotate(count=Count('date')).order_by(*order_by)

            response_serializer = GroupSearchSerializer(search_results, fields=(*group_by, 'date', 'count'), many=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)


