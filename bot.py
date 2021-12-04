#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
global bot, Blocks, commands
import psycopg2
from DataBase import DataBase

bot = telebot.TeleBot("5076051066:AAFNL2uekE97ukiQS4-QxIdeau1UeSD-V-Q")
user_data={}
def SendStats(message):
    bot.send_message(message.chat.id,"you are better then 100%")
def SendAchievements(message):
    bot.send_message(message.chat.id, "You've got level 5")
def SendInfo(message):
    bot.send_message(message.chat.id, "This is a bot of dreamteam")
def changeData(message):
    bot.send_message(message[0].chat.id, "Changed to "+" "+ message[0].text)
def SendButtons(message, buttonsList):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in buttonsList:
        markup.add(telebot.types.InlineKeyboardButton(text=button.title, callback_data=button.callback))
    bot.send_message(message.chat.id, text="Выбери вариант", reply_markup=markup)
def SendCard(message, card):

    bot.send_message(message.chat.id, card.info)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Далее'))
    msg = bot.send_message(message.chat.id, 'Следующая карточка?',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, nextcard)

def nextcard(msg):
    if len(user_data[str(msg.chat.id)])>0:
        if msg.text == "Далее":
            SendCard(msg, user_data[str(msg.chat.id)].pop(0))
    else:
        bot.send_message(msg.chat.id,"Все карточки пройдены!")




database = DataBase()
parents = database.GetButtonListWithChilds()
categories_ids = database.GetCategoriesIDs()

@bot.message_handler(commands=['start'])
def start_message(message):
    buttons = database.GetButtonsByLevel(1)
    SendButtons(message, buttons)

#
# @bot.message_handler(commands=['Tests'])
# def start_message(message):
#     buttons = database.GetButtonsByLevel(1);
#     SendButtons(message, buttons)
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    #bot.answer_callback_query(callback_query_id=call.id, text='Выбор модуля')
    callback = (call.data,)
    if callback not in parents:
        if callback[0]=="edit_profile":
            msg = bot.send_message(call.message.chat.id,"Type your name")
            bot.register_next_step_handler(msg,changeData)
        elif callback[0]=="statistics":
            SendStats(call.message)
        elif callback[0]=="achievements":
            SendAchievements(call.message)
        elif callback[0] == "info":
            SendInfo(call.message)
        elif callback[0] in categories_ids:

            cards = database.GetCards(callback[0])
            user_data[str(call.message.chat.id)] = cards
            if len(user_data[str(call.message.chat.id)])>0:
                SendCard(call.message, user_data[str(call.message.chat.id)].pop(0))
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="No information yet")
    elif callback in parents:
        buttons = database.GetChildButtons(callback[0])
        SendButtons(call.message, buttons)
    else:
        bot.answer_callback_query(callback_query_id = call.id, text = "No information yet")
bot.polling()