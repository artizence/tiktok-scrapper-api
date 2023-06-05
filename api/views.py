from django.shortcuts import render, HttpResponse 
from .tiktok_scraper import *
import threading
from django.http import HttpResponse
import csv
from .models import profile as PROFILE_TABLE
from .rapid_api import *  
# Create your views here.
## we have to change the auth
import logging
import pandas as pd 
logger = logging.getLogger(__name__)

#api_counts = api_call.objects.get(id=1)


def object_rejistry(user):
    if True:
    #try:
        state,pid = profile_scrapper(user)
        if state==True:
            print(pid)
            uidcrawler = uid_call(user)
            followings = api_call_followings(uidcrawler)
            for x in followings:
                #t1 = threading.Thread(target=object_rejistry,args=(x,))
                #t1.start()
                object_rejistry(x)
            print(user,pid)
            return pid

        else:
            return -99,None # -99 means that no output
    else:
    #except:
        return -99,None

def crawler(request):
    df = pd.read_csv('base_index.csv')
    #df = ['thekelleyfamily']
    for x in df['username']:
        try:
            print(f"function startd for {x}")
            logger.warning(f"uid function called for {x}")
            uid_call(x)
        except Exception as e :
            logger.error(e)

    return HttpResponse("Working")

def home(request):
    return HttpResponse('Welcome to the Tiktok Scrapper')

def scrapper_function(request):
	
	for _ in range(100000):
		explore_scrapper()
		
	return HttpResponse('Scrapping has started')		 

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    writer.writerow( ['username','region','followers_count','following_count','likes','signature','profile_photo_url','videos','email','category'])
    
    users = profile.objects.all().values_list('username','region','followers_count','following_count','likes','signature','profile_photo_url','videos','email','category')
    for user in users:
        writer.writerow(user)

    return response

def export_follower_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="followers.csv"'

    writer = csv.writer(response)

    writer.writerow(['username','influencer','region','profile_photo','age','signature','follower_count'])
    #usernames = usernames
    #users = profile.objects.all().values_list('followers_count', 'likes', 'signature', 'link', 'profile_photo_url', 'category')
    users = Follower.objects.all().values_list('username','influencer','region','profile_photo','age','signature','follower_count')
    for user in users:
        writer.writerow(user)

    return response

def updater_hanlder(request):
    Profiles = PROFILE_TABLE.objects.filter(all_feild_status=False)
    
    for prof in Profiles:
        updater(request,prof)
    return HttpResponse("Working")

def updater(request,prof):
    # follower (4)
    if api_counter() <=300000:
        response = s.get(f'https://www.tiktok.com/@{prof.username}').text

        soup = BeautifulSoup(response,'lxml')
        ## bs4 sections
        main_div = soup.find('div',class_='tiktok-1hfe8ic-DivShareLayoutContentV2 enm41491')
        profile_div = main_div.find('div',class_='tiktok-1g04lal-DivShareLayoutHeader-StyledDivShareLayoutHeaderV2 enm41492')
        info_div =  [ x.strong.text  for x in   profile_div.find_all('div',class_='tiktok-1kd69nj-DivNumber e1457k4r1')]
        signature = profile_div.find('h2',class_='tiktok-1n8z9r7-H2ShareDesc e1457k4r3').text
        ##email and other things etc

        videos = profile_video_scrapper(main_div.find('div',class_='tiktok-1qb12g8-DivThreeColumnContainer eegew6e2'))
        likes_temp = info_div[2] 
        emails= extract_email(signature)
        ## updating the Profile 
        prof.likes = likes_temp 
        prof.emails = emails
        prof.videos = videos
        prof.all_feild_status = True
        prof.save()

        ## calling the follower etc
        t1 = Thread(target=api_call_followers,args=(prof.uid,prof))
        t1.start()
    else:
        return "MAX LIMIT REACHED"

    
#django.db.utils.IntegrityError: duplicate key value violates unique constraint "api_user_username_key"

    

if __name__ == "__main__":
    pass
