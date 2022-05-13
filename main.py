
"""
pips
pip install pyowm
pip install pyTelegramBotAPI
pip install beautifulsoup4
pip install lxml
pip install requests
"""

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

import telebot
from telebot import types

from bs4 import BeautifulSoup

import requests

import xml.etree.ElementTree as et

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('07c8001ef0edd2097a8484787beae918', config_dict)

bot = telebot.TeleBot("5330204968:AAHcsTomKw2-hZbrzgBDm1fIWC0S9fh77vM")

@bot.message_handler(commands=["start", "help"])


def weather_check(place):
    weather = owm.weather_manager().weather_at_place(place).weather
    weather_now = str(weather.detailed_status)
    temp_now = str(weather.temperature('celsius')['temp'])
    answer = f'В городе  {place}  сейчас:  {weather_now} \nФактическая температура на улице:  {temp_now}  градусов.'
    return answer


def z_sing_pars(z_sing_href):
    url = ('https://www.astrostar.ru/horoscopes/main/' + z_sing_href + '/day.html')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.find_all('p')
    answer_z_sing = divs[0].text + '\n' + divs[1].text + '\n' + divs[2].text
    return answer_z_sing


def currencyrate(valueid):
    urlofrate = 'https://www.cbr-xml-daily.ru/daily_utf8.xml'
    response = requests.get(urlofrate)
    response.encoding = 'utf-8'
    root = et.fromstring(response.content)
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
    root = et.fromstring(response.content)
    answerli = []
    for valute in root.findall("Valute"):
        charcode = valute.find('CharCode').text
        name = valute.find('Name').text
        value = valute.find('Value').text.replace(',', '.')
        val = float(value)
        va1 = round(val, 2)
        answerli.append(charcode + ' ' + name + '\n' + str(va1) + ' руб.')
    answercrateall = ""
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
        if message.text == "Погода":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Новгород")
            btn2 = types.KeyboardButton("Питер")
            btn3 = types.KeyboardButton("Москва")
            btn4 = types.KeyboardButton("Арх")
            markup.add(btn1, btn2)
            markup.add(btn3, btn4)
            markup.add(btstart, bthelp)
            bot.send_message(message.chat.id, text="Выбери город:", reply_markup=markup)
        elif message.text == "Главное меню":
            start(message)
        elif message.text == "Помощь":
            helpmes = ('''Вы можете помочь разработке
            Отправть пожелания по изменению функционала:
            @IofakhNakh

            Помочь финансово:
            Карта Тинькофф:
            2200 7001 4130 4385
            ''')
            bot.send_message(message.chat.id, helpmes)
        elif message.text == "Новгород":
            place = 'Великий Новгород'
            bot.send_message(message.chat.id, weather_check(place))
        elif message.text == "Питер":
            place = 'Санкт-Петербург'
            bot.send_message(message.chat.id, weather_check(place))
        elif message.text == "Москва":
            place = 'Москва'
            bot.send_message(message.chat.id, weather_check(place))
        elif message.text == "Арх":
            place = 'Архангельск'
            bot.send_message(message.chat.id, weather_check(place))
        elif message.text == "Гороскоп":
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
        elif message.text == "♈️ Овен":
            z_sing_href = 'oven'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♉️ Телец":
            z_sing_href = 'telets'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♊️ Близницы":
            z_sing_href = 'bliznetsi'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♋️ Рак":
            z_sing_href = 'rac'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♌️ Лев":
            z_sing_href = 'lev'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♍️ Дева":
            z_sing_href = 'deva'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♎️ Весы":
            z_sing_href = 'vesy'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♏️ Скорпион":
            z_sing_href = 'scorpion'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♐️ Стрелец":
            z_sing_href = 'strelets'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♑️ Козерог":
            z_sing_href = 'kozerog'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♒️ Водолей":
            z_sing_href = 'vodoley'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "♓️ Рыбы":
            z_sing_href = 'riby'
            bot.send_message(message.chat.id, z_sing_pars(z_sing_href))
        elif message.text == "Курсы валют":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rbtn1 = types.KeyboardButton("Доллар США")
            rbtn2 = types.KeyboardButton("Евро")
            rbtn3 = types.KeyboardButton(
                "Фунт стерлингов Соединенного королевства")
            rbtn4 = types.KeyboardButton("Белорусский рубль")
            rbtn5 = types.KeyboardButton("Украинских гривен")
            rbtn6 = types.KeyboardButton("Китайский юань")
            rbtnall = types.KeyboardButton("Все курсы ЦБ РФ")
            markup.add(rbtn1, rbtn2, rbtn3)
            markup.add(rbtn4, rbtn5, rbtn6)
            markup.add(rbtnall)
            markup.add(btstart, bthelp)
            bot.send_message(message.chat.id, text="Выбери вадюту", reply_markup=markup)
        elif message.text == "Доллар США":
            valueid = 'R01235'
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif message.text == "Евро":
            valueid = 'R01239'
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif message.text == "Фунт стерлингов Соединенного королевства":
            valueid = 'R01035'
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif message.text == "Белорусский рубль":
            valueid = 'R01090B'
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif message.text == "Украинских гривен":
            valueid = 'R01720'
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif message.text == "Китайский юань":
            valueid = 'R01375'
            bot.send_message(message.chat.id, currencyrate(valueid))
        elif message.text == "Все курсы ЦБ РФ":
            bot.send_message(message.chat.id, currencyrateall())


bot.polling()
