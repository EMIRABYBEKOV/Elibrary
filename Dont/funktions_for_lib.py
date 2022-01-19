import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

bd_password = input("Password: ")
bd_user = input("Username: ")
bd_name = input("Databasename: ")
postgres = psycopg2.connect(
    dbname=f'{bd_name}', 
    user=f'{bd_user}', 
    password=f'{bd_password}',
    host='localhost'
)

cursor = postgres.cursor()


def check(mail, password, bd):
    cursor.execute(f"SELECT mail FROM {bd}")
    data = cursor.fetchall()
    for i in data:
        if i[0] == mail:
            cursor.execute(f"SELECT password FROM {bd} WHERE mail = '{mail}'")
            data1 = cursor.fetchall()
            for i in data1:
                if i[0] == password:
                    return True
                
    else:
        return False


def create(password, mail, bd):
    cursor.execute(f"INSERT INTO {bd}(password, mail) VALUES('{password}', '{mail}')")
    postgres.commit()


def send_mail(number, mail):
    try:
        fromaddr = "emir.qwerty9@gmail.com"
        mypass ='retyuuretyuu'
        toaddr = mail
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Отправитель: ELIBRARY"
        body = f"Введите данный код: {number}"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, mypass)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except Exception as e:
        print(e)


def verification():
    account = int(input("IF you are librarian write - 1.\nIF you are reader write - 2\n==>  "))
    if account == 1:
        account = 'librarian_acc'
    elif account == 2:
        account = 'reader_acc'
    choose = int(input("Create account - 1\nCheck - 2\n==>  "))
    if choose == 2:
        name = input("Введите имя аккаунта: ")
        password = input("Введите пароль от аккаунта: ")
        aut = check(name, password, account)
        if aut is True:
            print("Succesfull")
        else:
            print("Name or password is incorrect")
    elif choose == 1:
        name = input("Name for account: ")
        password = input("Password for account: ")
        global mail
        mail = input("Your mail: ")
        number = randint(1000, 10000)
        send_mail(number, mail)
        verif = int(input("Check your mail and write there your code\n==> "))
        if verif == number:
            create(name, password, mail, account)
            print("Account created")
        else:
            tr = 3
            while tr != 0:
                print(f"It was wrong. Try again you have {tr} attemts")
                verif = int(input("Check your mail and write there your code\n==> "))
                if verif == number:
                    create(name, password, mail, account)
                    print("Account created")
                    break
                else:
                    tr-=1


#########################################################################################################


def find_book():
    while True:
        choose = int(input("Find with name - 1.\nFind with author name - 2.\nIF you wont find with year - 3.\nIF you wont back to the menu write 4\n==>  "))
        if choose == 1:
            choose = 'name'
            column = input("Write book name:\n==>  ")
        elif choose == 2:
            choose = 'author'
            column = input("Write books author name:\n==>  ")
        elif choose == 3:
            choose = 'year'
            column = input("Write books year:\n==>  ")
        elif choose == 4:
            break
        else:
            print("i don't now it.")
        try:
            cursor.execute(f"SELECT * from books WHERE {choose} = '{column}'")
            data = cursor.fetchall()
            for i in data:
                print()
                print("Name: ", i[1])
                print("Author: ", i[2])
                print("year: ", i[3])
                print()
        except Exception as e:
             print(e)
             continue
def my_book_reader():
    cursor.execute(f"SELECT * FROM mybooks WHERE id = {sid}")
    data = cursor.fetchall()
    for i in data:
        print()
        print("Name: ", i[1])
        print("Author: ", i[2])
        print("Year: ", i[3])
        print()


def add_to_favorite_reader():
    name = input('Write book name:\n==>  ')
    try:
        cursor.execute(f"SELECT * FROM books LEFT OUTER JOIN f_books ON books.name = f_books.name WHERE books.name = '{name}' AND id = {sid}")
        i = cursor.fetchone()
        id = i[0]
        name = i[1]
        author = i[2]
        year = i[3]
        cursor.execute(f"INSERT INTO f_books(id, name, author, year) VALUES({sid},'{name}','{author}','{year}')")
        postgres.commit()
    except:
        print("Ther aren't books like this.")


def show_favorite_books_reader():
    cursor.execute(f"SELECT * FROM f_books WHERE id = {sid}")
    data = cursor.fetchall()
    for i in data:
        print()
        print("Name: ", i[1])
        print("Author: ", i[2])
        print("Year: ", i[3])
        print()
    
def show_wallet_reader():
    cursor.execute(f"SELECT wallet FROM reader_acc WHERE id = {sid}")
    data = cursor.fetchone()
    print(f"You have {data[0]} dollars")

def take_book_reader():
    choose = int(input("If you wont to buy a book write - 1.\n IF you wont to lend a book write - 2.\n==>  "))
    if choose == 1:
        choose = int(input("Find with name - 1.\nFind with author name - 2.\nIF you wont find with year - 3.\nIF you wont back to the menu write 4\n==>  "))
        if choose == 1:
            choose = 'name'
            column = input("Write book name:\n==>  ")
        elif choose == 2:
            choose = 'author'
            column = input("Write books author name:\n==>  ")
        elif choose == 3:
            choose = 'year'
            column = input("Write books year:\n==>  ")
        else:
            print("i don't now it.")

        try:
            cursor.execute(f"SELECT * from books WHERE {choose} = '{column}'")
            i = cursor.fetchone()
            print(f"Name is {i[1]}")
            print(f"Price is {i[4]}")
            choose = int(input("If you wont to buy it write - 1.\nIf you don't wont to buy it write 2.\n==>  "))
            if choose == 1:
                name = i[1]
                author = i[2]
                year = i[3]
                cursor.execute(f"INSERT INTO mybooks(id, name, author, year) VALUES({sid},'{name}','{author}','{year}')")
                postgres.commit()
                cursor.execute(f"UPDATE reader_acc SET wallet = wallet::integer - {sid[4]} ")
                postgres.commit()
                cursor.execute(f"INSERT INTO history(id, book, spend) VALUES({sid},'{name}',{i[4]})")
                postgres.commit()
                print("Succesful")
            elif choose == 2:
                print("Back to menu")
            else:
                print("i don't now it")

        except Exception as e:
            print(e)
            print("i don't find this book")

    elif choose == 2:
        name = input("write name for book, wich do you want to lend.\n==>  ")
        date = input("Write date:\n==>")
        cursor.execute(f"INSERT INTO lend_book(id, name, date) VALUES({sid}, '{name}', '{date}')")
        postgres.commit()
        print("Succeful")


def back_lend_book_reader():
    name = input("write name for book, wich do you want to delete from lend_book .\n==>  ")
    cursor.execute(f"DELETE FROM lend_book WHERE name = '{name}' AND id = {sid}")
    postgres.commit()
    print("Succeful")




#########################################################################################################





def show_readers():
    cursor.execute("SELECT name FROM reader_acc")
    names = cursor.fetchall()
    for i in names:
        print(i[0])

def show_lend_book():
    cursor.execute("SELECT name FROM lend_book")
    names = cursor.fetchall()
    for i in names:
        print(i[0])

def show_history():
    cursor.execute("SELECT * FROM history INNER JOIN reader_acc ON history.id = reader_acc.id")
    data = cursor.fetchall()
    for i in data:
        print(i)
