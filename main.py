
'''
pips
pip install pyowm
pip install pyTelegramBotAPI
pip install beautifulsoup4
pip install lxml
pip install requests
'''

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('07c8001ef0edd2097a8484787beae918', config_dict)


import telebot
from telebot import types
bot = telebot.TeleBot("5330204968:AAHcsTomKw2-hZbrzgBDm1fIWC0S9fh77vM")

import bs4
from bs4 import BeautifulSoup
import lxml

import requests

import xml.etree.ElementTree as ET

def weatherchek(place):

    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    weather = observation.weather
    observation = mgr.weather_at_place(place).weather
    temp = observation.temperature('celsius')
    answer = ("В городе " + place + "  сейчас: " + str(weather.detailed_status) + '\n'
              + "Фактическая температура на улице: " + str(temp['temp']) + " градусов.")
    return answer

def zsingpars(zsinghref):
    global answerzsing
    url = ('https://www.astrostar.ru/horoscopes/main/' + zsinghref + '/day.html')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.find_all('p')
    answerzsing = (divs[0].text) + '\n' + (divs[1].text) +  '\n' + (divs[2].text)
    return answerzsing

def currencyrate(valueid):
    urlofrate = 'https://www.cbr-xml-daily.ru/daily_utf8.xml'
    response = requests.get(urlofrate)
    response.encoding ='utf-8'
    root = ET.fromstring(response.content)
    answercrate = ''
    for valute in root.findall("Valute[@ID='" + valueid + "']"):
        charcode = valute.find('CharCode').text
        name = valute.find('Name').text
        value = valute.find('Value').text.replace(',', '.')
        answercrate = ("Курс от ЦБ РФ: \n" + charcode + " " + name + "\n" + str(round(float(value), 2)) + " руб.")
    return answercrate


def currencyrateall():
    urlofrate = 'https://www.cbr-xml-daily.ru/daily_utf8.xml'
    response = requests.get(urlofrate)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.content)
    answerli = []
    for valute in root.findall("Valute"):
        charcode = valute.find('CharCode').text
        name = valute.find('Name').text
        value = valute.find('Value').text.replace(',', '.')
        val = float(value)
        va1 = round(val, 2)
        answerli.append(charcode + ' ' + name + '\n' + str(va1) + ' руб.')
    answercrateall = ("")
    for i in range(len(answerli)):
        answercrateall = (answercrateall + answerli[i] + "\n")
    return answercrateall


@bot.message_handler(commands=["start", "help"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btweath = types.KeyboardButton("Погода")
    bthoros = types.KeyboardButton("Гороскоп")
    btcrate = types.KeyboardButton("Курсы валют")
    btstart = types.KeyboardButton("Главное меню")
    bthelp = types.KeyboardButton("Помощь")
    markup.add(btweath, bthoros, btcrate, bthelp)
    bot.send_message(message.chat.id, text="Вы в главном меню", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def func(message):
        if (message.text == "Погода"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Новгород")
            btn2 = types.KeyboardButton("Питер")
            btn3 = types.KeyboardButton("Москва")
            btn4 = types.KeyboardButton("Арх")
            markup.add(btn1, btn2)
            markup.add(btn3, btn4)
            markup.add(btstart, bthelp)
            bot.send_message(message.chat.id, text="Выбери город:", reply_markup=markup)
        elif (message.text == "Главное меню"):
            start(message)
        elif (message.text == "Помощь"):
            helpmes = ('''Вы можете помочь разработке
            Отправть пожелания по изменению функционала:
            @IofakhNakh

            Помочь финансово:
            Карта Тинькофф:
            2200 7001 4130 4385
            ''')
            bot.send_message(message.chat.id, helpmes)
        elif (message.text == "Новгород"):
            place = ('Великий Новгород')
            bot.send_message(message.chat.id, weatherchek(place))
        elif (message.text == "Питер"):
            place = ('Санкт-Петербург')
            bot.send_message(message.chat.id, weatherchek(place))
        elif (message.text == "Москва"):
            place = ('Москва')
            bot.send_message(message.chat.id, weatherchek(place))
        elif (message.text == "Арх"):
            place = ('Архангельск')
            bot.send_message(message.chat.id, weatherchek(place))
        elif (message.text == "Гороскоп"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            gbtn1 = types.KeyboardButton("♈️ Овен")
            gbtn2 = types.KeyboardButton("♉️ Телец")
            gbtn3 = types.KeyboardButton("♊️ Близницы")
            gbtn4 = types.KeyboardButton("♋️ Рак")
            gbtn5 = types.KeyboardButton("♌️ Лев")
            gbtn6 = types.KeyboardButton("♍️ Дева")
            gbtn7 = types.KeyboardButton("♎️ Весы")
            gbtn8 = types.KeyboardButton("♏️ Скорпион")
            gbtn9 = types.KeyboardButton("♐️ Стрелец")
            gbtn10 = types.KeyboardButton("♑️ Козерог")
            gbtn11 = types.KeyboardButton("♒️ Водолей")
            gbtn12 = types.KeyboardButton("♓️ Рыбы")
            markup.add(gbtn1, gbtn2, gbtn3, gbtn4, gbtn5, gbtn6, gbtn7, gbtn8, gbtn9, gbtn10, gbtn11, gbtn12)
            markup.add(btstart, bthelp)
            bot.send_message(message.chat.id, text="Знак зодиака", reply_markup=markup)
        elif (message.text == "♈️ Овен"):
            zsinghref = ('oven')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♉️ Телец"):
            zsinghref = ('telets')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♊️ Близницы"):
            zsinghref = ('bliznetsi')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♋️ Рак"):
            zsinghref = ('rac')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♌️ Лев"):
            zsinghref = ('lev')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♍️ Дева"):
            zsinghref = ('deva')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♎️ Весы"):
            zsinghref = ('vesy')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♏️ Скорпион"):
            zsinghref = ('scorpion')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♐️ Стрелец"):
            zsinghref = ('strelets')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♑️ Козерог"):
            zsinghref = ('kozerog')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♒️ Водолей"):
            zsinghref = ('vodoley')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "♓️ Рыбы"):
            zsinghref = ('riby')
            bot.send_message(message.chat.id, zsingpars(zsinghref))
        elif (message.text == "Курсы валют"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rbtn1 = types.KeyboardButton("Доллар США")  # {'ID': 'R01235'} USD Доллар США
            rbtn2 = types.KeyboardButton("Евро")  # {'ID': 'R01239'} EUR Евро
            rbtn3 = types.KeyboardButton(
                "Фунт стерлингов Соединенного королевства")  # {'ID': 'R01035'} GBP Фунт стерлингов Соединенного королевства
            rbtn4 = types.KeyboardButton("Белорусский рубль")  # {'ID': 'R01090B'} BYN Белорусский рубль
            rbtn5 = types.KeyboardButton("Украинских гривен")  # {'ID': 'R01720'} UAH Украинских гривен
            rbtn6 = types.KeyboardButton("Китайский юань")  # {'ID': 'R01375'} CNY Китайский юань
            rbtnall = types.KeyboardButton("Все курсы ЦБ РФ")
            markup.add(rbtn1, rbtn2, rbtn3)
            markup.add(rbtn4, rbtn5, rbtn6)
            markup.add(rbtnall)
            markup.add(btstart, bthelp)
            bot.send_message(message.chat.id, text="Выбери вадюту", reply_markup=markup)
        elif (message.text == "Доллар США"):
            valueid = ('R01235')
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif (message.text == "Евро"):
            valueid = ('R01239')
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif (message.text == "Фунт стерлингов Соединенного королевства"):
            valueid = ('R01035')
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif (message.text == "Белорусский рубль"):
            valueid = ('R01090B')
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif (message.text == "Украинских гривен"):
            valueid = ('R01720')
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif (message.text == "Китайский юань"):
            valueid = ('R01375')
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif (message.text == "Все курсы ЦБ РФ"):
            bot.send_message(message.chat.id, currencyrateall())


bot.polling()