import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import threading
from .models import profile as Profile_db , User
from .utils import *
from requests.auth import HTTPProxyAuth

#https://www.tiktok.com/
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


username ,following, followers, likes  , bio,videos,link = [],[],[],[],[],[],[]
lines = ['176.103.238.51:12323:14abbf240bd54:2268300b2b', '85.254.83.91:12323:14abbf240bd54:2268300b2b', '109.205.215.183:12323:14abbf240bd54:2268300b2b', '176.103.228.253:12323:14abbf240bd54:2268300b2b', '31.133.85.14:12323:14abbf240bd54:2268300b2b', '178.253.215.54:12323:14abbf240bd54:2268300b2b', '176.103.237.255:12323:14abbf240bd54:2268300b2b', '85.254.80.134:12323:14abbf240bd54:2268300b2b', '109.205.215.249:12323:14abbf240bd54:2268300b2b', '176.103.230.219:12323:14abbf240bd54:2268300b2b', '31.133.86.25:12323:14abbf240bd54:2268300b2b', '178.253.215.101:12323:14abbf240bd54:2268300b2b', '176.103.238.113:12323:14abbf240bd54:2268300b2b', '85.254.82.193:12323:14abbf240bd54:2268300b2b', '109.205.215.130:12323:14abbf240bd54:2268300b2b', '176.103.231.32:12323:14abbf240bd54:2268300b2b', '31.133.87.157:12323:14abbf240bd54:2268300b2b', '178.253.215.203:12323:14abbf240bd54:2268300b2b', '176.103.237.64:12323:14abbf240bd54:2268300b2b', '85.254.81.211:12323:14abbf240bd54:2268300b2b', '109.205.215.67:12323:14abbf240bd54:2268300b2b', '176.103.228.226:12323:14abbf240bd54:2268300b2b', '31.133.84.253:12323:14abbf240bd54:2268300b2b', '178.253.215.91:12323:14abbf240bd54:2268300b2b', '176.103.237.32:12323:14abbf240bd54:2268300b2b', '85.254.83.252:12323:14abbf240bd54:2268300b2b', '109.205.215.59:12323:14abbf240bd54:2268300b2b', '176.103.231.80:12323:14abbf240bd54:2268300b2b', '31.133.85.96:12323:14abbf240bd54:2268300b2b', '178.253.215.109:12323:14abbf240bd54:2268300b2b', '176.103.236.194:12323:14abbf240bd54:2268300b2b', '85.254.81.103:12323:14abbf240bd54:2268300b2b', '109.205.215.27:12323:14abbf240bd54:2268300b2b', '176.103.228.117:12323:14abbf240bd54:2268300b2b', '31.133.86.142:12323:14abbf240bd54:2268300b2b', '178.253.215.47:12323:14abbf240bd54:2268300b2b', '176.103.238.8:12323:14abbf240bd54:2268300b2b', '85.254.82.169:12323:14abbf240bd54:2268300b2b', '109.205.215.97:12323:14abbf240bd54:2268300b2b', '176.103.229.92:12323:14abbf240bd54:2268300b2b', '31.133.86.246:12323:14abbf240bd54:2268300b2b', '178.253.215.236:12323:14abbf240bd54:2268300b2b', '176.103.239.98:12323:14abbf240bd54:2268300b2b', '85.254.81.30:12323:14abbf240bd54:2268300b2b', '109.205.215.71:12323:14abbf240bd54:2268300b2b', '176.103.230.152:12323:14abbf240bd54:2268300b2b', '31.133.85.92:12323:14abbf240bd54:2268300b2b', '178.253.215.206:12323:14abbf240bd54:2268300b2b', '176.103.236.101:12323:14abbf240bd54:2268300b2b', '85.254.83.43:12323:14abbf240bd54:2268300b2b', '109.205.215.65:12323:14abbf240bd54:2268300b2b', '176.103.230.50:12323:14abbf240bd54:2268300b2b', '31.133.86.221:12323:14abbf240bd54:2268300b2b', '178.253.215.42:12323:14abbf240bd54:2268300b2b', '176.103.236.51:12323:14abbf240bd54:2268300b2b', '85.254.82.24:12323:14abbf240bd54:2268300b2b', '109.205.215.113:12323:14abbf240bd54:2268300b2b', '176.103.228.81:12323:14abbf240bd54:2268300b2b', '31.133.85.77:12323:14abbf240bd54:2268300b2b', '178.253.215.133:12323:14abbf240bd54:2268300b2b', '176.103.237.164:12323:14abbf240bd54:2268300b2b', '85.254.81.110:12323:14abbf240bd54:2268300b2b', '109.205.215.198:12323:14abbf240bd54:2268300b2b', '176.103.230.133:12323:14abbf240bd54:2268300b2b', '31.133.86.71:12323:14abbf240bd54:2268300b2b', '178.253.215.214:12323:14abbf240bd54:2268300b2b', '176.103.239.13:12323:14abbf240bd54:2268300b2b', '85.254.80.129:12323:14abbf240bd54:2268300b2b', '176.103.230.166:12323:14abbf240bd54:2268300b2b', '31.133.86.242:12323:14abbf240bd54:2268300b2b', '178.253.215.100:12323:14abbf240bd54:2268300b2b', '176.103.236.26:12323:14abbf240bd54:2268300b2b', '85.254.82.241:12323:14abbf240bd54:2268300b2b', '176.103.229.29:12323:14abbf240bd54:2268300b2b', '31.133.84.164:12323:14abbf240bd54:2268300b2b', '178.253.215.202:12323:14abbf240bd54:2268300b2b', '176.103.236.27:12323:14abbf240bd54:2268300b2b', '85.254.80.201:12323:14abbf240bd54:2268300b2b', '176.103.228.167:12323:14abbf240bd54:2268300b2b', '31.133.84.9:12323:14abbf240bd54:2268300b2b', '178.253.215.229:12323:14abbf240bd54:2268300b2b', '176.103.236.83:12323:14abbf240bd54:2268300b2b', '85.254.82.99:12323:14abbf240bd54:2268300b2b', '176.103.228.162:12323:14abbf240bd54:2268300b2b', '31.133.85.12:12323:14abbf240bd54:2268300b2b', '178.253.215.234:12323:14abbf240bd54:2268300b2b', '176.103.239.240:12323:14abbf240bd54:2268300b2b', '85.254.83.10:12323:14abbf240bd54:2268300b2b', '176.103.230.65:12323:14abbf240bd54:2268300b2b', '31.133.87.178:12323:14abbf240bd54:2268300b2b', '178.253.215.48:12323:14abbf240bd54:2268300b2b', '176.103.236.209:12323:14abbf240bd54:2268300b2b', '85.254.83.135:12323:14abbf240bd54:2268300b2b', '176.103.230.254:12323:14abbf240bd54:2268300b2b', '31.133.86.100:12323:14abbf240bd54:2268300b2b', '178.253.215.108:12323:14abbf240bd54:2268300b2b', '176.103.237.60:12323:14abbf240bd54:2268300b2b', '85.254.82.212:12323:14abbf240bd54:2268300b2b', '176.103.231.92:12323:14abbf240bd54:2268300b2b', '31.133.85.30:12323:14abbf240bd54:2268300b2b']

s = requests.Session()

def hompage_scrapping():
    for _ in range(2000):
        #max_attemp = 10        
        source = s.get(f'https://www.tiktok.com/foryou').text
        soup = BeautifulSoup(source,'lxml')
        #main div
        #parent = soup.find('div',class_='app')
        main_div = soup.find('div',class_ = 'tiktok-ywuvyb-DivBodyContainer e1irlpdw0')
        
        video_div = main_div.find('div',class_='tiktok-b4uwjw-DivOneColumnContainer e108hwin0')

        
        parent= video_div.find_all('div',class_ = "tiktok-1nncbiz-DivItemContainer etvrc4k0")
        
        ##main
        print(len(parent))
        for div in parent:
            print(div.a['href'])


    #videos_div = main_div.find_all('div',class_='tiktok-1nncbiz-DivItemContainer etvrc4k0')
    
def explore_scrapper():
    if True:
        ''' 
        indexs = int(np.random.uniform(low=0, high=99, size=(1,))[0])
        line = lines[indexs]
        index = line.split(':')
        proxies = {"http": f"{index[0]}:{index[1]}"}
        auth = HTTPProxyAuth(f"{index[2]}", f"{index[3]}")

        '''
        #max_attemp = 10
        source = s.get(f'https://www.tiktok.com/explore?lang=en').text
        soup = BeautifulSoup(source,'lxml')
        #main div
        #parent = soup.find('div',class_='app')
        main_div = soup.find('div',class_ = 'tiktok-1hfe8ic-DivShareLayoutContentV2 enm41491')
        
        video_div = main_div.find('div',class_='tiktok-1qb12g8-DivThreeColumnContainer eegew6e2')

        parent= video_div.find_all('div',class_ = "tiktok-x6y88p-DivItemContainerV2 e19c29qe7")
        

        ##main
        for div in parent:
            user = div.a['href'].split('@')[-1].split('/')[0]
            profile_scrapper(user)



def profile_video_scrapper(videos_div):
    #print(videos_div)
    try:
        main = videos_div.find('div',class_='tiktok-yvmafn-DivVideoFeedV2 ecyq5ls0')
        divs = main.find_all('div',class_="tiktok-x6y88p-DivItemContainerV2 e19c29qe8")
        video = ""
        for x in divs:
            video = video + ',' +' ' + x.a['href']
        return video
    except Exception as e:
        print(e)
        print(videos_div)
        return "NO VIDEO"

## it will be used for likes , videos , comment etc
def profile_scrapper(username):
    if True:
    #try:
        response = s.get(f'https://www.tiktok.com/@{username}',headers=headers).text
        soup = BeautifulSoup(response,'lxml')
        
        main_div = soup.find('div',class_='tiktok-1hfe8ic-DivShareLayoutContentV2 enm41491')
        profile_div = main_div.find('div',class_='tiktok-1g04lal-DivShareLayoutHeader-StyledDivShareLayoutHeaderV2 enm41492')

        info_div =  [ x.strong.text  for x in   profile_div.find_all('div',class_='tiktok-1kd69nj-DivNumber e1457k4r1')]
        followers_temp = info_div[1]

        ## influencer checkers
        if 'M' in followers_temp or 'K' in followers_temp or digit_extractor(followers_temp) >=5000:
            likes_temp = info_div[2]
            following_temp = info_div[0]
        
            profile_photo_url = profile_div.find('div',class_='tiktok-uha12h-DivContainer e1vl87hj1').img['src'] ## image deliver
            signature = profile_div.find('h2',class_='tiktok-1n8z9r7-H2ShareDesc e1457k4r3').text
            emails= extract_email(signature)
            
            ##video
            #videos_temp = profile_video_scrapper(main_div.find('div',class_='tiktok-1qb12g8-DivThreeColumnContainer eegew6e2'))
            if True:
            #try:
                pass
                #infleuncer_register(unique_id=username,signature=signature
                #                    bio=bio)
            else:
            #except:
                pass
        else:
        #xcept:
            print("followers",followers_temp)
            pass
        return True,None 
    else:
    #except Exception as e:
        print("ERROR")
        print(e)

        return False,None




if __name__ == "__main__":

    for _ in range(100000):
        t1 = threading.Thread(target=explore_scrapper)
        t1.start()

            

