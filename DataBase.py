
import psycopg2
from ClassTable import *


class DataBase():
	def __init__(self):
		pass
	def Connect(self):
		connect = psycopg2.connect(dbname='dream_team', user='dream',
		                        password='611621team', host='rc1c-sz7li2hysj2rl3ak.mdb.yandexcloud.net', port=6432)
		return connect.cursor(), connect

	def Inquiry(self, column, database):
		return """SELECT {} FROM {}""".format(column, database)

	def InquiryDataBase(self, select=None, insert=None):
		connection = None
		cursor = None
		DataOut = 1
		try:
			cursor, connection = self.Connect()
			if (select != None):
				cursor.execute(select)
				DataOut = cursor.fetchall()
			else:
				cursor.execute(insert)
				connection.commit()
		except:
			return 0
		finally:
			if connection:
				cursor.close()
				connection.close()
		return DataOut

	def GreatUser(self, user_id, user_name):
		return self.InquiryDataBase(insert = """INSERT INTO UserData  (user_id, username)  VALUES  ('{}', '{}')""".format(str(user_id), str(user_name)))

	def GetUser(self):
		table = self.InquiryDataBase(select=self.Inquiry("*", "UserData"))
		result = []
		try:
			for row in table:
				result.append(User(row))
		except:
			return 0
		return result


	def GetTopic(self):
		table = self.InquiryDataBase(select=self.Inquiry("*", "Topic"))
		result = []
		try:
			for row in table:
				result.append(Topic(row))
		except:
			return 0
		return result

	def GetOption(self, question_id):
		table = self.InquiryDataBase(select=self.Inquiry("*", "Option WHERE question_id = {}".format(str(question_id))))
		result = []
		try:
			for row in table:
				result.append(Option(row))
		except:
			return 0
		return result

	def GetQuestion(self, card_id):
		table = self.InquiryDataBase(select=self.Inquiry("*", "Question WHERE card_id = {}".format(str(card_id))))
		result = []
		try:
			for row in table:
				result.append(Question(row))
		except:
			return 0
		return result

	def GetCards(self, category_callback):
		print(category_callback)
		table = self.InquiryDataBase(select=self.Inquiry("*", "Card WHERE category_callback = '{}'".format(str(category_callback))))
		result = []
		try:
			for row in table:
				result.append(Card(row))
		except:
			return 0
		return result

	def GetCategory(self, topic_id):

		table = self.InquiryDataBase(select=self.Inquiry("*", "Category WHERE topic_id = {}".format(str(topic_id))))
		result = []
		try:
			for row in table:
				result.append(Category(row))
		except:
			return 0
		return result

	def GetAchievments(self):
		table = self.InquiryDataBase(select=self.Inquiry("*", "Achievments"))
		result = []
		try:
			for row in table:
				result.append(Achievments(row))
		except:
			return 0
		return result


	def GetUserAchievments(self, user_id):
		table = self.InquiryDataBase(select=self.Inquiry("*", "user_achievments WHERE user_id = '{}'".format(str(user_id))))
		result = []
		try:
			for row in table:
				result.append(UserAchievments(row))
		except:
			return 0
		return result

	def GetButtonsByLevel(self, level):

		table = self.InquiryDataBase(select=self.Inquiry("*", "buttons WHERE level ={} ORDER by id".format(str(level))))
		result =[]
		try:
			for row in table:
				result.append(Button(row))
		except:
			return 0
		return result

	def GetAllButtonsCallback(self):
		return self.InquiryDataBase(select = self.Inquiry("callback", "buttons"))
	def GetButtonListWithChilds(self):
		return self.InquiryDataBase(select=self.Inquiry("callback", "buttons WHERE has_child = False"))
	def GetCategoriesIDs(self):
		categories =[]
		result = self.InquiryDataBase(select=self.Inquiry("DISTINCT category_callback", "category"))
		for r in result:
			categories.append(r[0])
		return categories
	def GetChildButtons(self, parent_callback):
		table = self.InquiryDataBase(select=self.Inquiry("*", "buttons WHERE parent_callback ='{}' ORDER BY id".format(parent_callback)))
		result = []
		try:
			for row in table:
				result.append(Button(row))
		except:
			return 0
		return result

	def __str__(self):
		return self.title
# DataBase = DataBase()
# # print(DataBase.GreatUser('test', 'test'))
# #
# # print(DataBase.GetAllUser())
# # print(DataBase.GetAllButtonsCallback())
# for b in DataBase.GetButtonListWithChilds():
# 	print(b[0])
