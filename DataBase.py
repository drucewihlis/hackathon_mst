
import psycopg2


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
				print(select)
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

	def GetAllUser(self):
		return self.InquiryDataBase(select=self.Inquiry("*", "UserData"))

	def GetTopic(self):
		return self.InquiryDataBase(select=self.Inquiry("*", "Topic"))

	def GetAllButtonsCallback(self):
		return self.InquiryDataBase(select = self.Inquiry("callback", "buttons"))
	def GetButtonListWithChilds(self):
		return self.InquiryDataBase(select=self.Inquiry("callback", "buttons WHERE has_child = False"))
	def GetButtonsByLevel(self, level):
		table = self.InquiryDataBase(select=self.Inquiry("*", "buttons WHERE level ={} ORDER BY id".format(level)))
		result =[]
		for row in table:
			result.append(Button(row))
		return result
	def GetChildButtons(self, parent_callback):
		table = self.InquiryDataBase(select=self.Inquiry("*", "buttons WHERE parent_callback ='{}' ORDER BY id".format(parent_callback)))
		result = []
		for row in table:
			result.append(Button(row))
		return result
class Button:
	def __init__(self, row):
		self.id=row[0]
		self.title = row[1]
		self.callback = row[2]
		self.level = row[3]
		self.parCallbackId = row[4]
		self.parentCallback = row[5]

	def __str__(self):
		return self.title
# DataBase = DataBase()
# # print(DataBase.GreatUser('test', 'test'))
# #
# # print(DataBase.GetAllUser())
# # print(DataBase.GetAllButtonsCallback())
# for b in DataBase.GetButtonListWithChilds():
# 	print(b[0])
