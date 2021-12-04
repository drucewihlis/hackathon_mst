#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
global bot, Blocks, commands
import psycopg2
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
class ButtonBlock:
    def __init__(self, listOfTopics, title, call):
        self.topicList = []
        for topic, callback in listOfTopics:
            self.topicList.append(Topic(topic, callback))
        self.title = title
        self.call = call

    def __eq__(self, other):
        return self.call==other.call
def CreateButtons(self, message):
    markup = telebot.types.InlineKeyboardMarkup()
    for topic in self.topicList:
        markup.add(telebot.types.InlineKeyboardButton(text=topic.text, callback_data=topic.callback))
    bot.send_message(message.chat.id, text="Choose module you want to learn", reply_markup=markup)
def GetButtonsByLevel(level):

def GetButtons(call_id):
    return True

class Topic:
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback
    def __eq__(self, other):
        return self.text==other

def SendStats(message):
    bot.send_message(message.chat.id,"you are better then 100%")
def SendAchievements(message):
    bot.send_message(message.chat.id, "You've got level 5")
def SendInfo(message):
    bot.send_message(message.chat.id, "This is a bot of dreamteam")
def changeData(msg):
    bot.send_message(msg.chat.id, "Changed to "+" "+ msg.text)
table = {
        'ch_mod_1':["Title 1", [['Topic EP 1', "ep_1"], ['Topic EP 2',"ep_1"], ['Topic EP 3',"ep_1"]]],
         'ch_mod_2':["Title 2",[['Topic PL 1', "pl_1"], ['Topic PL 2',"pl_1"], ['Topic PL 3',"pl_1"]]],
         "ch_mod_3":["Title 3",[['Topic web 1', "web_1"], ['Topic web 2',"web_1"], ['Topic web 3',"web_1"]]],
         "learn":["Chose module",[["Module 1", "ch_mod_1"], ["Module 2", "ch_mod_2"], ['Module 3', "ch_mod_3"]]]
         }
commands = ["info","change", "stats", "achiev"]
Blocks={}
for k in table.keys():
    Blocks[k] = ButtonBlock(table[k][1],table[k][0],k)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Learn', callback_data="learn"))
    markup.add(telebot.types.InlineKeyboardButton(text='Tests', callback_data="tests"))
    markup.add(telebot.types.InlineKeyboardButton(text='Achievements', callback_data="achievements"))
    markup.add(telebot.types.InlineKeyboardButton(text='Statistics', callback_data="statistics"))
    markup.add(telebot.types.InlineKeyboardButton(text='Info', callback_data="info"))
    markup.add(telebot.types.InlineKeyboardButton(text='Change personal data', callback_data="change"))
    bot.send_message(message.chat.id, text="Choose variant", reply_markup=markup)

@bot.message_handler(commands=['Statistics'])
def start_message(message):
    SendStats(message)


@bot.message_handler(commands=['Tests'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Module 1', callback_data="ch_mod_1"))
    markup.add(telebot.types.InlineKeyboardButton(text='Module 2', callback_data="ch_mod_2"))
    markup.add(telebot.types.InlineKeyboardButton(text='Module 3', callback_data="ch_mod_3"))
    bot.send_message(message.chat.id, text="Choose module you want to learn", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    #bot.answer_callback_query(callback_query_id=call.id, text='Выбор модуля')
    if call.data in table.keys():
        Blocks[call.data].CreateButtons(call.message)
    elif call.data == "change":
        msg = bot.send_message(call.message.chat.id,"Type your name")
        bot.register_next_step_handler(msg,changeData)
    elif call.data == "stats":
        SendStats(call.message)
    elif call.data == "achiev":
        SendAchievements(call.message)
    elif call.data == "info":
        SendInfo(call.message)
    else:
        bot.answer_callback_query(callback_query_id = call.id, text = "No information yet")
bot.polling()