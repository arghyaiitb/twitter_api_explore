**POST /get_twitter_data/search_keyword/**

User can load the data from twitter using the following api point:

{  
"search_key" : "#BTC",   
"load_limit" : 99 ,   
"tweet_lang" : "en",   
"tweet_since" : 2018-01-28   
}

  
**search_key** is a string on which search needs to be made  
**load_limit** is the number of tweets to be uploaded (default 99)  
**tweet_lang** is the language in which tweets needs to be searched (default en)  
**tweeet_since** is the date from which the tweets needs to be extracted (YYYY-MM-DD, default 7 days old to current date)

**We are loading only original tweets and not retweets**

Response:

Status code 200  
{  
"users_added": 12,  
"tweets_added": 10  
}

_users_added_ is the number of new users added to the database  
_tweets_added_ is the number of new tweets added to the database


################################################################

**POST  /custom_search/plain_search/**

{  
"search_on": "tweets",  
"search_key": "BTC",  
"sort_by": ["-retweet_count","created_at"]  
}  

**search_on** options available: _"tweets", "user"_  
**search_key** search term  
**sort_by** feild names in an array, put _" - "_ to get descending sort on a field   

Response:

Status code 200  
Array of json object of the corresponding data
################################################################

**POST  /custom_search/group_search/**

{  
	"group_by": ["lang", "author_screen_name"],  
	"order_by": ["-count"],  
	"date_group": {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start_date" : "2018-01-20",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end_date" : "2018-01-30",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"bucket_by": "quarter"  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
}

**group_by** field names on which it needs to be grouped on  
**order_by** field names to sort, additionally _count_ can be used to sort on the counts, put _" - "_ to get descending sort on a field  
**date_group** to use date filter and date wise group  
_start_date_ the start date range(YYYY-MM-DD)  
_end_date_ the end date range(YYYY-MM-DD)  
_bucket_by_ to group by on buckets of day, options available _date, month, quarter, year_ (by default it will take date)

################################################################

**POST  /custom_search/filtered_search/**

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

**search_on** options _'tweets', 'user'_  
**filter_fields** array of filters on different field with the type of filter

Options available:

String field: _'startswith', 'endswith'_, etc all available in django  
Integer field: _'gte', 'gt'_, etc all available in django  
Array field: _'contains'_ , etc all available in django  

Response: 

Status code 200

{  
results_count : 10   
filtered_data: [USER/TWEET OBJECT ]    
}

################################################################

**POST  /csv_dump_data/csv_data_dump/**

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
		}],  
    "result_columns": ["retweet_count","id"]  
}  

**search_on** options _'tweets', 'user'_  
**filter_fields** array of filters on different field with the type of filter

Options available:

String field: _'startswith', 'endswith'_, etc all available in django  
Integer field: _'gte', 'gt'_, etc all available in django  
Array field: _'contains'_ , etc all available in django  

**result_columns** selective columns required for the dump
