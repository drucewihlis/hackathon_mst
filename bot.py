#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import gmail

global bot, Blocks, commands
from DataBase import DataBase

bot = telebot.TeleBot("5076051066:AAFNL2uekE97ukiQS4-QxIdeau1UeSD-V-Q")
user_data = {}
achiv_img_path = 'img/achievments/'


def SendReg(message):
    email = message.text
    domenName = message.text.split('@')[-1]
    if not bool(database.GetDomenByName(domenName)):
        msg = bot.send_message(message.chat.id, "Данный email не имеет доступа к боту, введите Вашу корпоративную почту")
        bot.register_next_step_handler(msg, SendReg)
    else:
        code = gmail.send_email(email)
        msg = bot.send_message(message.chat.id, "Введите код выслаланный на указанный Вами email")
        user_data[message.chat.id] = code
        bot.register_next_step_handler(msg, CheckCode)


def CheckCode(message):
    if message.text == user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Вы успешно авторизированы')
        database.CreateUser(message.chat.id, str(message.from_user.first_name)+" "+str(message.from_user.last_name))
        buttons = database.GetButtonsByLevel(1)
        SendButtons(message, buttons)
    else:
        msg = bot.send_message(message.chat.id, 'Неверный код - попробуйте еще раз')
        bot.register_next_step_handler(msg, CheckCode)


def SendStats(message):
    bot.send_message(message.chat.id, "Вы готовы к атакам киберпреступников лучше чем 100% пользователей")


def SendAchievements(message):
    achievments = database.GetAchievmentsByUserId(message.chat.id)
    for achiv in achievments:
        sti = open(achiv_img_path + achiv.img, 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, achiv.title + ' - ' + achiv.info)


def SendInfo(message):
    bot.send_message(message.chat.id, "Чат-бот команды dreamteam")


def changeData(message):
    bot.send_message(message.chat.id, "Changed to " + " " + message.text)


def SendButtons(message, buttonsList):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in buttonsList:
        markup.add(telebot.types.InlineKeyboardButton(text=button.title, callback_data=button.callback))

    bot.send_message(message.chat.id, text="Выбери вариант", reply_markup=markup)


def SendCard(message, card):
    bot.send_message(message.chat.id, card.info)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Да'))
    markup.add(telebot.types.KeyboardButton('Нет'))
    msg = bot.send_message(message.chat.id, 'Следующая карточка?',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, nextcard)


def nextcard(msg):
    if len(user_data[str(msg.chat.id)]) > 0:
        if msg.text == "Да":
            SendCard(msg, user_data[str(msg.chat.id)].pop(0))
    else:

        bot.send_message(msg.chat.id, "Все карточки пройдены!",reply_markup = telebot.types.ReplyKeyboardRemove())
        buttons = database.GetButtonsByLevel(1)
        SendButtons(msg, buttons)


database = DataBase()
parents = database.GetButtonListWithChilds()
categories_ids = database.GetCategoriesIDs()


@bot.message_handler(commands=['start'])
def start_message(message):
    if database.GetUser(message.chat.id):
        buttons = database.GetButtonsByLevel(1)
        SendButtons(message, buttons)
    else:
        buttons = database.GetButtonsByLevel(0)
        SendButtons(message, buttons)
@bot.message_handler(commands=['menu'])
def menu_message(message):
    buttons = database.GetButtonsByLevel(1)
    SendButtons(message, buttons)
@bot.message_handler(commands=['info'])
def info_message(message):
    SendInfo(message)
@bot.message_handler(commands=['achievements'])
def Achievment_message(message):
    SendAchievements(message)
@bot.message_handler(commands=['statistics'])
def Achievment_message(message):
    SendStats(message)

#
# @bot.message_handler(commands=['Tests'])
# def start_message(message):
#     buttons = database.GetButtonsByLevel(1);
#     SendButtons(message, buttons)
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # bot.answer_callback_query(callback_query_id=call.id, text='Выбор модуля')
    callback = (call.data,)
    if callback not in parents:
        if callback[0] == "edit_profile":
            msg = bot.send_message(call.message.chat.id, "Type your name")
            bot.register_next_step_handler(msg, changeData)
        elif callback[0] == "statistics":
            SendStats(call.message)
        elif callback[0] == "achievements":
            SendAchievements(call.message)
        elif callback[0] == "info":
            SendInfo(call.message)

        elif callback[0] in categories_ids:

            cards = database.GetCards(callback[0])
            user_data[str(call.message.chat.id)] = cards
            if len(user_data[str(call.message.chat.id)]) > 0:
                SendCard(call.message, user_data[str(call.message.chat.id)].pop(0))

        elif callback[0] == "reg":
            msg = bot.send_message(call.message.chat.id, "Введите Вашу почту")
            bot.register_next_step_handler(msg, SendReg)
        # elif callback[0] in categories_ids:

        else:
            bot.answer_callback_query(callback_query_id=call.id, text="No information yet")
    elif callback in parents:
        buttons = database.GetChildButtons(callback[0])
        SendButtons(call.message, buttons)
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="No information yet")


bot.polling()
