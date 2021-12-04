#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import gmail

global bot, Blocks, commands
from DataBase import DataBase

bot = telebot.TeleBot("5076051066:AAFNL2uekE97ukiQS4-QxIdeau1UeSD-V-Q")
userData = {}

def SendReg(message):
    email = message.text
    code = gmail.send_email(email)
    msg = bot.send_message(message.chat.id, "Введите код выслаланный на указанный Вами email")
    userData[message.chat.id] = code
    bot.register_next_step_handler(msg, CheckCode)

def CheckCode(message):
    if message.text == userData[message.chat.id]:
        bot.send_message(message.chat.id, 'Вы успешно авторизированы')
        buttons = database.GetButtonsByLevel(1)
        SendButtons(message, buttons)
    else:
        msg = bot.send_message(message.chat.id, 'Неверный код - попробуйте еще раз')
        bot.register_next_step_handler(msg, CheckCode)


def SendStats(message):
    bot.send_message(message.chat.id, "you are better then 100%")


def SendAchievements(message):
    print(message)
    bot.send_message(message.chat.id, "You've got level 5")


def SendInfo(message):
    bot.send_message(message.chat.id, "This is a bot of dreamteam")


def changeData(message):
    bot.send_message(message.chat.id, "Changed to " + " " + message.text)


def SendButtons(message, buttonsList):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in buttonsList:
        markup.add(telebot.types.InlineKeyboardButton(text=button.title, callback_data=button.callback))
    bot.send_message(message.chat.id, text="Выберете одну из опций", reply_markup=markup)


database = DataBase()
parents = database.GetButtonListWithChilds()
categories_ids = database.GetCategoriesIDs()


@bot.message_handler(commands=['start'])
def start_message(message):
    buttons = database.GetButtonsByLevel(0)
    SendButtons(message, buttons)

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
