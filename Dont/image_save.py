import requests
import psycopg2
import urllib.request

bd_password = '1234'#input("Введите пароль от Базы Данных: ")
bd_user = 'suluguni'#input("Имя юзера: ")

postgres = psycopg2.connect(
    dbname='mydb', 
    user=f'{bd_user}', 
    password=f'{bd_password}',
    host='localhost'
)

cursor = postgres.cursor()




cursor.execute("SELECT image, id FROM en_books")
images = cursor.fetchall()


# for i in images:
#     image = i[0]
#     id = i[1]
#     URL = image
#     img = urllib.request.urlopen(URL).read()
#     out = open(f"img.{id}-", "wb")
#     out.write(img)
#     out.close
# cursor.execute('SELECT image, name, author, year, price, many FROM ai_books')
# info = cursor.fetchall()

# for i in info:
#     image = i[0]
#     name = i[1]
#     author = i[2]
#     year = i[3]
#     price = i[4]
#     many = i[5]
#     cursor.execute(f"INSERT INTO ch_books(image, name, author, year, price, many) VALUES('{image}','{name}','{author}','{year}',{price},{many})")
#     postgres.commit()

# cursor.execute("SELECT id FROM en_books")
# id = cursor.fetchall()


# for i in id:
#     idd = 'images/img.' + f'{i[0]}' + '-'
#     cursor.execute(f"UPDATE en_books SET image = '{idd}' WHERE id = {i[0]}")
#     postgres.commit()


# cursor.execute("SELECT image, name FROM en_books")
# id = cursor.fetchall()


# for i in id:
#     idd = 'https://' + f'{i[0]}'
#     cursor.execute(f"UPDATE en_books SET image = '{idd}' WHERE name= '{i[1]}'")
#     postgres.commit()


cursor.execute('SELECT image, name, author, year, price, many FROM en_books')
info = cursor.fetchall()

for i in info:
    image = i[0]
    name = i[1]
    author = i[2]
    year = i[3]
    price = i[4]
    many = i[5]
    cursor.execute(f"INSERT INTO ch_books(image, name, author, year, price, many) VALUES('{image}','{name}','{author}','{year}',{price},{many})")
    postgres.commit()