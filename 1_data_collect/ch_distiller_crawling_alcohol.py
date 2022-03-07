import requests
from bs4 import BeautifulSoup
import pandas as pd
alcohol_list = pd.read_csv('C:/Users/codnj/python_vscode/alcohol_list.csv')

# input:
# alcohol_id, alcohol_type, alcohol_url

# output:
# alcohol_id, alcohol_type, origin, alcohol_age, alcohol_cost, ABV, tasting_note, tasting_score, flavor_profile, flavor_type_rating, Field
# crawling : 
# origin, alcohol_age, alcohol_cost, ABV, tasting_note, tasting_score, flavor_profile, flavor_type_rating
# if : alcohol_age, ABV, tasting_note, tasting_score, flavor_profile

cols = ['alcohol_id', 'alcohol_type', 'origin', 'alcohol_age', 'alcohol_cost', 'ABV', 'tasting_note', 'tasting_score', 'flavor_profile', 'flavor_type_rating']
alcohol_tb = pd.DataFrame(data=[],  columns=cols)

for i in range(len(alcohol_list)):
    url = alcohol_list['alcohol_url'][i]
    print(url)
    
    alcohol_page = f"https://distiller.com{url}"
    alcohol_page = requests.get(alcohol_page)
    
    if alcohol_page.status_code == 200:
        alcohol_page_soup = BeautifulSoup(alcohol_page.text, "lxml")

        origin = alcohol_page_soup.find("h2", attrs={"class": "ultra-mini-headline location middleweight"}).get_text()  
        origin = origin.strip()
        alcohol_cost = str(alcohol_page_soup.find_all("div", attrs={"class": "spirit-cost"}))[30:31]
        
        if alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.spirit-show__description-container > div.other-details-container > ul > div > li.detail.age > div.value") != None:
            alcohol_age = alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.spirit-show__description-container > div.other-details-container > ul > div > li.detail.age > div.value").get_text()  
        else:
            alcohol_age = None
        if alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.spirit-show__description-container > div.other-details-container > ul > div > li.detail.abv > div.value") != None: 
            ABV = alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.spirit-show__description-container > div.other-details-container > ul > div > li.detail.abv > div.value").get_text()  
        else:
            ABV = None
        if alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.details-module.spirit-show__tasting-notes.screened > div.content > p") != None:
            tasting_note = alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.details-module.spirit-show__tasting-notes.screened > div.content > p").get_text()  
        else:
            tasting_note = None
        if alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.details-module.spirit-show__tasting-notes.screened > div.content > div.distiller-score > span") !=None:
            tasting_score = alcohol_page_soup.select_one("#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.details-module.spirit-show__tasting-notes.screened > div.content > div.distiller-score > span").get_text()  
        else:
            tasting_score = None   
        if alcohol_page_soup.find("canvas",attrs={"class":"js-flavor-profile-chart"}) != None:
            flavor_profile = alcohol_page_soup.find("canvas",attrs={"class":"js-flavor-profile-chart"})['data-flavors']
        else:
            flavor_profile = None
        if alcohol_page_soup.select_one('#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.stats-container > div > div > div > div > div.rating-display__value.average-rating > span') != None:
            flavor_type_rating = alcohol_page_soup.select_one('#main-content > div > div.spirit-show.center-column.js-carousel.whiskey-content > div.primary-content > div.tabs > div > div > div.stats-container > div > div > div > div > div.rating-display__value.average-rating > span').get_text()  
        else:
            flavor_type_rating = None
    else:
        print(f'{url}는 {alcohol_page.status_code}에러 입니다.')
    
    new_row = pd.DataFrame({'alcohol_id':[alcohol_list['alcohol_id'][i]], 'alcohol_type':[alcohol_list['alcohol_type'][i]], 
               'origin':[origin], 'alcohol_age':[alcohol_age], 'alcohol_cost':[alcohol_cost], 
               'ABV':[ABV], 'tasting_note':[tasting_note], 'tasting_score':[tasting_score], 
               'flavor_profile':[flavor_profile], 'flavor_type_rating':[flavor_type_rating]})
    alcohol_tb = pd.concat([alcohol_tb,new_row], axis=0)
         

alcohol_tb.to_csv('C:/Users/codnj/python_vscode/alcohol_tb.csv',index=False)