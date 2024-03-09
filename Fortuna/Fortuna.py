import kivy
import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.lang import Builder
from functools import partial
import json
import os

#Custom Builder
Builder.load_string('''
<HPProgressBar>:
    canvas:
        Clear
        Color:
            rgba: 1, 0, 0, 0.5
        Rectangle:
            pos: self.pos
            size: self.size[0],self.height
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size[0] * self.value_normalized, self.height
<SPProgressBar>:
    canvas:
        Clear
        Color:
            rgba: 0.298, 0.545, 0.855, 0.5
        Rectangle:
            pos: self.pos
            size: self.size[0],self.height
        Color:
            rgba: 0.298, 0.545, 0.855, 1
        Rectangle:
            pos: self.pos
            size: self.size[0] * self.value_normalized, self.height
''')

#Keinar Zepher Custom Features
class NameInput(TextInput):
    max_characters = 9
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring=''
        return super().insert_text(substring, from_undo)
class AddOnInput(TextInput):
    max_characters = 15
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring=''
        return super().insert_text(substring, from_undo)
class SignatureInput(TextInput):
    max_characters = 27
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring=''
        return super().insert_text(substring, from_undo)  
class HPProgressBar(ProgressBar):
    pass
class SPProgressBar(ProgressBar):
    pass

#Data
class database():
    add_on = [
        {'name': 'Almighty Soul', 'price':50 ,'purchased':False},
        {'name': 'Spiritual Soul', 'price':50 ,'purchased':False},
        {'name': 'Elemental Soul', 'price':50 ,'purchased':False},
        {'name': 'dlc', 'price':600 ,'purchased':False},
        {'name': 'Leader', 'price':1000 ,'purchased':False}
    ]
    current_title_screen = 'start'
    music_volume = 0.5
    sfx_volume = 0.5
    karma = 60
    language = 'English'
    gamedata = {
        'day name counter': 2,
        'day': 29,
        'month': 2,
        'year': 200,
        'money': 0,
        'current screen': 'dungeon',
        'player':{
            'name': 'Indra',
            'level': 1,
            'hp': 100,
            'max hp': 100,
            'health': 200,
            'max health': 200,
            'sp': 100,
            'max sp': 100,
            'soul': 200,
            'max soul': 200,
            'str': 6,
            'int': 6,
            'dex': 6,
            'vit': 6,
            'wil': 6,
            'agi': 6,
            'bonus': 20
        },
        'left ally':{
            'name': 'Dankun',
            'source': '.sprite/cultist.png',
            'distance': 12,
            'position': 'behind',
            'hp': 100,
            'max hp': 100,
            'health': 200,
            'max health': 200,
            'sp': 100,
            'max sp': 100,
            'soul': 200,
            'max soul': 200,
            'str': 6,
            'int': 6,
            'dex': 6,
            'vit': 6,
            'wil': 6,
            'agi': 6,
            'bonus': 20
        },
        'right ally':{},
        'left enemy':{},
        'mid enemy':{},
        'right enemy':{}
    }
class reset():
    gamedata = {
        'day': 1,
        'current screen': 'dungeon',
        'player':{
            'name': 'Indra',
            'level': 1,
            'hp': 1,
            'max hp': 1,
            'health': 1,
            'max health': 1,
            'sp': 1,
            'max sp': 1,
            'soul': 1,
            'max soul': 1
        },
        'left ally':{},
        'right ally':{},
        'left enemy':{},
        'mid enemy':{},
        'right enemy':{}
    }

#Screen
class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        #Main UI
        self.main_layout = BoxLayout(orientation='vertical')
        #Header UI
        self.header_layout = BoxLayout(size_hint=(1,0.15))
        #Body UI
        self.body_layout = RelativeLayout()
        self.option_body_layout = BoxLayout(orientation='vertical')
        self.hidden_button_layout = BoxLayout(orientation='vertical')
        self.language_layout = BoxLayout(size_hint=(1,0.5))
        self.english_button = Button(text='English', on_release=self.english, background_color=(0.6196,0.6118,0.7137,1))
        self.indonesia_button = Button(text='Indonesia', on_release=self.indonesia, background_color=(0.6196,0.6118,0.7137,1))
        self.language_layout.add_widget(self.indonesia_button)
        self.language_layout.add_widget(self.english_button)
        self.hall_of_memories = BoxLayout(size_hint=(1,0.7))
        self.memory_layout = BoxLayout(orientation='vertical')
        self.grid_title = BoxLayout(spacing=0, size_hint_y=None)
        self.memories_shop = ScrollView()
        self.add_on_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.add_on_grid.bind(minimum_height=self.add_on_grid.setter('height'))
        self.hidden_layout = BoxLayout(orientation='vertical')
        #Button UI
        self.button_layout = BoxLayout(size_hint=(1,0.15))
        #Footer UI
        self.footer_layout = BoxLayout(size_hint=(1,0.15))
    def on_enter(self, *args):
        self.count = 0
        if database.current_title_screen == 'start':
            Clock.schedule_once(self.ouroquad, 0)
        elif database.current_title_screen == 'title':
            Clock.schedule_once(self.title, 0)
        elif database.current_title_screen == 'option':
            Clock.schedule_once(self.option, 0)
        else:
            self.clear_widgets()
            self.add_widget(Label(text='please not edit this game code'))
    def ouroquad(self, instance):
        self.clear_widgets()
        ouroquad = Image(source='.background/OuroQuad.png', opacity=0)
        self.add_widget(ouroquad)
        animation = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=2)
        animation.start(ouroquad)
        Clock.schedule_once(self.title, 4)
    def title(self, instance):
        database.current_title_screen = 'title'
        self.clear_widgets()
        self.main_layout.clear_widgets()
        self.body_layout.clear_widgets()
        self.button_layout.clear_widgets()
        self.footer_layout.clear_widgets()
        self.hidden_button_layout.clear_widgets()
        self.main_layout.add_widget(self.body_layout)
        self.main_layout.add_widget(self.button_layout)
        self.main_layout.add_widget(self.footer_layout)
        self.add_widget(self.main_layout)
        self.body_layout.add_widget(Label(text='Fortuna', font_size=60))
        self.body_layout.add_widget(self.hidden_button_layout)
        self.hidden_button_layout.add_widget(Label())
        self.hidden_button_layout.add_widget(Label())
        self.hidden_button_layout.add_widget(Label())
        if database.language == 'English':
            text_1 = 'play game'
            text_2 = 'option'
        else:
            text_1 = 'mulai permainan'
            text_2 = 'pengaturan'
        self.hidden_button_layout.add_widget(Button(text=text_1, size_hint=(1,0.5), background_color=(1,1,1,0), on_release=self.hall_of_memories_menu))
        self.hidden_button_layout.add_widget(Button(text=text_2, size_hint=(1,0.5), background_color=(1,1,1,0), on_release=self.option))
        if hasattr(self, 'music') and self.music:
            pass
        else:
            Clock.schedule_once(self.start_music, 0)
    def start_music(self, dt):
        self.music = SoundLoader.load('.bgm/event.mp3')
        self.music.volume = database.music_volume
        self.music.play()
        self.music.loop = True
    def on_leave(self, *args):
        if hasattr(self, 'music') and self.music:
            Clock.schedule_once(self.fade_stop, 0)
    def fade_stop(self, dt):
        if self.music.volume > 0.1:
            self.music.volume -= 0.1
            Clock.schedule_once(self.fade_stop, 0.2)
        else:
            self.music.stop()
            self.music.loop = False
            self.music.volume = 1.0
    def option(self, instance):
        self.clear_widgets()
        self.main_layout.clear_widgets()
        self.header_layout.clear_widgets()
        self.option_body_layout.clear_widgets()
        self.button_layout.clear_widgets()
        self.footer_layout.clear_widgets()
        self.main_layout.add_widget(self.header_layout)
        self.main_layout.add_widget(self.option_body_layout)
        self.main_layout.add_widget(self.button_layout)
        self.main_layout.add_widget(self.footer_layout)
        self.add_widget(self.main_layout)
        self.music_slider = Slider(min=0,max=1, value=self.music.volume, size_hint=(1,0.5))
        self.music_slider.bind(value=self.on_music_volume_change)
        self.sfx_slider = Slider(min=0,max=1, value=database.sfx_volume, size_hint=(1,0.5))
        self.sfx_slider.bind(value=self.on_sfx_volume_change)
        bgm = self.music.volume * 100
        bgm = int(bgm)
        sfx = database.sfx_volume * 100
        sfx = int(sfx)
        if database.language == 'English':
            self.header_layout.add_widget(Label(text='Option'))
            self.footer_layout.add_widget(Button(text='Back', on_release=self.title, background_color=(0.6196,0.6118,0.7137,1)))
            self.option_body_layout.add_widget(Label(text='Language', size_hint=(1,0.5)))
            self.option_body_layout.add_widget(self.language_layout)
            self.option_body_layout.add_widget(Label(text=f'BGM Volume: {bgm}%', size_hint=(1,0.5)))
            self.option_body_layout.add_widget(self.music_slider)
            self.option_body_layout.add_widget(Label(text=f'SFX Volume: {sfx}%', size_hint=(1,0.5)))
            self.option_body_layout.add_widget(self.sfx_slider)
            self.button_layout.add_widget(Button(text='Default Setting', on_release=self.reset_setting, background_color=(0.6196,0.6118,0.7137,1)))
        else:
            self.header_layout.add_widget(Label(text='Pengaturan'))
            self.footer_layout.add_widget(Button(text='Kembali', on_release=self.title, background_color=(0.6196,0.6118,0.7137,1)))
            self.option_body_layout.add_widget(Label(text='Bahasa', size_hint=(1,0.5)))
            self.option_body_layout.add_widget(self.language_layout)
            self.option_body_layout.add_widget(Label(text=f'Volume BGM: {bgm}%', size_hint=(1,0.5)))
            self.option_body_layout.add_widget(self.music_slider)
            self.option_body_layout.add_widget(Label(text=f'Volume SFX: {sfx}%', size_hint=(1,0.5)))
            self.option_body_layout.add_widget(self.sfx_slider)
            self.button_layout.add_widget(Button(text='Reset Pengaturan', on_release=self.reset_setting, background_color=(0.6196,0.6118,0.7137,1)))
        self.option_body_layout.add_widget(Label())
    def english(self, instance):
        database.language = 'English'
        Clock.schedule_once(self.option, 0)
    def indonesia(self, instance):
        database.language = 'Indonesia'
        Clock.schedule_once(self.option, 0)
    def on_music_volume_change(self, instance, value):
        self.music.volume = value
        database.music_volume = value
        Clock.schedule_once(self.option, 0)
    def on_sfx_volume_change(self, instance, value):
        database.sfx_volume = value
        Clock.schedule_once(self.option, 0)
    def reset_setting(self, instance):
        self.music.volume = 0.5
        database.music_volume = 0.5
        database.sfx_volume = 0.5
        Clock.schedule_once(self.option, 0)
    def hall_of_memories_menu(self, instance):
        self.clear_widgets()
        self.main_layout.clear_widgets()
        self.header_layout.clear_widgets()
        self.body_layout.clear_widgets()
        self.option_body_layout.clear_widgets()
        self.button_layout.clear_widgets()
        self.footer_layout.clear_widgets()
        self.hall_of_memories.clear_widgets()
        self.memory_layout.clear_widgets()
        self.add_on_grid.clear_widgets()
        self.memories_shop.clear_widgets()
        self.grid_title.clear_widgets()
        self.hidden_layout.clear_widgets()
        self.hidden_button_layout.clear_widgets()
        self.main_layout.add_widget(self.header_layout)
        self.main_layout.add_widget(self.option_body_layout)
        self.main_layout.add_widget(self.button_layout)
        self.main_layout.add_widget(self.footer_layout)
        self.add_widget(self.main_layout)
        self.header_layout.add_widget(Label(text='Hall of Memories'))
        self.hall_of_memories.add_widget(Image(source='.sprite/cultist.png'))
        if database.language == 'English':
            no_savedata = 'No Savedata'
            start_text= 'Start Game'
            footer_text='Title Screen'
            delete_savedata_text = 'Delete Savedata'
            add_on_shop = 'Add-On Shop'
            mysterious_person = '-- Mysterious Man --'
            quote_list = [
                'death just one way to escape from life',
                'what do you think?',
                '.....',
                'you can buy add-on with karma',
                'the highest difficult has a special boss'
            ]
        else:
            no_savedata = 'Tak Ada Data Save'
            start_text= 'Mulai Permainan'
            delete_savedata_text = 'Hapus data save'
            footer_text='Layar Judul'
            add_on_shop ='Toko Add-On'
            mysterious_person = '-- Pria Misterius --'
            quote_list = [
                'kematian adalah salah satu cara untuk\nkabur dari kehidupan'
                'apa yang kamu pikirkan?',
                '.....',
                'kamu dapat membeli add-on dengan karma',
                'tingkat kesulitan tertinggi\nmemiliki boss spesial'
            ]
        random_number = random.randint(0,len(quote_list)-1)
        quote = quote_list[random_number]
        if database.gamedata == {}:
            self.memory_layout.add_widget(Label(text=no_savedata))
            self.memory_layout.add_widget(Button(text=start_text, on_release=self.start_game, background_color=(0.6196,0.6118,0.7137,1)))
            self.memory_layout.add_widget(Label())
        else:
            level = database.gamedata['player']['level']
            name = database.gamedata['player']['name']
            self.memory_layout.add_widget(Label(text=f'Lv {level} {name}'))
            self.memory_layout.add_widget(Button(text=start_text, on_release=self.start_game, background_color=(0.6196,0.6118,0.7137,1)))
            self.memory_layout.add_widget(Button(text=delete_savedata_text, on_release=self.delete_savedata, background_color=(0.6196,0.6118,0.7137,1)))
        self.hall_of_memories.add_widget(self.memory_layout)
        self.option_body_layout.add_widget(self.hall_of_memories)
        self.grid_title.add_widget(Label(size_hint_y=None, height=100))
        self.option_body_layout.add_widget(self.grid_title)
        self.hidden_layout.add_widget(Label(text=mysterious_person))
        self.hidden_layout.add_widget(Label(text=quote))
        self.hidden_layout.add_widget(Label())
        self.option_body_layout.add_widget(self.hidden_layout)
        self.button_layout.add_widget(Button(text=add_on_shop, on_release=self.hall_of_memories_karma_shop, background_color=(0.6196,0.6118,0.7137,1)))
        self.footer_layout.add_widget(Button(text=footer_text, on_release=self.title, background_color=(0.6196,0.6118,0.7137,1)))
    def hall_of_memories_karma_shop(self, instance):
        self.clear_widgets()
        self.main_layout.clear_widgets()
        self.header_layout.clear_widgets()
        self.option_body_layout.clear_widgets()
        self.button_layout.clear_widgets()
        self.footer_layout.clear_widgets()
        self.hall_of_memories.clear_widgets()
        self.memory_layout.clear_widgets()
        self.add_on_grid.clear_widgets()
        self.memories_shop.clear_widgets()
        self.grid_title.clear_widgets()
        self.main_layout.add_widget(self.header_layout)
        self.main_layout.add_widget(self.option_body_layout)
        self.main_layout.add_widget(self.button_layout)
        self.main_layout.add_widget(self.footer_layout)
        self.add_widget(self.main_layout)
        self.header_layout.add_widget(Label(text='Hall of Memories Shop'))
        self.hall_of_memories.add_widget(Image(source='.sprite/cultist.png'))
        if database.language == 'English':
            shopkeeper = 'Mysterious Man'
            footer_text='Back'
            add_on_name = 'Name'
            add_on_price = 'Price'
            search_text = 'Search Add On'
        else:
            shopkeeper = 'Pria Misterius'
            footer_text='Kembali'
            add_on_name = 'Name'
            add_on_price = 'Harga'
            search_text = 'Cari Add On'
        self.memory_layout.add_widget(Label(text=shopkeeper))
        self.add_on_search = AddOnInput(hint_text=search_text, multiline=False, size_hint=(1,None), size=(1,50), halign='center')
        self.add_on_search.bind(text=self.on_search_change)             
        self.memory_layout.add_widget(self.add_on_search)
        self.memory_layout.add_widget(Label())
        self.grid_title.add_widget(Label(text=add_on_name, size_hint_y=None, height=100))
        self.grid_title.add_widget(Label(text=add_on_price, size_hint_y=None, size_hint_x=0.5, height=100))
        self.hall_of_memories.add_widget(self.memory_layout)
        self.memories_shop.add_widget(self.add_on_grid)
        self.option_body_layout.add_widget(self.hall_of_memories)
        self.option_body_layout.add_widget(self.grid_title)
        self.option_body_layout.add_widget(self.memories_shop)
        self.button_layout.add_widget(Label(text=f'Karma: {database.karma}'))
        self.footer_layout.add_widget(Button(text=footer_text, on_release=self.hall_of_memories_menu, background_color=(0.6196,0.6118,0.7137,1)))
        self.show_add_on_list()
    def buy_add_on(self, name):
        for item in database.add_on:
            if item['name'] == name:
                if database.karma >= item['price']:
                    database.karma = database.karma - item['price']
                    item['purchased'] = True
                Clock.schedule_once(self.hall_of_memories_karma_shop, 0)
                break
    def on_search_change(self, instance, value):
        self.filter_add_on(value)
    def show_add_on_list(self):
        self.add_on_grid.clear_widgets()
        if database.language == 'English':
            purchased_text = 'Purchased'
        else:
            purchased_text = 'Telah Dibeli'
        for item in database.add_on:
            self.add_on_grid.add_widget(Label(text=str(item['name']), size_hint_y=None, height=100))
            if item['purchased'] == True:
                self.add_on_grid.add_widget(Label(text=purchased_text, size_hint_y=None, height=100, size_hint_x=0.5))
            else:
                self.add_on_grid.add_widget(Button(text=str(item['price']), size_hint_y=None, height=100, size_hint_x=0.5, on_release=lambda instance, item=item: self.buy_add_on(item['name']), background_color=(0.6196,0.6118,0.7137,1)))
    def filter_add_on(self,search):
        self.add_on_grid.clear_widgets()
        self.add_on_grid.clear_widgets()
        if database.language == 'English':
            purchased_text = 'Purchased'
        else:
            purchased_text = 'Telah Dibeli'
        filtered_item = [item for item in database.add_on if search.lower() in item['name'].lower()]
        for item in filtered_item :
            self.add_on_grid.add_widget(Label(text=str(item['name']), size_hint_y=None, height=100))
            if item['purchased'] == True:
                self.add_on_grid.add_widget(Label(text=purchased_text, size_hint_y=None, height=100, size_hint_x=0.5))
            else:
                self.add_on_grid.add_widget(Button(text=str(item['price']), size_hint_y=None, height=100, size_hint_x=0.5, on_release=lambda instance, item=item: self.buy_add_on(item['name']), background_color=(0.6196,0.6118,0.7137,1)))
    def delete_savedata(self, instance):
        database.gamedata = {}
        Clock.schedule_once(self.hall_of_memories_menu, 0)
    def start_game(self, instance):
        self.manager.current = 'Dungeon Screen'
class DungeonScreen(Screen):
    def __init__(self, **kwargs):
        super(DungeonScreen, self).__init__(**kwargs)
        #Main UI
        self.main_layout = BoxLayout(orientation='vertical')
        #Header UI
        self.header_layout = BoxLayout(size_hint=(1,0.1))
        self.day_date_layout = BoxLayout(orientation='vertical')
        self.header_layout.add_widget(self.day_date_layout)
        self.header_layout.add_widget(Button(text='Menu', size_hint=(0.25,1), border=(2,2,2,2), background_color=(0.6196,0.6118,0.7137,1)))
        #Body UI
        self.body_layout = BoxLayout(orientation='vertical')
        self.top_screen_layout = RelativeLayout()
        self.bottom_screen_layout = RelativeLayout()
        self.body_layout.add_widget(self.top_screen_layout)
        self.body_layout.add_widget(self.bottom_screen_layout)

        #For Dungeon Path
        self.three_path_dungeon=BoxLayout(orientation='vertical')
        self.three_path_dungeon.add_widget(Label(size_hint=(0,0.3)))
        self.fill_path_dungeon=BoxLayout()
        self.left_box=RelativeLayout()
        self.left_box.add_widget(Button(border=(1,1,1,1), background_color=(0.6196,0.6118,0.7137,1)))
        self.left_path=GridLayout(cols=2)
        self.mid_box=RelativeLayout()
        self.mid_box.add_widget(Button(border=(1,1,1,1), background_color=(0.6196,0.6118,0.7137,1)))
        self.mid_path=GridLayout(cols=2)
        self.right_box=RelativeLayout()
        self.right_box.add_widget(Button(border=(1,1,1,1), background_color=(0.6196,0.6118,0.7137,1)))
        self.right_path=GridLayout(cols=2)
        self.left_box.add_widget(self.left_path)
        self.mid_box.add_widget(self.mid_path)
        self.right_box.add_widget(self.right_path)
        self.fill_path_dungeon.add_widget(self.left_box)
        self.fill_path_dungeon.add_widget(self.mid_box)
        self.fill_path_dungeon.add_widget(self.right_box)
        self.three_path_dungeon.add_widget(self.fill_path_dungeon)
        self.three_path_dungeon.add_widget(Label(size_hint=(0,0.3)))

        #To Show Party
        self.party_layout = BoxLayout()
        self.left_party_slot = BoxLayout(orientation='vertical')
        self.self_party_slot = BoxLayout(orientation='vertical')
        self.right_party_slot = BoxLayout(orientation='vertical')
        self.party_layout.add_widget(self.left_party_slot)
        self.party_layout.add_widget(self.self_party_slot)
        self.party_layout.add_widget(self.right_party_slot)
        self.left_party_bar = BoxLayout(orientation='vertical', size_hint_y=0.4)
        self.self_party_bar = BoxLayout(orientation='vertical', size_hint_y=0.4)
        self.right_party_bar = BoxLayout(orientation='vertical', size_hint_y=0.4)

        #Button UI
        self.button_layout = BoxLayout(size_hint=(1,0.15))
        #Footer UI
        self.footer_layout = BoxLayout(size_hint=(1,0.15))
        #return main layout
        self.add_widget(self.main_layout)
    def on_enter(self, *args):
        if database.gamedata['current screen'] == 'dungeon':
            Clock.schedule_once(self.explore_dungeon_screen, 0)
    def next_day(self, *args):
        the_day = database.gamedata['day'] + 1
        the_month = database.gamedata['month']
        the_year = database.gamedata['year']
        if the_month in (1,3,5,7,8,10,12):
            if the_day > 31:
                database.gamedata['day'] = 1
                the_month = database.gamedata['month'] + 1
                if the_month > 12:
                    database.gamedata['month'] = 1
                    database.gamedata['year'] = database.gamedata['year'] + 1
            else:
                database.gamedata['day'] = the_day
        elif the_month == 2:
            if the_year % 4 == 0:
                if the_day > 29:
                    database.gamedata['day'] = 1
                    the_month = database.gamedata['month'] + 1
                    if the_month > 12:
                        database.gamedata['month'] = 1
                        database.gamedata['year'] = database.gamedata['year'] + 1
                else:
                    database.gamedata['day'] = the_day
            else:
                if the_day > 28:
                    database.gamedata['day'] = 1
                    the_month = database.gamedata['month'] + 1
                    if the_month > 12:
                        database.gamedata['month'] = 1
                        database.gamedata['year'] = database.gamedata['year'] + 1
                else:
                    database.gamedata['day'] = the_day
        else:
            if the_day > 30:
                database.gamedata['day'] = 1
                the_month = database.gamedata['month'] + 1
                if the_month > 12:
                    database.gamedata['month'] = 1
                    database.gamedata['year'] = database.gamedata['year'] + 1
            else:
                database.gamedata['day'] = the_day
        day_name = database.gamedata['day name counter'] + 1
        if day_name > 7:
            database.gamedata['day name counter'] = 1
        else:
            database.gamedata['day name counter'] = day_name
    def update_header(self, *args):
        self.day_date_layout.clear_widgets()
        if database.language == 'English':
            day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        else:
            day_names = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']
        current_day_name = day_names[database.gamedata['day name counter']]
        the_day = database.gamedata['day']
        the_month = database.gamedata['month']
        the_year = database.gamedata['year']
        self.day_date_layout.add_widget(Label(text=f'{current_day_name}, {the_day}/{the_month}/{the_year}'))
        the_money = database.gamedata['money']
        self.day_date_layout.add_widget(Label(text=f'{the_money} FC'))
    def show_party(self, *args):
        self.left_party_slot.clear_widgets()
        self.left_party_bar.clear_widgets()
        if database.gamedata['left ally'] != {}:
            self.left_party_bar.add_widget(Label(text=database.gamedata['left ally']['name'], bold=True))
            distance = database.gamedata['left ally']['distance']
            self.left_party_bar.add_widget(Label(text=f'{distance} ft'))
            self.left_party_bar.add_widget(Label(text=database.gamedata['left ally']['position']))
            self.left_party_slot.add_widget(self.left_party_bar)
            self.left_party_slot.add_widget(Image(source=database.gamedata['left ally']['source']))
        self.self_party_slot.clear_widgets()
        self.self_party_bar.clear_widgets()
        self.self_party_bar.add_widget(Label(text=database.gamedata['player']['name'], bold=True))
        current_hp = database.gamedata['player']['hp']
        max_hp = database.gamedata['player']['max hp']
        self.self_party_bar.add_widget(Label(text=f'{current_hp}/{max_hp}'))
        self.self_party_bar.add_widget(HPProgressBar(value=(current_hp*100/max_hp), max=100, size_hint=(1, 0.1)))
        current_sp = database.gamedata['player']['sp']
        max_sp = database.gamedata['player']['max sp']
        self.self_party_bar.add_widget(Label(text=f'{current_sp}/{max_sp}'))
        self.self_party_bar.add_widget(SPProgressBar(value=(current_sp*100/max_sp), max=100, size_hint=(1, 0.1)))
        self.self_party_slot.add_widget(self.self_party_bar)
        self.self_party_slot.add_widget(Image(source='.sprite/mc.png'))
        self.right_party_slot.clear_widgets()
        self.right_party_bar.clear_widgets()
        if database.gamedata['right ally'] != {}:
            self.right_party_bar.add_widget(Label(text=database.gamedata['right ally']['name'], bold=True))
            distance = database.gamedata['right ally']['distance']
            self.right_party_bar.add_widget(Label(text=f'{distance} ft'))
            self.right_party_bar.add_widget(Label(text=database.gamedata['right ally']['position']))
            self.right_party_slot.add_widget(self.right_party_bar)
            self.right_party_slot.add_widget(Image(source=database.gamedata['right ally']['source']))
    def random_dungeon_path(self, *args):
        self.left_path.clear_widgets()
        count = 0
        number = random.randint(1,20)
        if number != 20:
            self.left_path.add_widget(Image(source='.icon/enemy.png'))
            count = count+1
        number = random.randint(1,10)
        if number <= 2:
            self.left_path.add_widget(Image(source='.icon/event.png'))
            count = count+1
        number = random.randint(1,20)
        if number <= 2:
            self.left_path.add_widget(Image(source='.icon/chest.png'))
            count = count+1
        elif number == 3:
            self.left_path.add_widget(Image(source='.icon/trap_chest.png'))
            count = count+1
        for i in range(4-count):
            self.left_path.add_widget(Label())
        count = 0
        self.mid_path.clear_widgets()
        number = random.randint(1,20)
        if number != 20:
            self.mid_path.add_widget(Image(source='.icon/enemy.png'))
            count = count+1
        number = random.randint(1,10)
        if number <= 2:
            self.mid_path.add_widget(Image(source='.icon/event.png'))
            count = count+1
        number = random.randint(1,20)
        if number <= 2:
            self.mid_path.add_widget(Image(source='.icon/chest.png'))
            count = count+1
        elif number == 3:
            self.mid_path.add_widget(Image(source='.icon/trap_chest.png'))
            count = count+1
        for i in range(4-count):
            self.mid_path.add_widget(Label())
        count = 0
        self.right_path.clear_widgets()
        number = random.randint(1,20)
        if number != 20:
            self.right_path.add_widget(Image(source='.icon/enemy.png'))
            count = count+1
        number = random.randint(1,10)
        if number <= 2:
            self.right_path.add_widget(Image(source='.icon/event.png'))
            count = count+1
        number = random.randint(1,20)
        if number <= 2:
            self.right_path.add_widget(Image(source='.icon/chest.png'))
            count = count+1
        elif number == 3:
            self.right_path.add_widget(Image(source='.icon/trap_chest.png'))
            count = count+1
        for i in range(4-count):
            self.right_path.add_widget(Label())
    def explore_dungeon_screen(self, instance):
        database.gamedata['current screen'] = 'dungeon'
        self.main_layout.clear_widgets()
        self.update_header()
        self.main_layout.add_widget(self.header_layout)
        self.top_screen_layout.clear_widgets()
        self.random_dungeon_path()
        self.top_screen_layout.add_widget(self.three_path_dungeon)
        self.bottom_screen_layout.clear_widgets()
        self.show_party()
        self.bottom_screen_layout.add_widget(self.party_layout)
        self.main_layout.add_widget(self.body_layout)
        self.button_layout.clear_widgets()
        if database.language == 'English':
            dungeon_text = 'Choose your path'
            preparation_text = 'Preparation'
        else:
            dungeon_text = 'Pilih jalan-mu'
            preparation_text = 'Persiapan'
        self.button_layout.add_widget(Label(text=dungeon_text))
        self.main_layout.add_widget(self.button_layout)
        self.footer_layout.clear_widgets()
        self.footer_layout.add_widget(Button(text=preparation_text, background_color=(0.6196,0.6118,0.7137,1), on_release=self.explore_dungeon_screen))
        self.main_layout.add_widget(self.footer_layout)
    def start_music(self, dt):
        self.music = SoundLoader.load('.bgm/event.mp3')
        self.music.volume = database.music_volume
        self.music.play()
        self.music.loop = True
    def on_leave(self, *args):
        if hasattr(self, 'music') and self.music:
            Clock.schedule_once(self.fade_stop, 0)
    def fade_stop(self, dt):
        if self.music.volume > 0.1:
            self.music.volume -= 0.1
            Clock.schedule_once(self.fade_stop, 0.2)
        else:
            self.music.stop()
            self.music.loop = False
            self.music.volume = 1.0

#Screen Manager
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name='Title Screen'))
        sm.add_widget(DungeonScreen(name='Dungeon Screen'))
        sm.current = 'Title Screen'
        return sm

if __name__ == '__main__':
    GameApp().run()