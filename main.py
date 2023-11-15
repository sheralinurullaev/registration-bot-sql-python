import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('токен бота')

login = None

@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('database.db')
    crs = connect.cursor()
    
    crs.execute("""CREATE TABLE IF DONT EXIST users(
                id INT AUTO_INCREMENT,
                login VARCHAR(50),
                password VARCHAR(50),
                PRIMARY KEY(id)
    )""")

    connect.commit()
    crs.close()
    bot.send_message(message.chat.id, 'Здравствуйте уважаемый пользователь, для начала нужно зарегестрироваться введите свой логин для регистрации!')
    bot.register_next_step_handler(message, login)

def login(message):
    global login
    login = message.text.strip()
    bot.send_message(message.chat.id, 'Теперь введите пароль!')
    bot.register_next_step_handler(message, password)

def password(message):
    password = message.text.strip()
    connect = sqlite3.connect('database.db')
    crs = connect.cursor()
    
    crs.execute("INSERT INTO users(login, password) VALUES('%s', '%s')" % (login, password))

    connect.commit()
    crs.close()   

    bot.send_message(message.chat.id, 'Приятной вам работы, вы успешно зарегестрированы!')

bot.infinity_polling()
