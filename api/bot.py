import telebot
from telebot import types
from telebot.types import Message
import random
import string
import urllib
import os
from core.bot import *
from core.settings import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

REGISTER = 'Регистрация'
LOGIN = 'Войти'
MY_TASKS = 'Мои задания'
LOGOUT = 'Выйти'
CAT = 'Котик'
DOG = 'Собачка'
INVITE_TO_LOGIN = 'Введите логин и пароль: login/password'


def is_authenticate(message: Message):
    id = message.from_user.id
    return is_register(id) and bot.get_state(id, message.chat.id) == 'connected'


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    if(not is_register(message.from_user.id)):
        rkb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        rkb.add(types.KeyboardButton(REGISTER), types.KeyboardButton(LOGIN))
        msg_bot = bot.send_message(
            message.chat.id, f'Welcome {message.from_user.full_name}', reply_markup=rkb)
        bot.register_next_step_handler(msg_bot, get_user_answer)


def register_user(message: Message) -> dict:
    user = message.from_user.to_dict()
    uid = '_'.join(message.from_user.first_name.split(' '))
    uid = f'{uid}_{message.from_user.id}'.lower()
    password = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(8))
    user['password'] = password
    user['uid'] = uid
    users.append(user)
    msg = f'''
            Вы успешно зарегистрировались
            Ваш логин: {user['uid']}
            Ваш пароль: {user['password']}
            '''
    msg = bot.send_message(message.from_user.id, msg)
    bot.register_next_step_handler(msg, get_user_answer)


def invite_login(message: Message):
    msg = bot.send_message(message.from_user.id, INVITE_TO_LOGIN)
    bot.register_next_step_handler(msg, login)


def login(message: Message):
    content = message.text.split('/')
    if len(content) == 2:
        uid, password = content
        user = authenticate(uid, password)
        if user:
            bot.set_state(message.from_user.id, 'connected', message.chat.id)
            rkb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            rkb.add(types.KeyboardButton(MY_TASKS),
                    types.KeyboardButton(LOGOUT))
            msg = bot.send_message(message.from_user.id,
                                   'Успешно авторизованы!', reply_markup=rkb)
            bot.register_next_step_handler(msg, get_user_answer)
        else:
            bot.send_message(message.from_user.id,
                             f'логин или пароль неправильный')
    else:
        msg = bot.send_message(message.from_user.id, INVITE_TO_LOGIN)
        bot.register_next_step_handler(msg, login)


def logout(message: Message):
    bot.set_state(message.from_user.id, '', message.chat.id)
    users.clear()
    bot.send_message(message.from_user.id, 'Goodbye!')


def get_tasks(message: Message):
    if bot_bag['current_image']:
        rkb = types.ReplyKeyboardMarkup()
        buttons = [types.KeyboardButton(cat) for cat in categories]
        rkb.add(*buttons)
        n, e = os.path.splitext(bot_bag['current_image']['url'])
        filename = f'out{e}'
        with open(filename, 'wb') as f:
            f.write(urllib.request.urlopen(
                bot_bag['current_image']['url']).read())
            with open(filename, 'rb') as img:
                msg = bot.send_photo(message.from_user.id,
                                     img,  reply_markup=rkb)
                bot.register_next_step_handler(msg, match_image)


def match_image(message: Message):
    if bot_bag['current_image']:
        if message.text == bot_bag['current_image']['category']:
            try:
                bot_bag['current_image'] = get_current_image()
                get_tasks(message)
            except (sqlite3.ProgrammingError, StopIteration) as ex:
                print(ex)
                add_vote(message.from_user.id)
                bot.send_message(message.from_user.id, 'No vote available')
            except:
                print("error ")
        else:
            not_match_image(message)


def not_match_image(message: Message):
    msg = bot.send_message(message.from_user.id, 'Does not match')
    bot.register_next_step_handler(msg, match_image)


def get_user_answer(message: Message):
    if message.text == LOGIN:
        invite_login(message)
    elif message.text == REGISTER:
        register_user(message)
    elif message.text == LOGOUT:
        logout(message)
    elif message.text == MY_TASKS:
        get_tasks(message)


# bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()
bot.polling()
