from bs4 import BeautifulSoup
import requests
import psycopg2
import random
from random import randint
import logging

from requests.api import delete
from requests.models import encode_multipart_formdata

# logging.captureWarnings(True)


db_name = input("Введите название базы данных: ")
db_user = input("Имя юзера: ")
db_password = input("Введите пароль от Базы Данных: ")


postgres = psycopg2.connect(
    dbname=f'{db_name}', 
    user=f'{db_user}', 
    password=f'{db_password}',
    host='localhost'
)

cursor = postgres.cursor()

cursor.execute("CREATE TABLE ch_books(id SERIAL PRIMARY KEY, name VARCHAR, author VARCHAR, year VARCHAR, price INT, image VARCHAR, many INT)")
postgres.commit()


def parse1(): # Парсим 20 книг Чынгыз Айтматова в бд

    try:
        print("wait...")
        print()
        URL='https://knijky.ru/authors/chingiz-aytmatov'
        HEADERS = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
        }

        response = requests.get(URL, headers=HEADERS, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='views-row')

        hrefs=[]
        book_name=[]

        for i in items:
            hrefs.append("https://knijky.ru" + i.find("span", class_="field-content").find("a").get("href"))
            book_name.append({
                "name": i.find("span", class_="field-content").get_text(strip=True),
                #"whatsin": i.find("div", class_="views-field views-field-body").find("span", class_="field-content").get_text(strip=True)
                })
        
        book_info=[]
        for i in hrefs:
            response = requests.get(i, headers=HEADERS, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')
            book_info.append({
                "author": soup.find("span", class_="left").find("a").get_text(strip=True),
                "year": (''.join(i for i in soup.find("div", class_="info_block col-lg-9 col-md-9 col-sm-9").get_text(strip=True) if i.isdigit())),
                "image": soup.find('div', class_='img_block col-lg-3 col-md-3 col-sm-3').find("img", class_="img-responsive").get("src"),
                "price": random.randrange(500, 1000, 50),
                "many": randint(3,10)
            })
            # print(soup.find('div', class_='img_block col-lg-3 col-md-3 col-sm-3'))

        for i in book_name:
            cursor.execute(f"INSERT INTO ai_books(name) VALUES('{i['name']}')")
            postgres.commit()

        id = 1
        for i in book_info:
            cursor.execute(f"UPDATE ai_books SET author = '{i['author']}', year = '{i['year']}', image = '{i['image']}', price = {i['price']}, many = {i['many']} WHERE id = {id}")
            id+=1
            postgres.commit()

        cursor.execute("UPDATE ai_books SET year = '1970' WHERE name = 'Рассказы'")
        postgres.commit()

        print("Successfull")
    except Exception as a:
        print(a)


def parse2():    # Парсим 100 ангоязычных книг
    try:
        print("wait...")
        print()
        URL='https://wordery.com/tarot-cards?viewBy=grid&resultsPerPage=20&page=1&leadTime[]=any'
        HEADERS = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
        }

        response = requests.get(URL, headers=HEADERS, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        itemss = soup.find_all("div", class_='c-book c-book--auto-portrait')

        book_info = []
        
        for i in itemss:
                book_info.append({
                    'image': i.find("img").get('data-lz-src'),
                    'name': (''.join(i for i in i.find("a", class_="c-book__title").get_text(strip=True) if i != "'")),
                    'author': i.find("span", class_="c-book__by").find("a").get_text(strip=True),
                    'year': randint(1990, 2015),
                    'price': random.randrange(500, 1000, 50),
                    "many": randint(3,10)

                    })
                print(i.find("img").get('data-lz-src'))
        
        for i in book_info:
                cursor.execute(f'''INSERT INTO en_books(name, image, author, year, price, many) VALUES('{i['name']}', '{i['image']}', '{i['author']}',{i['year']}, '{i['price']}', {i['many']})''')
                postgres.commit()
        print("Successfull")
        
    except Exception as e:
        print(e)
parse2()