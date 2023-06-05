## followers info extraction
# https://rapidapi.com/Sonjik/api/tokapi-mobile-version
# https://rapidapi.com/tikwm-tikwm-default/api/tiktok-scraper7/details

import requests
from pprint import pprint
from django.db.utils import OperationalError
import json
from .models import *
from threading  import Thread
import time 
from multiprocessing.pool import ThreadPool as Pool
from .utils import *
import logging
from .models import Follower 
logger = logging.getLogger(__name__)

## object creation in api call

#api_counts = ''  #
#api_counts = api_call.objects.get(id=1)

querystring = {"count":"200"}

headers = {
    'X-RapidAPI-Key': '53c68747bcmsh8a9091caacdd8fep163f68jsn6bc23acbd6ea',
    'X-RapidAPI-Host': 'tokapi-mobile-version.p.rapidapi.com'
}
    


## ek function banao joh pahle se existing uid and usernames pe api call na hone hai

def uid_call(user):
	"""
	default region USA
	"""
	try:
		username_counter(user)
	except Exception as e:
		print(e)
	if len(profile.objects.filter(username=user))>0:
		print((profile.objects.filter(username=user)))
		print("profile present")	
		return "Data Allready Present"

	if api_counter() <=3*1000000 :
		url = f"https://tokapi-mobile-version.p.rapidapi.com/v1/user/@{user}" # not return the region

	else:
		print("max limit reached")
		return "MAX LIMIT REACHED"
	
	#if True:
	try:
		response = requests.get(url, headers=headers).json()['user']#['share_info']
		userid = response['uid']
		signature = response['signature']
		category = response['category']
		followers_count = response['follower_count']
		following_count = response['following_count']
		image = response['avatar_168x168']['url_list'][0]
		#if True:
		try:
				username_counter(user)
				pid = infleuncer_register(user,signature,region='US',uid=userid,
				follower_count=followers_count,following_count=following_count,
				profile_photo=image 
				)
				if pid =="Error occured":
					logger.error(f"user not created for {userid}")
					return "Error occured"
				api_call_followings(userid)
		#else:
		except OperationalError:
				logger.error(f" Error occured at  user created for {userid}")		
		except Exception as e :
			print(e)
	#else:
	except Exception as e:
		logger.error(f"{e}")
		print('exception')
		print(e)
		return "Error occured"
	return pid
	


	
def api_call_followings(uid):
	#print(api_counter(),type(api_counter()))
	
	if api_counter() <=3*1000000 :
		url = f"https://tokapi-mobile-version.p.rapidapi.com/v1/user/{uid}/followings"
		querystring = {"count":"200"}
		response = requests.get(url, headers=headers, params=querystring).json()

	else:
		print("max limit reached")
		return "MAX LIMIT REACHED"
	
	try:
		if response['status_code']==3002060:
			print('not allowd')
			return 'not allowed'
		#if True:
		try:
			for x in range(0,len(response['followings'])):
				state = response['followings'][x]
				#if True:
				if response['followings'][x]['follower_count'] >= 5000 and state['region'] == 'US':
					## object creation and calling the uid_call  
					#if True:
						#if user already exist in db?
					if len(profile.objects.filter(uid=state['uid']))>0:
						print(f"{uid} allready present ")
						return "Data Allready Present"
					
					try: 
						profile_photo_url=state['avatar_168x168']['url_list'][0]
						try:
							username_counter(state['unique_id'])
						except Exception as e:
							print(e)
						## influencer register
						pid = infleuncer_register(unique_id=state['unique_id'],
							signature=state['signature'],region=state['region'],uid=state['uid'],
							follower_count=state['follower_count'],following_count=state['following_count'],
							profile_photo=profile_photo_url)
						print(pid)
						## adding multi polling
						x = Thread(target=api_call_followings,args=(state['uid'],))
						x.start()
						#x.join()
						## join to make sure the threading is not infinite
					#else:
					except OperationalError:
						time.sleep(60*5)
						x = Thread(target=api_call_followings,args=(state['uid'],))
						x.start()
					
					except Exception as e:
						try:
							time.sleep(400*1.8)
							x = Thread(target=api_call_followings,args=(state['uid'],))
							x.start()
						except:
							print(e)
							logger.warning(e)
		#else:		
		except Exception as e:
			logger.warning(e)

	except Exception as e:
		print(e)
	return 'working'	


## this will be called during the time of update of database
def api_call_followers(uid,INFLUENCER_OBJ):

	if api_counter() <=3*1000000 : 
		url = f"https://tokapi-mobile-version.p.rapidapi.com/v1/user/{uid}/followers"
		response = requests.get(url, headers=headers, params=querystring).json()

	else:
		print('MAX LIMIT API CALL REACHED')
		return "MAX LIMIT REACHED"
	
	
	for follower in response['followers']:
		##after the api call we will added the data in database
		profile_photo = (follower['avatar_larger']['url_list'][0])
		region = follower['region']
		username = follower['unique_id'] # it's username
		signature = follower['signature']
		follower_count = follower['follower_count']
		following_count=follower['following_count']
		fuid = follower['uid']
		## create follower with uid of the influencer
		try:
			fid = Follower.objects.create(uid=fuid,username=username,
				influencer=INFLUENCER_OBJ,region=region,profile_photo=profile_photo,
				signature= signature,email=extract_email(signature),
				follower_count= follower_count
				)
			logger.info(f"Follower object created {fid} for {uid} ")
		
		except Exception as e :
			print(e)
			logger.error(f"Follower object created {fid} for {uid} ")

		
		if follower_count>=5000 and region=='US':
			pid = infleuncer_register(unique_id=username,
				signature= signature ,region= region,uid=fuid,
				follower_count= follower_count,following_count=following_count,
				profile_photo=profile_photo)

			print(pid)
			## adding multi polling
			x = Thread(target=api_call_followings,args=(fuid,))
			x.start()
			#x.join()
			
		#print('know something good') 
 
if __name__ == '__main__':
	api_call_followings(6546356850533602319)





## like ki liye scrapper 
## video ke liye scrapper
## comment ke liye scrapper

