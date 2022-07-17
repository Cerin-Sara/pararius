from bs4 import BeautifulSoup
import requests
from csv import writer
base_url ="https://www.pararius.com/apartments/amsterdam/page-"
pages_url=[]

count=1
while count < 24:
    page_url = base_url + str(count)
    pages_url.append(page_url)

    for page in pages_url:
        response = requests.get(page)
        if response.status_code==200:
            soup = BeautifulSoup(response.text,'lxml')
    count = count + 1

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36"}
# url='https://www.pararius.com/apartments/amsterdam'
#page=requests.get(base_url, headers=headers)
card = soup.find_all('section',class_='search-list__item search-list__item--listing')
with open('pararius.csv','w',newline='') as f:
    thewriter=writer(f)
    header=['TITLE','LOCATION','PRICE PER MONTH','AREA IN m²','LINK','INTERIOR']
    thewriter.writerow(header)

    for list in card:
        title = list.find('a',class_='listing-detail-summary__title').text.replace('\n','')
        location = list.find('div',class_='listing-detail-summary__location').text.replace('\n','')
        price = list.find('div',class_='listing-detail-summary__price').text.replace('\n','')
        area = list.find('li',class_='illustrated-features__item illustrated-features__item--surface-area').text.replace('\n','')
        interior = list.find('li',class_='illustrated-features__item illustrated-features__item--surface-area').text.replace('\n','')
        links_list = soup.find_all('a',class_='listing-search-item__link listing-search-item__link--title')
        
        for link in links_list:
            if 'href' in link.attrs:
                each_link='https://www.pararius.com'+str(link.attrs['href'])
                
        price =price.replace('per month','')
        area =area.replace('m²','')
        price=price.replace('£','')
        info=[title,location,price,area,each_link,interior]
        thewriter.writerow(info)

all_links = set()

anchor = soup.find_all('a')
for link in anchor:
    if(link.get('href') != '#'):
        linkText="https://www.pararius.com"+link.get('href')
        all_links.add(link)
        #print(linkText)

