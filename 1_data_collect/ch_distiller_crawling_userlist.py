import requests
from bs4 import BeautifulSoup
import pandas as pd

heavy_members = ['cascode', 'pbmichiganwolverine', 'scott_e', 'ctbeck11', 'soonershrink', 'stephanie_moreno','washeewashee', 'exelixi', 'thewhiskeyjug', 'joeparkerpoe', 'leeevolved', 'slainte-mhath', 'doneeb', 'islay_emissary', 'richard-moderndrinking']
user_urls = ['/profile/cascode', '/profile/pbmichiganwolverine', '/profile/scott_e', '/profile/ctbeck11', '/profile/soonershrink', '/profile/stephanie_moreno', '/profile/washeewashee', '/profile/exelixi', '/profile/thewhiskeyjug', '/profile/joeparkerpoe', '/profile/leeevolved', '/profile/slainte-mhath', '/profile/doneeb', '/profile/islay_emissary', '/profile/richard-moderndrinking']

for i in heavy_members:

    print(f'{i} 유저가 팔로잉한 유저')
    following_page = f'https://distiller.com/profile/{i}/following'
    following_page = requests.get(following_page)
    if following_page.status_code == 200:
        following_page_soup = BeautifulSoup(following_page.text, "lxml")
        following_num = following_page_soup.select_one("#main-content > div > div.center-column > div > div.desktop-profile-nav > div > div.user-statistics > div.statistic.following-link > a > span").get_text().split()[0]
        if int(following_num) == 0:
            pass
        elif int(following_num) <= 20:
            following_page_num = f'https://distiller.com/profile/{i}/following'
            following_page_num = requests.get(following_page_num)
            following_page_num_soup = BeautifulSoup(following_page_num.text, "lxml")

            user_url = following_page_num_soup.find_all("li", attrs={"class": "user-list-item"})  
            user_urls += [url.find('a')['href'] for url in user_url]
        else:
            last_page = following_page_soup.select_one("#main-content > div > div.center-column > div > div.personal-content > div.profile-list > ul > div > div > nav > span.last > a").attrs['href']
            n = int(last_page.split('=')[1])
            for j in range(1, n+1):
                following_page_num = f'https://distiller.com/profile/{i}/following?page={j}'
                following_page_num = requests.get(following_page_num)
                following_page_num_soup = BeautifulSoup(following_page_num.text, "lxml")
                
                user_url = following_page_num_soup.find_all("li", attrs={"class": "user-list-item"})  
                user_urls += [url.find('a')['href'] for url in user_url]
    else:
        print(f'{i}는 {following_page.status_code}에러 입니다.')

    print(f'{i} 유저의 팔로워 유저')
    followers_page = f'https://distiller.com/profile/{i}/followers'
    followers_page = requests.get(followers_page)
    if followers_page.status_code == 200:
        followers_page_soup = BeautifulSoup(followers_page.text, "lxml")
        followers_num = followers_page_soup.select_one("#main-content > div > div.center-column > div > div.desktop-profile-nav > div > div.user-statistics > div.statistic.followers-link > a > span").get_text().split()[0]
        if int(followers_num) == 0:
            pass
        elif int(followers_num) <= 20:
            followers_page_num = f'https://distiller.com/profile/{i}/followers'
            followers_page_num = requests.get(followers_page_num)
            followers_page_num_soup = BeautifulSoup(followers_page_num.text, "lxml")
            followers_names = followers_page_num_soup.find_all("div", attrs={"class": "name"})
            
            user_url = followers_page_num_soup.find_all("li", attrs={"class": "user-list-item"})  
            user_urls += [url.find('a')['href'] for url in user_url]
        else:
            last_page = followers_page_soup.select_one("#main-content > div > div.center-column > div > div.personal-content > div.profile-list > ul > div > div > nav > span.last > a").attrs['href']
            n = int(last_page.split('=')[1])
            for j in range(1, n+1):
                followers_page_num = f'https://distiller.com/profile/{i}/followers?page={j}'
                followers_page_num = requests.get(followers_page_num)
                followers_page_num_soup = BeautifulSoup(followers_page_num.text, "lxml")
                
                user_url = followers_page_num_soup.find_all("li", attrs={"class": "user-list-item"})  
                user_urls += [url.find('a')['href'] for url in user_url]
    else:
        print(f'{i}는 {followers_page.status_code}에러 입니다.')
        
    
print('heavy_members '+str(len(heavy_members))+'명')
user_urls = list(set(user_urls))
print('user_urls '+str(len(user_urls))+'명')

df = pd.DataFrame(user_urls, columns = ['user_url'])
df['user_name'] = [i.split('/')[-1] for i in df['user_url']]

df['user_id'] = df.index
df = df[['user_id','user_name','user_url']]

df.to_csv('C:/Users/codnj/python_vscode/user_table.csv',index=False)