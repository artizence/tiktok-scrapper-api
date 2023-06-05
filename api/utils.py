import re
import numpy as np 
from .models import *
import time 
import logging
from django.db.utils import OperationalError
import pandas as pd 
logger = logging.getLogger(__name__)

def digit_extractor(text):
    n = re.findall(r'\d+', text)
    return int(n[0])

def db_writer(username,region,uid,signature,followers_count,email,following_count,profile_photo_url):
    with open('database.txt','a',encoding='UTF-8') as f:
        #RAM==BHAGWAN
        text = [username,str(region),str(uid),str(signature),str(followers_count),str(email),str(following_count),str(profile_photo_url)]
        text = ' RAM==BHAGWAN '.join(text)
        f.write(text)
    
### EXTACT LIKK_EMAIL
def extract_email(text):
    """
    Extract Links
    """
    EMAIL =[]
    [EMAIL.append(x) for x in re.findall(r'[\w\.-]+@[\w\.-]+', text)] 
    return np.unique(EMAIL)

def infleuncer_register(unique_id,signature,region,uid,follower_count,following_count,profile_photo):
    try: 
        emails= extract_email(signature)
    except:
        logger.warning('email is not added')
        emails =''
    
    #if True:
    try:
        ##username bug that can appear
        #if True:
        try: 
            #pass   
            userid = User.objects.create(username=unique_id)
        #else:
        except SyntaxError: #OperationalError:
            #if True:
            try:
                    logger.warning('database is locked at ) is called')
                    userid = User.objects.create(username=unique_id)
                    logger.info('database is locked solved for {userid} , object created')
            except Exception as e:
                    logger.error(str(e))
                    username_logs(unique_id)
                    return "Error occured"
            #else:    
        except Exception as e:
                logger.error(str(e))
                username_logs(unique_id)
                return "Error occured"
        ## userid
        ''' 
        db_writer(username=unique_id,region=region,uid=uid,
                  signature=signature,followers_count=follower_count,
                  following_count=following_count,email=str(emails),profile_photo_url=profile_photo)

        ''' 
        pid=profile.objects.create(user=userid,username=unique_id,signature=signature,
            region=region,uid=uid,followers_count=follower_count,email=emails,following_count=following_count,
            profile_photo_url=profile_photo)
        
        print(pid)
        return pid
        
    except OperationalError:
        logger.info('database is locked')
        try:
            print('we need to sleep for some time ')
            time.sleep(60*5)
            pid=profile.objects.create(user=userid,signature=signature,email=emails,
            region=region,uid=uid,followers_count=follower_count,following_count=following_count,
            profile_photo_url=profile_photo)

            logger.info(f"profile created for {pid}")
            print(pid)
            return pid
        except OperationalError :
            try:
                time.sleep(60*5)
                pid=profile.objects.create(user=userid,signature=signature,email=emails,
                region=region,uid=uid,followers_count=follower_count,following_count=following_count,
                profile_photo_url=profile_photo)

                logger.info(f"profile created for {pid}")
                print(pid)
            except:
                logger.error(str(e))
                username_logs(unique_id)
                return "Error occured"
        #else:
    
    except Exception as e:
        print(e)
        logger.error(str(e))
        username_logs(unique_id)
        return "Error occured"
    
def error_log(e):
    with open('../error.txt','a') as f:
        f.writelines([e]) 

def username_logs(username):
    # have log of username which are not added due to a error
    with open('../error.txt','a') as f:
        f.writelines([username]) 


def api_counter():
    s=0
    with open('counter.txt','r') as f:
        c=  int(f.read())   
        s=c    
        #f.write(str(c+1))
    with open('counter.txt','w') as f:
        c = f.write(str(c+1))
    
    return int(s+1)

def username_counter(username):

    with open('username.txt','a') as f:
        c = f.write(str(f'{username} ,'))    
    return username


if __name__ == "__main__":
    #infleuncer_register('aksaht','achive the goal','IND','12042035','89423','123124','artizence.com/images/lalaji.png')
    print(api_counter())

