from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import  ScreenManager
from kivy.uix.screenmanager import WipeTransition, NoTransition,SlideTransition
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton,MDTextButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import  MDList, OneLineListItem, ThreeLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import TwoLineListItem
from kivy.metrics import sp
from kivy.uix.label import Label
from lib_func import *

#####ANOTHER BOOK#######

import psycopg2
from random import randint

db_name = input("Databasename: ")
db_user = input("Username: ")
db_password = ("Password: ")


postgres = psycopg2.connect(
    dbname=f'{db_name}', 
    user=f'{db_user}', 
    password=f'{db_password}',
    host='localhost'
)

cursor = postgres.cursor()



Window.size = (400,600)


class Manager(ScreenManager):
    pass


class FirstScreen(MDScreen):
    def left(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'liblog'
    
    def rleft(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'readlog'
    
    def libreg(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'libregister'
    def readreg(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'readregister'

        

libmail=''
class LiblogScreen(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.lib_email.text = ""
        self.ids.lib_password.text = ""

    def loglib(self) :
        global libmail
        libmail = self.ids.lib_email.text
        libpassword = self.ids.lib_password.text
        
     
        result = check(libmail,libpassword, 'librarian_acc')
        if result == True:
            self.manager.transition=NoTransition()
            self.manager.current = 'libprofile'

        else:
            if libmail and libpassword:
               
                self.ids.lib_password.text = ""
                self.ids.lib_email.focus = True

            elif libmail and not libpassword:
                self.ids.lib_password.focus = True

            elif libpassword and not libmail:
                self.ids.lib_password.text = ""
                self.ids.lib_email.focus = True

            else:
                self.ids.lib_email.focus = True
        

    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'firstscreen'
    
    def reset(self):
        self.manager.transition.direction='left'
        self.manager.current = 'libreset'




class LibRegister(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.email_register2.text = ""
        self.ids.password_register2.text = ""
        self.ids.password_register_confirm2.text = ""
        self.ids.label_register2.text = "Enter your data"
        

    def callback(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'firstscreen'

    def submit(self):
        self.manager.transition = NoTransition()
        self.manager.current  = 'verification2'
        
class LibResetPassword(MDScreen): 

         
 
    def callback(self, *args): 
        self.manager.transition.direction = 'right' 
        self.manager.current = 'liblog' 
 
    def on_pre_enter(self, *args): 
        self.ids.text_redefined.theme_text_color = 'Custom' 
        self.ids.text_redefined.text_color = [0,0,0,1] 
        self.ids.text_redefined.text = "Send E-mail to reset password." 
        self.ids.email_confirm.text = ""
        


read_mail=''
class ReaderLog(MDScreen):

    def on_pre_enter(self, *args):
        self.ids.read_email.text = ''
        self.ids.read_password.text = ''
    
    def sign_in(self):
        global read_mail
        read_mail = self.ids.read_email.text 
        read_pass = f'{self.ids.read_password.text}' 
        # mycursor.execute(f"select email from about_readers where email = '{read_mail}' ")
        result = check(read_mail,read_pass, 'reader_acc')
        print(result)
        print(type(read_mail))
        print(type(read_pass))
        if result == True:
            
            self.manager.transition = NoTransition()
            self.manager.current = 'readprofile'
        else:
            self.ids.read_email.text=''
            self.ids.read_password.text=''
  
      
    def callback(self):
        self.manager.transition.direction='right'
        self.manager.current = 'firstscreen'
    def reset(self):
        self.manager.transition.direction='left'
        self.manager.current = 'readreset'

class ReadRegister(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.email_register.text = ''
        self.ids.password_register.text = ''
        self.ids.password_register_confirm.text = ''
    def callback(self):
        self.manager.transition.direction='right'
        self.manager.current = 'firstscreen'
    def check(self):
        self.manager.transition.direction='right'
        self.manager.current = 'verification'
        global reader_number
        reader_number = randint(1000, 10000)
        print(self.ids.email_register.text)
        send_mail(reader_number, self.ids.email_register.text)
        global read_mail
        read_mail = self.ids.email_register.text
        global reader_pass
        reader_pass = self.ids.password_register.text


class ReaderProfile(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_name)
        Clock.schedule_once(self.set_toolbar_font_size)
        self.l1=[]
        

    def set_toolbar_font_name(self, *args):
        self.ids.tooltitle.ids.label_title.font_name = 'fonts/welcome.ttf'

    def set_toolbar_font_size(self, *args):
        self.ids.tooltitle.ids.label_title.font_size = '30sp'

    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'firstscreen'

    def search_book(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readsearch'
        
    def readed_books(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readedbooks'
        
    def favorites(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'favoritebooks'

    def wallet(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'wallet'

    def borrow(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'borrowbook'

    def returnbook(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'return_book'

    def cardtap(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readbookinfo'

    def borrowed_list(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'listborrowed'

    def all_books(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'allbooks'
    
    def aboutlib(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'aboutlib'


    def gg(self,g):
        cursor.execute(f"SELECT name, author, year, price, image FROM ch_books WHERE name='{g.text}'")
        global name
        global img
        global price 
        global year
        global author

        result = cursor.fetchone() 
        name = result[0]
        img = result[4]
        price = result[3]
        year = result[2]
        author = result[1]

        self.manager.transition = SlideTransition()
        self.manager.current = 'readbookinfo'

    def on_pre_enter(self,*args):
    
        
        cursor.execute(f'SELECT name, author, year, price, image, id FROM ch_books')
        result = cursor.fetchall()
        if len(self.l1) < len(result):
            for i in range (len(result)):
                card = MDCard(orientation='vertical', padding=3,spacing=1,size_hint=(.1,None))
                card.elevation = 14
                card.height = 245
                card.radius = [20,20,20,20]

                
                im = Image(source=f"{result[i][4]}",size_hint_y=.7,allow_strech=True,keep_ratio=False)
                card.add_widget(im)
                n = MDTextButton(size_hint_y=.1,text=f"{result[i][0]}",pos_hint={"center_x":.5})
                n.theme_text_color = 'Custom'
                n.text_color = [1,0,1,1]
                n.font_size = 13
                n.bind(on_press=self.gg)
                card.add_widget(n)
                a = MDLabel(size_hint_y=.1,text=f"Author: {result[i][1]}",halign='center')
                a.font_size = 13
                card.add_widget(a)
                pr = MDLabel(size_hint_y=.1,text=f"Price: {str(result[i][3])} $",halign='center')
                pr.font_size = 13
                card.add_widget(pr)
                self.l1.append(i)
                self.ids.readgrid.add_widget(card)
    
    

class ReadResetPassword(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readlog'


img = ''
name = ''
price = 0
author = '' 
year=0
class ReadSearchBook(MDScreen):
    def on_pre_enter(self, *args):
        
        self.ids.readauthor.text = ""
        self.ids.readyear.text = ""
        self.ids.readbookname.text = ""

    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def search(self,**kwargs):
        global name
        global img
        global price 
        global year
        global author

        aut_name = self.ids.readauthor.text 
        year_book = self.ids.readyear.text
        book_name = self.ids.readbookname.text
        close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
        if aut_name=='' and year_book=='' and book_name == '':
            self.dialog = MDDialog(title='Alert',text='Fill one of the fields!',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
        elif aut_name != '':
            cursor.execute(f"SELECT author FROM ch_books WHERE author='{str(aut_name)}'")
            result = cursor.fetchone()
            if result:
                
                author = result[0]
                
                self.manager.transition = NoTransition()
                self.manager.current = 'newsearch'
            else: 
                self.ids.readauthor.text=''
                self.ids.readyear.text=''
                self.ids.readbookname.text=''

        elif year_book != '':
            cursor.execute(f"SELECT year FROM ch_books WHERE year='{year_book}'")
            result = cursor.fetchone()
            if result:

                year = result[0]
            
                self.manager.transition = NoTransition()
                self.manager.current = 'yearsearch'

            else: 
                self.ids.readauthor.text=''
                self.ids.readyear.text=''
                self.ids.readbookname.text=''

        elif  book_name != '':
            cursor.execute(f"SELECT * FROM ch_books WHERE name='{book_name}' " )
            result = cursor.fetchone()
            if result:
                
                name = result[1]

                
                img = result[5]

                
                price = result[4]

                
                year = result[3]

                 
                author = result[2]
                
                self.manager.transition = NoTransition()
                self.manager.current = 'readbookinfo'

            else: 
                self.ids.readauthor.text=''
                self.ids.readyear.text=''
                self.ids.readbookname.text=''



class ReadedBooks(MDScreen):
    def on_pre_enter(self, **kwargs):
        listitem = self.ids.txt.text 
        for i in range(1):
            self.ids.container.add_widget(
                OneLineListItem(text=f"{listitem}")
            )
        
    def __init__(self,**kwargs):
        super(ReadedBooks,self).__init__(**kwargs)
        layout = FloatLayout()

        toolbar = MDToolbar(md_bg_color=[1, 1, 1, 1],pos_hint={'top':1}, 
                            specific_text_color=[156/255,45/255,230/255,1])
        toolbar.left_action_items=[["arrow-left", lambda x: self.callback()]]

        label = MDLabel(text='The Readed Books:',halign='center',font_size=15,pos_hint={"center_x": .5,"center_y":.95})
        scrollview = ScrollView(size_hint_y=.5, pos_hint = {"center_x": .5, "center_y": .53})
        self.list1 = MDList()
        self.ids['readedbooks']=self.list1
        scrollview.add_widget(self.list1)
        layout.add_widget(scrollview)
        label1 =  MDLabel(text='Add a book:',halign='center',font_size=15,pos_hint={"center_x": .5,"center_y":.25})
        txt = MDTextField(hint_text='name of the book',pos_hint={"center_x": .5,"center_y":.18},size_hint_x=.8)
        self.ids['txt']=txt
        btn =  MDFillRoundFlatIconButton(text='ADD',font_size=20,icon='plus',pos_hint = {"center_x": .5, "center_y": .1})
        btn.elevation = 8
        btn.theme_text_color = 'Custom'
        btn.text_color = [254/255.0, 254/255.0, 254/255.0, 1]
        btn.md_bg_color = [0.18, 0.53, 1, 1]
        
        btn.bind(on_press=self.add_read_book)
        layout.add_widget(label1)
        layout.add_widget(txt)
        layout.add_widget(toolbar)
        layout.add_widget(label)
        layout.add_widget(btn)
        self.add_widget(layout)
        

    def on_pre_enter(self, *args):
        self.list1.clear_widgets()
        self.ids.txt.focus = True
        cursor.execute(f"SELECT name FROM r_books WHERE mail = '{read_mail}'")
        result = cursor.fetchall()
        for t in result:
            self.ids.readedbooks.add_widget(OneLineListItem(text=f'{t[0]}'))
                
        
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    def add_read_book(self,obj):
        str(obj)
    
        read_mail
        bname = self.ids.txt.text
        cursor.execute(f"INSERT INTO r_books (mail, name) values('{read_mail}','{bname}')")
        postgres.commit()

        close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
        self.dialog = MDDialog(title='Successfully !!!',text='The book was added.',
                            size_hint=(.7,1),buttons=[close_btn])
        self.dialog.open()
        self.ids.txt.text = ''

        

    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()
  


class FavoriteBooks(MDScreen):

        
    def __init__(self,**kwargs):
        super(FavoriteBooks,self).__init__(**kwargs)
        layout = FloatLayout()

        toolbar = MDToolbar(md_bg_color=[1, 1, 1, 1],pos_hint={'top':1}, 
                            specific_text_color=[156/255,45/255,230/255,1])
        toolbar.left_action_items=[["arrow-left", lambda x: self.callback()]]

        label = MDLabel(text='The Favorite Books:',halign='center',font_size=15,pos_hint={"center_x": .5,"center_y":.95})
        scrollview = ScrollView(size_hint_y=.5, pos_hint = {"center_x": .5, "center_y": .53})
        self.list1 = MDList()
        self.ids['favbooks']=self.list1
        scrollview.add_widget(self.list1)
        layout.add_widget(scrollview)
        label1 =  MDLabel(text='Add a book:',halign='center',font_size=15,pos_hint={"center_x": .5,"center_y":.25})
        txt = MDTextField(hint_text='name of the book',pos_hint={"center_x": .5,"center_y":.18},size_hint_x=.8)
        self.ids['favtxt']=txt
        btn =  MDFillRoundFlatIconButton(text='ADD',font_size=20,icon='plus',pos_hint = {"center_x": .5, "center_y": .1})
        btn.elevation = 8
        btn.theme_text_color = 'Custom'
        btn.text_color = [254/255.0, 254/255.0, 254/255.0, 1]
        btn.md_bg_color = [0.18, 0.53, 1, 1]
        
        btn.bind(on_press=self.add_read_book)
        layout.add_widget(label1)
        layout.add_widget(txt)
        layout.add_widget(toolbar)
        layout.add_widget(label)
        layout.add_widget(btn)
        self.add_widget(layout)
        

    def on_pre_enter(self, *args):
        self.list1.clear_widgets()
        self.ids.favtxt.focus = True
        cursor.execute(f"SELECT name FROM f_books WHERE mail = '{read_mail}'")
        result = cursor.fetchall()
        for t in result:
            self.ids.favbooks.add_widget(OneLineListItem(text=f'{t[0]}'))
           

        
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    def add_read_book(self,obj):
        str(obj)
    
        global read_mail
        bname = self.ids.favtxt.text
        cursor.execute(f"INSERT INTO f_books(mail, name) VALUES('{read_mail}','{bname}')")
        postgres.commit()

        close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
        self.dialog = MDDialog(title='Successfully !!!',text='The book has been added.',
                            size_hint=(.7,1),buttons=[close_btn])
        self.dialog.open()
        self.ids.favtxt.text = ''

        

    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()



class Wallet(MDScreen):

    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    def on_pre_enter(self, *args):
        global read_mail
        cursor.execute(f"SELECT wallet FROM reader_acc WHERE mail='{read_mail}'")
        result = cursor.fetchone()
        txt = result[0]
        self.ids.wally.text = str(txt)

    def fillbalance(self):
        value = int(self.ids.filldollar.text)
        cursor.execute(f"SELECT wallet FROM reader_acc WHERE mail='{read_mail}'")
        result = cursor.fetchone()
        current_value = result[0]
        eventual = value + current_value
        cursor.execute(f"UPDATE reader_acc SET wallet={eventual} WHERE mail='{read_mail}'")
        postgres.commit()
        close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
        self.dialog = MDDialog(title='Successfully !!!',text='Your balance has been topped up.',
                            size_hint=(.7,1),buttons=[close_btn])
        self.dialog.open()
        self.ids.filldollar.text = ''

    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()
        

class BorrowBook(MDScreen):
    def on_pre_enter(self,*args):
        self.ids.borrow_name.text = ''
        self.ids.dateborrow.text = ''
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    def on_cancel(self,instance,value):
        self.ids.dateborrow.text = "You clicked cancel."
    def on_save(self,instance,value,date_range):
        self.date_range = date_range
        self.ids.dateborrow.text = f'{str(self.date_range[0])} >>> {str(self.date_range[-1])}'

    def calendar(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save,on_cancel=self.on_cancel)
        date_dialog.open()
    
    def submit(self,**kwargs):
        global read_mail
        cursor.execute(f"SELECT many FROM ch_books WHERE name = '{self.ids.borrow_name.text}'")
        result = cursor.fetchone()
        print(result)
        if result:
            if result[0]>=1:

                cursor.execute(f'''
                                INSERT INTO borrowed_b (mail,st_date,end_date,name) 
                                VALUES ('{read_mail}','{str(self.date_range[0])}','{str(self.date_range[-1])}','{self.ids.borrow_name.text}') ''')
                postgres.commit()

                n = result[0] - 1
                cursor.execute(f"UPDATE ch_books SET many={n} WHERE name = '{self.ids.borrow_name.text}' ")
                postgres.commit()
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Borrowing',text='The book has been borrowed.',
                                    size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
            elif result[0]==0:
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Sorry',text=f'Sorry, but there are no "{self.ids.borrow_name.text}" left.',
                                    size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
        else:
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Sorry',text=f'Sorry, there are no  such books in InLibrary :(',
                                size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()

        

    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()


class BorrowBook2(MDScreen):
    def on_pre_enter(self,*args):
        global name
        self.ids.borrow2_name.text = f"{name}"
        self.ids.borrow2_name.focus = True
        self.ids.date2borrow.text = ''
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readbookinfo'
    def on_cancel(self,instance,value):
        self.ids.date2borrow.text = "You clicked cancel."
    def on_save(self,instance,value,date_range):
        self.date_range = date_range
        self.ids.date2borrow.text = f'{str(self.date_range[0])} >>> {str(self.date_range[-1])}'

    def calendar(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save,on_cancel=self.on_cancel)
        date_dialog.open()
    
    def submit(self,**kwargs):
        global read_mail
        cursor.execute(f"SELECT many FROM ch_books WHERE name = '{self.ids.borrow2_name.text}'")
        result = cursor.fetchone()
        print(result)
        if result:
            if result[0]>=1:

                cursor.execute(f'''
                                INSERT INTO borrowed_b (mail, st_date, end_date, name) 
                                VALUES ('{read_mail}','{str(self.date_range[0])}','{str(self.date_range[-1])}','{self.ids.borrow2_name.text}') ''')
                postgres.commit()

                n = result[0] - 1
                cursor.execute(f"UPDATE ch_books SET many={n}  WHERE name = '{self.ids.borrow2_name.text}' ")
                postgres.commit()
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Borrowing',text='The book has been borrowed.',
                                    size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
            elif result[0]==0:
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Sorry',text=f'Sorry, but there are no "{self.ids.borrow2_name.text}" left.',
                                    size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
        else:
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Sorry',text=f'Sorry, there are no  such books in InLibrary :(',
                                size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
        
        

    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()






class ReturnBook(MDScreen):
    
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    
    def on_pre_enter(self,**kwargs):
        self.ids.return_name.text = ''


    def returnb(self,**kwargs):
        global read_mail
        cursor.execute(f"SELECT name FROM borrowed_b WHERE (name='{self.ids.return_name.text}' and mail = '{read_mail}')")
        result = cursor.fetchone()
        if result: 
            cursor.execute(f"DELETE FROM borrowed_b WHERE (name='{self.ids.return_name.text}' and mail = '{read_mail}')")
            postgres.commit()
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Successfully!',text='The book has been returned.',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
        else:
            close_btn = MDFlatButton(text='Close',on_release=self.close_window)
            self.dialog = MDDialog(title='Error',text='Wrong book name.',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()

    def close_window(self,obj):
        self.dialog.dismiss()
        self.ids.return_name.text = ''
        
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()
class BookInfRead(MDScreen):
    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'readprofile'

    def on_pre_enter(self,*args):
        self.ids.bookimage.source = img
        self.ids.bookname.text = name
        self.ids.bookauthor.text = f"Author: {author}"
        self.ids.bookyear.text = f"Year: {str(year)}"
        self.ids.bookprice.text = f"Price: {str(price)} $"
    
    def bor(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'borrowbook2'

    def buy(self):
        
        cursor.execute(f"SELECT price FROM ch_books WHERE name='{name}'")
        result = cursor.fetchone()
        cena = result[0]
    
        cursor.execute(f"SELECT wallet FROM reader_acc WHERE mail='{read_mail}'")
        res = cursor.fetchone()
        current = res[0]
        itogo = 0
        if current>=int(cena):
            itogo = current - cena
            cursor.execute(f"UPDATE reader_acc SET wallet={itogo} WHERE mail='{read_mail}'")
            postgres.commit()
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Congratulations !!!',text=f"You have boungt the book {name} ",
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            cursor.execute(f"INSERT INTO mybooks(name, mail) VALUES('{name}', '{read_mail}')")
            postgres.commit()
        else:
            k = cena - current
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Error',text=f'You need {str(k)} more dollars to purchase. ',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            

    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()

class BookInfRead2(MDScreen):
    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'readprofile'

    def on_pre_enter(self,*args):
        self.ids.bookimage2.source = img
        self.ids.bookname2.text = name
        self.ids.bookauthor2.text = f"Author: {author}"
        self.ids.bookyear2.text = f"Year: {str(year)}"
        self.ids.bookprice2.text = f"Price: {str(price)} $"
    
    def bor(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'borrowbook2'
    
    def buy(self):
        
        cursor.execute(f"SELECT price FROM ch_books WHERE name='{name}'")
        result = cursor.fetchone()
        cena = result[0]
    
        cursor.execute(f"SELECT wallet FROM reader_acc WHERE mail='{read_mail}'")
        res = cursor.fetchone()
        current = res[0]
        itogo = 0
        if current>=cena:
            itogo = current - cena
            cursor.execute(f"UPDATE reader_acc SET wallet={itogo} WHERE mail='{read_mail}'")
            cursor.execute(f"INSERT INTO mybooks(name, mail) VALUES('{name}', '{read_mail}')")
            postgres.commit()
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Congratulations !!!',text=f'You have boungt the book "{name}"',
                            size_hint=(.7,1),buttons=[close_btn])
            
            self.dialog.open()
        else:
            k = cena - current
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Error',text=f'You need {str(k)} more dollars to purchase. ',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()





mycursor = postgres.cursor()
        

class BookInfRead3(MDScreen):
    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'newsearch'

    def on_pre_enter(self,*args):
        self.ids.bookimage3.source = img
        self.ids.bookname3.text = name
        self.ids.bookauthor3.text = f"Author: {author}"
        self.ids.bookyear3.text = f"Year: {str(year)}"
        self.ids.bookprice3.text = f"Price: {str(price)} $"
    
    def bor(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'borrowbook2'
    
    def buy(self):
        
        cursor.execute(f"SELECT price FROM ch_books WHERE name='{name}'")
        result = cursor.fetchone()
        cena = result[0]
    
        cursor.execute(f"SELECT wallet FROM reader_acc WHERE mail='{read_mail}'")
        res = cursor.fetchone()
        current = res[0]
        itogo = 0
        if current>=cena:
            itogo = current - cena
            cursor.execute(f"UPDATE reader_acc SET wallet={itogo} WHERE mail='{read_mail}'")
            postgres.commit()
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Congratulations !!!',text=f'You have boungt the book "{name}"',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            cursor.execute(f"INSERT INTO mybooks(name, mail) VALUES('{name}', '{read_mail}')")
            postgres.commit()
        else:
            k = cena - current
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Error',text=f'You need {str(k)} more dollars to purchase. ',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()


class BookInfRead4(MDScreen):
    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'yearsearch'

    def on_pre_enter(self,*args):
        self.ids.bookimage4.source = img
        self.ids.bookname4.text = name
        self.ids.bookauthor4.text = f"Author: {author}"
        self.ids.bookyear4.text = f"Year: {str(year)}"
        self.ids.bookprice4.text = f"Price: {str(price)} $"
    # FavoriteBooks>:
#     MDFloatLayout:
#         MDToolbar:
#             pos_hint: {"top": 1}
#             left_action_items: [["arrow-left", lambda x: root.callback()]]
#             specific_text_color: 156/255,45/255,230/255,1
#             md_bg_color: 1, 1, 1, 1
#             size_hint_y: .1
#         MDLabel:
#             #size_hint_y: .1
#             text: 'Favorite books'
#             font_size: 20
#             theme_text_color: 'Custom'
#             text_color: 156/255,45/255,230/255,1
#             pos_hint: {"center_y":.95}
#             halign: 'center'
#         ScrollView:
#             size_hint_y: .5
#             pos_hint:{'center_x':.5,'center_y':.4}
#             MDList:
#                 id: fav_books
#         MDTextField:
#             hint_text: "Book name"
#             size_hint_x: .8
#             size_hint_y: .1
#             pos_hint: {"center_x": .5}
#             icon_right: "book-plus-outline"
#             icon_right_color: 156/255,45/255,230/255,1
#             id: favplus

#         MDFillRoundFlatIconButton:
            
#             text: "Add"
#             font_size: 20
#             elevation: 8
#             theme_text_color: "Custom"
#             text_color: 254/255.0, 254/255.0, 254/255.0, 1
#             pos_hint: {"center_x": .5,"center_y":.1}
#             icon: "plus"
#             on_release: root.add_read_book()
    def bor(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'borrowbook2'
    
    def buy(self):
        
        mycursor.execute(f"SELECT price FROM ch_books WHERE name='{name}'")
        result = mycursor.fetchone()
        cena = result[0]
    
        mycursor.execute(f"SELECT wallet FROM reader_acc WHERE mail='{read_mail}'")
        res = mycursor.fetchone()
        current = res[0]
        itogo = 0
        if current>=cena:
            itogo = current - cena
            mycursor.execute(f"UPDATE reader_acc SET wallet={itogo} WHERE mail='{read_mail}'")
            postgres.commit()
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Congratulations !!!',text=f'You have boungt the book "{name}"',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            cursor.execute(f"INSERT INTO mybooks(name, mail) VALUES('{name}', '{read_mail}')")
            postgres.commit()
        else:
            k = cena - current
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Error',text=f'You need {str(k)} more dollars to purchase. ',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
            
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
        self.dialog.dismiss()


class ListBorrowedReader(MDScreen):
        
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    
    def on_pre_enter(self, *args): 
        self.ids.readborrowed.clear_widgets()  
        mycursor.execute(f"SELECT name, st_date, end_date FROM borrowed_b WHERE mail='{read_mail}'")
        result = mycursor.fetchall()
        for t in result:
            n = TwoLineListItem(text=f'{t[0]}',secondary_text=f'{t[1]} >>> {t[2]}')
            
            self.ids.readborrowed.add_widget(n)
        



class NewSearch(MDScreen):
    def su(self,c):
        mycursor.execute(f"SELECT name, author, year, price, image FROM ch_books WHERE name='{c.text}'")
        global name
        global img
        global price 
        global year
        global author

        result = mycursor.fetchone() 
        name = result[0]
        img = result[4]
        price = result[3]
        year = result[2]
        author = result[1]

        self.manager.transition = SlideTransition()
        self.manager.current = 'readbookinfo3'

    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readsearch'
    def on_pre_enter(self,*args):
        self.ids.autlabel.text = f"The books of {author}"
        self.ids.autorbook.clear_widgets()
        mycursor.execute(f"SELECT * FROM ch_books WHERE author='{author}'")
        result = mycursor.fetchall()
        for i in range(len(result)):
            n = TwoLineListItem(text=result[i][1],secondary_text=f'Year: {str(result[i][3])}')
            n.bind(on_release=self.su)
            self.ids.autorbook.add_widget(n)

class YearSearch(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readsearch'
    def gg(self,g):
        mycursor.execute(f"SELECT name, author, year, price, image FROM ch_books WHERE name='{g.text}'")
        global name
        global img
        global price 
        global year
        global author

        result = mycursor.fetchone() 
        name = result[0]
        img = result[4]
        price = result[3]
        year = result[2]
        author = result[1]

        self.manager.transition = SlideTransition()
        self.manager.current = 'readbookinfo4'
    def on_pre_enter(self,*args):
        self.ids.yearlabel.text=f"The books published in {str(year)}:"
        self.ids.yearbook.clear_widgets()
        mycursor.execute(f"SELECT * FROM ch_books WHERE year='{year}'")
        result = mycursor.fetchall()
        for i in range(len(result)):
            n = TwoLineListItem(text=result[i][1],secondary_text=f"Author: {result[i][2]}")
            n.bind(on_release=self.gg)
            self.ids.yearbook.add_widget(n)



class AllBooks(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    
    def ck(self,j):
        mycursor.execute(f"SELECT name, author, year, price, image FROM ch_books WHERE name='{j.text}'")
        global name
        global img
        global price 
        global year
        global author

        result = mycursor.fetchone() 
        name = result[0]
        img = result[4]
        price = result[3]
        year = result[2]
        author = result[1]
        self.manager.transition = NoTransition()
        self.manager.current = 'readbookinfo2'

    def on_pre_enter(self,*args):
        self.ids.allbook.clear_widgets()
        mycursor.execute(f"SELECT name, author, year FROM ch_books")
        result = mycursor.fetchall()
        for i in range(len(result)):
            n = ThreeLineListItem(text=result[i][0],secondary_text=f"Author: {result[i][1]}",tertiary_text=f"Year: {str(result[i][2])}")
            n.bind(on_release=self.ck)
            self.ids.allbook.add_widget(n)
            
class AboutLib(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readprofile'
    


class LibProfile(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_name)
        Clock.schedule_once(self.set_toolbar_font_size)
    def lookreader(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'lookreader'

    def set_toolbar_font_name(self, *args):
        self.ids.libtitle.ids.label_title.font_name = 'fonts/welcome.ttf'

    def set_toolbar_font_size(self, *args):
        self.ids.libtitle.ids.label_title.font_size = '30sp'
    def reserve(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'reservebook'
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'firstscreen'
    def libsearchbook(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libsearchbook'
    
    def on_pre_enter(self, *args): 
        
        self.ids.libgrid.clear_widgets()  
        mycursor.execute(f"SELECT mail, name, st_date, end_date FROM borrowed_b ORDER BY end_date")
        result = mycursor.fetchall()
        
        for i in range(len(result)):

            n = ThreeLineListItem(text=f"Email: {result[i][0]}", secondary_text=f"{result[i][1]}", tertiary_text=f'{str(result[i][2])} >>>>> {str(result[i][3])}')
            
            self.ids.libgrid.add_widget(n)
    
    def list_readers(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'listofreaders'
    def aboutlib(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libaboutlib'

    def liblistreserved(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libreserved'

        
class ListofReaders(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libprofile'
    def on_pre_enter(self,*args):
        self.ids.listreaders.clear_widgets()

        mycursor.execute(f"SELECT mail from reader_acc")
        result = mycursor.fetchall()
        for i in range(len(result)):
            n = OneLineListItem(text=f'{result[i][0]}')
            n.bind(on_release=self.aboutreader)
            self.ids.listreaders.add_widget(n)
    
    def aboutreader(self,obj):
        global read_mail
        read_mail = obj.text
        self.manager.transition = NoTransition()
        self.manager.current = 'aboutreader'

readname=''
readsurname=''
libreturn = ''
readcontact=''
class AboutReader(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'listofreaders'
    def libreturn(self,obj):
        global libreturn
        libreturn = obj.text
        self.manager.transition = NoTransition()
        self.manager.current = 'libreturn'

    def on_pre_enter(self,*args):
        mycursor.execute(f"SELECT mail FROM reader_acc WHERE mail='{read_mail}'")
        result = mycursor.fetchone()

        self.ids.aboutread.text = f'Email: {read_mail}'
        

        mycursor.execute(f"SELECT name FROM borrowed_b WHERE mail='{read_mail}'")
        res = mycursor.fetchall()
        self.ids.readborrow.clear_widgets() 
        self.ids.readbought.clear_widgets()
        for i in range(len(res)):
            n = OneLineListItem(text=f"{res[i][0]}")
            n.bind(on_release=self.libreturn)
            self.ids.readborrow.add_widget(n)
        
        mycursor.execute(f"SELECT name FROM mybooks WHERE mail='{read_mail}'")
        resi = mycursor.fetchall()
         
        for i in range(len(resi)):
            k = OneLineListItem(text=f"{resi[i][0]}")
            
            self.ids.readbought.add_widget(k)

class ReturnBook2(MDScreen):
    
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'aboutreader'
    
    def on_pre_enter(self,**kwargs):
        self.ids.return_name2.text = libreturn


    def returnb(self,**kwargs):
        global read_mail
        mycursor.execute(f"SELECT name FROM borrowed_b WHERE name='{self.ids.return_name2.text}' and mail = '{read_mail}'")
        result = mycursor.fetchone()
        if result: 
            mycursor.execute(f"DELETE FROM borrowed_b WHERE name='{self.ids.return_name2.text}' and mail = '{read_mail}'")
            postgres.commit()
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Successfully!',text='The book has been returned.',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
        else:
            close_btn = MDFlatButton(text='Close',on_release=self.close_window)
            self.dialog = MDDialog(title='Error',text='Wrong book name.',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()

    def close_window(self,obj):
        self.dialog.dismiss()
        self.ids.return_name2.text = ''
        
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'aboutreader'
        self.dialog.dismiss()


# class LookReader(MDScreen):
#     def callback(self):
#         self.manager.transition = NoTransition()
#         self.manager.current = 'libprofile'
#     def on_pre_enter(self, *args):
        
        
#         self.ids.readsur.text = ""
#         self.ids.readname2.text = ""

#     def close_dialog(self,obj):
#         self.dialog.dismiss()
    
#     def search(self,**kwargs):
#         global readname
#         global readsurname
#         global readcontact
#         global read_mail
        

#         read_name = self.ids.readname2.text 
#         read_surname = self.ids.readsur.text
        
#         close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
#         if read_name=='' and read_surname=='':
#             self.dialog = MDDialog(title='Alert',text='Fill one of the fields!',
#                             size_hint=(.7,1),buttons=[close_btn])
#             self.dialog.open()
#         elif read_name != '':
#             mycursor.execute(f"SELECT name, surname,email,contact_number from readers where name="{str(read_name)}"')
#             result = mycursor.fetchone()
#             if result:
                
#                 readname = result[0]
#                 readsurname = result[1]
#                 read_mail = result[2]
#                 readcontact = result[3]


                
#                 self.manager.transition = NoTransition()
#                 self.manager.current = 'libreaderserch'
#             else: 
                
#                 self.ids.readsur.text=''
#                 self.ids.readname2.text=''

#         elif read_surname != '':
#             mycursor.execute(f'select surname,email,name,contact_number from readers where surname="{read_surname}"')
#             result = mycursor.fetchone()
#             if result:


#                 readsurname = result[0]
#                 read_mail = result[1]
#                 readname = result[2]
#                 readcontact = result[3]

                
#                 self.manager.transition = NoTransition()
#                 self.manager.current = 'libreaderserch'

#             else: 
#                 self.ids.readsur.text=''
#                 self.ids.readname2.text=''

        


class Libreaderserch(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'lookreader'
class Verification(MDScreen):
    def on_pre_enter(self,*args):
        self.ids.code_verification.text=''
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'readregister'
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'firstscreen'
        self.dialog.dismiss()
    def close_window(self):
        self.dialog.dismiss()
    def submit(self):
        code = self.ids.code_verification.text
        if self.ids.code_verification.text == '':
            self.ids.ode_verification.focus = True
        else:
            if code == str(reader_number):
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Successfully',text='The reader is created!',
                            size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
                create(reader_pass, read_mail, 'reader_acc' )
                # cursor.execute(f"INSERT INTO kurs_acc(mail, password) VALUES('{reader_mail}', '{reader_pass}'")
                # postgres.commit()
            else:
                close_btn = MDFlatButton(text='Close',on_release=self.close_window)
                self.dialog = MDDialog(title='Error',text='The code is not right.Try again.',
                            size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
                self.ids.code_verification.text = ''




class LibSearchBook(MDScreen):
    def on_pre_enter(self, *args):
        
        self.ids.readauthor2.text = ""
        self.ids.readyear2.text = ""
        self.ids.readbookname2.text = ""

    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libprofile'

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def search(self,**kwargs):
        global name
        global img
        global price 
        global year
        global author

        aut_name = self.ids.readauthor2.text 
        year_book = self.ids.readyear2.text
        book_name = self.ids.readbookname2.text
        close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
        if aut_name=='' and year_book=='' and book_name == '':
            self.dialog = MDDialog(title='Alert',text='Fill one of the fields!',
                            size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
        elif aut_name != '':
            mycursor.execute(f"SELECT author FROM ch_books WHERE author='{str(aut_name)}'")
            result = mycursor.fetchone()
            if result:
                
                author = result[0]
                
                self.manager.transition = NoTransition()
                self.manager.current = 'newsearch2'
            else: 
                self.ids.readauthor2.text=''
                self.ids.readyear2.text=''
                self.ids.readbookname2.text=''

        elif year_book != '':
            mycursor.execute(f"SELECT year FROM ch_books WHERE year='{year_book}'")
            result = mycursor.fetchone()
            if result:

                year = result[0]
                
                self.manager.transition = NoTransition()
                self.manager.current = 'yearsearch2'

            else: 
                self.ids.readauthor2.text=''
                self.ids.readyear2.text=''
                self.ids.readbookname2.text=''

        elif  book_name != '':
            mycursor.execute(f"SELECT * FROM ch_books WHERE name='{book_name}'" )
            result = mycursor.fetchone()
            if result:
                
                name = result[1]

                
                img = result[5]

                
                price = result[4]

                
                year = result[3]

                 
                author = result[2]
                
                self.manager.transition = NoTransition()
                self.manager.current = 'bookinf7'

            else: 
                self.ids.readauthor2.text=''
                self.ids.readyear2.text=''
                self.ids.readbookname2.text=''
class NewSearch2(MDScreen):
    def s(self,c):
        mycursor.execute(f"SELECT name, author, year, price, image FROM ch_books WHERE name='{c.text}'")
        global name
        global img
        global price 
        global year
        global author

        result = mycursor.fetchone() 
        name = result[0]
        img = result[4]
        price = result[3]
        year = result[2]
        author = result[1]

        self.manager.transition = NoTransition()
        self.manager.current = 'readbookinfo5'

    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libsearchbook'
    def on_pre_enter(self,*args):
        self.ids.autlabel.text = f"The books of {author}"
        self.ids.autorbook.clear_widgets()
        mycursor.execute(f"SELECT * FROM ch_books WHERE author='{author}'")
        result = mycursor.fetchall()
        for i in range(len(result)):
            n = TwoLineListItem(text=result[i][1],secondary_text=f'Year: {str(result[i][3])}')
            n.bind(on_release=self.s)
            self.ids.autorbook.add_widget(n)

class BookInfRead5(MDScreen):
    def callback(self):
        self.manager.transition=NoTransition()
        self.manager.current = 'newsearch2'

    def on_pre_enter(self,*args):
        self.ids.bookimage5.source = img
        self.ids.bookname5.text = name
        self.ids.bookauthor5.text = f"Author: {author}"
        self.ids.bookyear5.text = f"Year: {str(year)}"
        self.ids.bookprice5.text = f"Price: {str(price)} $"
    
class ReserveBook(MDScreen):
    def callback(self):
        self.manager.transition=NoTransition()
        self.manager.current = 'libprofile'

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def reservebook(self):
        mycursor.execute(f"SELECT name FROM ch_books WHERE name='{self.ids.resbook.text}'")
        result = mycursor.fetchone()
        if result:
            mycursor.execute(f"SELECT many FROM ch_books WHERE name='{self.ids.resbook.text}'")
            res = mycursor.fetchone()
            number = res[0]
            if number>0:
                number -= 1
                mycursor.execute(f"UPDATE ch_books SET many={number} WHERE name='{self.ids.resbook.text}'")
                postgres.commit()
                mycursor.execute(f"INSERT INTO reserved_b(mail,name) VALUES('{self.ids.resread.text}','{self.ids.resbook.text}')")
                postgres.commit()
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Successfully',text='The book is reserved.',
                            size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
                self.ids.resbook.text=''
                self.ids.resread.text=''
        else:
            close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
            self.dialog = MDDialog(title='Error',text='There are no such book in InLibrary :(',
                        size_hint=(.7,1),buttons=[close_btn])
            self.dialog.open()
    
    def on_pre_enter(self,*args):
        self.ids.resbook.text=''
        self.ids.resread.text=''



class YearSearch2(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libsearchbook'
    def gg(self,g):
        mycursor.execute(f"SELECT name, author, year, price, image FROM ch_books WHERE name='{g.text}'")
        global name
        global img
        global price 
        global year
        global author

        result = mycursor.fetchone() 
        name = result[0]
        img = result[4]
        price = result[3]
        year = result[2]
        author = result[1]

        self.manager.transition = SlideTransition()
        self.manager.current = 'readbookinf8'
    def on_pre_enter(self,*args):
        self.ids.yearlabel2.text=f"The books published in {str(year)}:"
        self.ids.yearbook2.clear_widgets()
        mycursor.execute(f"SELECT * FROM ch_books WHERE year='{year}'")
        result = mycursor.fetchall()
        for i in range(len(result)):
            n = TwoLineListItem(text=result[i][1],secondary_text=f"Author: {result[i][2]}")
            n.bind(on_release=self.gg)
            self.ids.yearbook2.add_widget(n)
class BookInfRead7(MDScreen):
    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'libsearchbook'

    def on_pre_enter(self,*args):
        self.ids.bookimage7.source = img
        self.ids.bookname7.text = name
        self.ids.bookauthor7.text = f"Author: {author}"
        self.ids.bookyear7.text = f"Year: {str(year)}"
        self.ids.bookprice7.text = f"Price: {str(price)} $"
    

class LibAboutLib(MDScreen):
    def callback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'libprofile'

class LibReserved(MDScreen):
        
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libprofile'
    
    def on_pre_enter(self, *args): 
        self.ids.listreserved.clear_widgets()  
        mycursor.execute(f"SELECT mail, name FROM reserved_b")
        result = mycursor.fetchall()
        for t in result:
            n = TwoLineListItem(text=f'Email: {t[0]}',secondary_text=f'{t[1]}')
            
            self.ids.listreserved.add_widget(n)


class Verification2(MDScreen):
    def callback(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'libregister'
    def on_pre_enter(self,*args):
        self.ids.code_verification2.text=''
    def close_dialog(self,obj):
        self.manager.transition = NoTransition()
        self.manager.current = 'firstscreen'
        self.dialog.dismiss()
    def close_window(self,obj):
        self.dialog.dismiss()
    def submit(self):
        code = self.ids.code_verification2.text
        if self.ids.code_verification2.text == '':
            self.ids.code_verification2.focus = True
        else:
            if code == "123":
                close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
                self.dialog = MDDialog(title='Successfully',text='The librarian account is created!',
                            size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
                #reader insert
            else:
                close_btn = MDFlatButton(text='Close',on_release=self.close_window)
                self.dialog = MDDialog(title='Error',text='The code is not right.Try again.',
                            size_hint=(.7,1),buttons=[close_btn])
                self.dialog.open()
                self.ids.code_verification2.text = ''

class BookInfRead8(MDScreen):
    def callback(self):
        self.manager.transition=NoTransition()
        self.manager.current = 'yearsearch2'

    def on_pre_enter(self,*args):
        self.ids.bookimage8.source = img
        self.ids.bookname8.text = name
        self.ids.bookauthor8.text = f"Author: {author}"
        self.ids.bookyear8.text = f"Year: {str(year)}"
        self.ids.bookprice8.text = f"Price: {str(price)} $"



class InLisisiApp(MDApp):
    pass 
        


if __name__=="__main__":
    InLisisiApp().run()

        



