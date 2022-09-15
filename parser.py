import json
from urllib import response
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import urllib.request
import os
import datetime


urls = []
ids = []
titles = []
descriptions = []
promotions = []
paramss = []
marks = []
users = []
contacts = []
locations = []
photoss = []
categorys = []
prices = []
conditions = []
negotiables = []
telephones = []
private_or_bussiness = []

cats = {
    "Ноутбуки": 80, 
    "Телефоны и аксессуары": 44,
    "Телевизоры": 75, 
    "Канцтовары / расходные материалы": 632, 
    "Мебель": 57,
    "Инструменты": 654, 
    "Детская мебель": 69,
    "Детские коляски": 68,
    "Детские автокресла": 538,
    "Антиквариат / коллекции": 53,
    "Книги / журналы": 49,
    "Спорт / отдых": 573,
    "Автозапчасти и аксессуары": 111,
    "Мотозапчасти и аксессуары": 1469,
    "Шины, диски и колёса": 270  
    }

#Жалгас поменяй переменную ниже на "Ноутбуки"(Или "Телефоны и аксессуары") и запусти скпипт командой  python new_parser.py в командной строке
curr_category = "Ноутбуки"

time.sleep(2)
rsp = requests.get("https://www.olx.kz/api/v1/offers/?category_id={}&limit=40".format(cats[curr_category]))
print(rsp.status_code)

soup = BeautifulSoup(rsp.text, 'html.parser')
site_json = json.loads(soup.text)
for element in site_json['data']:
    urls.append(element['url'])
    ids.append(element['id'])
    titles.append(element['title'])
    descriptions.append(element['description'].replace('<br />',''))
    promotions.append(element['promotion'])
    marks.append(element['params'][-1]['value']['label'])
    prices.append(element['params'][0]['value']['label'])
    conditions.append(element['params'][1]['value']['label'])
    negotiables.append("Да")
    users.append(element['user'])
    contacts.append(element['contact']['name'])
    locations.append(element['location']['city']['name'])
    link = ''
    count = 0
    for photo in element['photos']:
        name_file = ''
        count+=1
        name_file += "{}_{}.webp".format(ids[0],str(count))+'\n'
        link = photo['link'].replace(':443','').replace('{width}',str(photo['width'])).replace('{height}',str(photo['height']))
        path = element['url'].replace("https://www.olx.kz/d/obyavlenie/","").replace('.html','')
        isExist = os.path.exists(path)
        if not isExist:
            os.chdir('photos')
            os.makedirs(element['url'].replace("https://www.olx.kz/d/obyavlenie/","").replace('.html',''), exist_ok=True)
            os.chdir("..")
        else:
            continue
        name_dir = element['url'].replace("https://www.olx.kz/d/obyavlenie/","").replace('.html','')
        urllib.request.urlretrieve(link,os.getcwd()+"/photos/"+name_dir+"/file_{}.webp".format(str(count)))
        print("{}_{}.webp is succesfully downloaded at {}".format(element['url'].replace("https://www.olx.kz/d/obyavlenie/","").replace('.html',''),str(count),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    
    photoss.append(name_file)
    categorys.append(curr_category)
    telephones.append(element['user']['name'])
    private_or_bussiness.append('Частный')
df = pd.DataFrame(list(zip(ids,marks,titles,categorys,photoss,descriptions,prices,negotiables,private_or_bussiness,conditions,locations,contacts,telephones,urls)),
columns=['ID товара', 'Марка товара', 'Название', 'Категория', 'Ссылки на фото', 'Описание товара', 'Цена', 'Договорная', 'Частный или бизнес', 'Состояние', 'Местоположение', 'Имя продавца', 'Телефон','Ссылка на OLX'])

df.to_excel("{}_demo_results.xlsx".format(curr_category))

