from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import StreamingHttpResponse

from get_twitter_data.models import Tweets, Users

import csv

'''
input:
{
	"filter_on": "tweets",
	"filter_fields":[
		{
		"field_name": "author_screen_name",
		"options": [
			{
			"key":"istartswith",
			"value": "i"
			}]
		},
		{
		"field_name": "retweet_count",
		"options": [
			{
			"key":"gte",
			"value": "0"
			}]
		}],
		
	"result_columns": ["retweet_count","id"] 
}


Output:
Status code 200
CSV file

'''


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@api_view(['GET', 'POST'])
def csv_data_dump(request):
    search_results = None
    search_details = request.data
    download_columns = search_details['result_columns']
    if search_details['filter_on'] == 'tweets':
        search_results = Tweets.objects.filter()
        for filter_filter in search_details['filter_fields']:
            for field_option in filter_filter['options']:
                query_field = filter_filter['field_name'] + '__' + field_option['key']
                query_value = field_option['value']
                search_results = search_results.filter(**{query_field: query_value})
    else:
        search_results = Users.objects.filter()
        for filter_filter in search_details['filter_fields']:
            for field_option in filter_filter['options']:
                query_field = filter_filter['field_name'] + '__' + field_option['key']
                query_value = field_option['value']
                search_results = search_results.filter(**{query_field: query_value})
    search_results = search_results.values_list(*download_columns)

    rows = ([filtered_row for filtered_row in search_results.iterator()])

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'
    return response
