from kivy.config import Config
Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 375)
Config.set("graphics", "height", 667)

from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

import sqlite3


connection= sqlite3.connect('trainings.db')
cursor= connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Trainings (
id INTEGER PRIMARY KEY UNIQUE,
date DATE NOT NULL,
ochki INTEGER NOT NULL,
ochki_max INTEGER NOT NULL
)
''')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%                                                                                              %
#%                                                                                              %
#%                                          ЭКРАНЫ                                              %
#%                                                                                              %
#%                                                                                              %
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class MyTextInput(TextInput):

        def insert_text(self, substring, from_undo=False):
            new_text = self.text + substring
            if not new_text.isdigit() or int(new_text) > 100:
                return
            super(MyTextInput, self).insert_text(substring, from_undo)






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






class TrainingScreen(Screen):
    stat= 0 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation= 'vertical')
        float= GridLayout(cols=2, spacing=-2.5, size_hint_y=0.4)
        self.label = Label(text="Общее кол-во очков",
                            pos_hint={'center_x':0.5, 'center_y':0.8})


        self.x:int= 0
        def on_press_num(num=None):
            self.label.text= f'Общее кол-во очков: {self.x+int(num)}'
            self.x+=num
            self.layout.pos= (0.5, .5)
        
#        self.button= Button(text= 'ОК', on_press= on_press_num)
        self.ochki= TextInput(text= '',input_filter= 'int',multiline=False,
                               size_hint=(.15, .05),
                               pos_hint= {'center_x': 0.5, 'center_y': .4}, 
                               on_text_validate= on_press_num)
        for i in range(10):
            float.add_widget(Button(text= f'{i+1}', 
                                    size= (.1,.5), on_press= lambda instance, 
                                    num=i+1: on_press_num(num),
                                    ))

        self.layout.add_widget(Button(text= '->', pos_hint= {'center_x':.95},
                                       size_hint_x= .12, size_hint_y= .075, 
                                       on_press= self.exit))
        self.layout.add_widget(self.label)



        self.add_widget(self.layout)
        self.add_widget(float)
    i= 0
    def exit(self, *args):
        home_screen = self.manager.get_screen('home')

        if self.i== 0:
            label= Label(text='''Дата: 23.02.2025\nКол-во очков: 5/300\nСреднее попадание: 2.5''', 
                         font_size= 20, color= 'black')
            self.i+= 1
        elif self.i==1:
            label= Label(text='Дата: 23.02.2025\nКол-во очков: 18/120\nСреднее попадание: 6', 
                         font_size= 20, color= 'black')
            self.stat+=1
        home_screen.carusell.add_widget(label)
        with label.canvas:
            Color(0, 1, 200, 0.50)
            Rectangle(pos=home_screen.carusell.pos, size= (300,480))
        self.manager.current = 'home'






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






class TrainingsSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(TrainingsSettingsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout(pos_hint= {'center_x': 0.5, 'center_y': 0.35},
                                   size= (.5,.5))

        self.text1 = MyTextInput(multiline=False, size_hint=(.15, .05),
                                  pos_hint= {'center_x': 0.5, 'center_y': .8})
        self.label1 = Label(text="Кол-во серий", pos_hint= {'center_y': .85})

        self.text2 = MyTextInput(multiline=False, size_hint=(.15, .05),
                                  pos_hint= {'center_x': 0.5, 'center_y': .7})
        self.label2 = Label(text='Кол-во выстрелов в серии', pos_hint= {'center_y': .75})

        self.label = Label(text="Training Settings", pos_hint= {'center_y': 1.1})

        self.button= Button(text= 'Начать тренеровку ->', 
                            pos_hint= {'center_y': .2, 'center_x': .5},
                             size_hint= (.5, .07), on_press= self.set_press)

        self.layout.add_widget(self.text1)
        self.layout.add_widget(self.text2)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.label1)
        self.layout.add_widget(self.label2)
        self.layout.add_widget(self.button)

        self.add_widget(self.layout)

    def set_press(self, *args):
        self.manager.current = 'tr'






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.label = Label(text="Your Trainings", 
                           pos_hint= {'center_y': .95, 'center_x': .5})
        self.button = Button(text='+',
                              size_hint=(.12, .07),
                              pos_hint={'x': 0.88, 'center_y': 0.03},
                              on_press=self.training_press)
        layout.add_widget(self.label)
        layout.add_widget(self.button)
        self.add_widget(layout)
    
        self.carusell= Carousel(direction= 'bottom', size_hint= (.9,.9),
                                 pos_hint= {'center_y':.5, 'center_x':.5})
        layout.add_widget(self.carusell)





    def training_press(self, *args):
        self.manager.current = 'tr_st'





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





class StatsScreen(Screen):
    stat= 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        if self.stat==1:
            self.label = Label(text="Статистика пока пуста")
            self.layout.add_widget(self.label)
            self.stat+= 1
        elif self.stat==0:
            self.label = Label(text="Среднее попадание\nза всё время:", bold= True, font_size= 20)
            self.label1 = Label(text="4,25", bold= True, font_size= 20, color= 'red')
            self.label2 = Label(text="Среднее попадание  за\nпоследние 5 тренировок:", bold= True, font_size= 20)
            self.label3 = Label(text="4,25", bold= True, font_size= 20, color= 'red')   
            self.layout.add_widget(self.label)
            self.layout.add_widget(self.label1)
            self.layout.add_widget(self.label2)
            self.layout.add_widget(self.label3)

        self.add_widget(self.layout)




connection.commit()
connection.close()