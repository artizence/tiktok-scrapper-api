import requests
from pprint import pprint
url = "https://tokapi-mobile-version.p.rapidapi.com/v1/user/@nike"

headers = {
    'X-RapidAPI-Key': '53c68747bcmsh8a9091caacdd8fep163f68jsn6bc23acbd6ea',
    'X-RapidAPI-Host': 'tokapi-mobile-version.p.rapidapi.com'
}
   

response = requests.get(url, headers=headers)

## we will do one thing is that we will add the now scrapped data to the db
#api call 
'''
# profile pic
# category
# follower_count
# following_count
# 'nickname'
# 'uid'
# signature
'''

pprint(response.json())