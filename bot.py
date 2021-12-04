#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
global bot, Blocks, commands
import psycopg2
from DataBase import DataBase

bot = telebot.TeleBot("5076051066:AAFNL2uekE97ukiQS4-QxIdeau1UeSD-V-Q")
conn = psycopg2.connect("""
    host=rc1c-sz7li2hysj2rl3ak.mdb.yandexcloud.net
    port=6432
    dbname=dream_team
    user=dream
    password=611621team
    target_session_attrs=read-write
    sslmode=verify-full
""")

def SendStats(message):
    bot.send_message(message.chat.id,"you are better then 100%")
def SendAchievements(message):
    bot.send_message(message.chat.id, "You've got level 5")
def SendInfo(message):
    bot.send_message(message.chat.id, "This is a bot of dreamteam")
def changeData(message):
    bot.send_message(message.chat.id, "Changed to "+" "+ message.text)
def SendButtons(message, buttonsList, ):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in buttonsList:
        markup.add(telebot.types.InlineKeyboardButton(text=button.title, callback_data=button.callback))
    bot.send_message(message.chat.id, text="Выбери вариант", reply_markup=markup)
database = DataBase()
parents = database.GetButtonListWithChilds()
@bot.message_handler(commands=['start'])
def start_message(message):
    buttons = database.GetButtonsByLevel(1);
    SendButtons(message, buttons)


@bot.message_handler(commands=['Statistics'])
def start_message(message):
    SendStats(message)

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
    elif callback in parents:
        buttons = database.GetChildButtons(callback[0])
        SendButtons(call.message, buttons)
    else:
        bot.answer_callback_query(callback_query_id = call.id, text = "No information yet")
bot.polling()