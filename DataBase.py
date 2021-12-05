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
                # print(select)
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

    def CreateUser(self, user_id, user_name):
        return self.InquiryDataBase(
            insert="""INSERT INTO UserData  (user_id, username)  VALUES  ('{}', '{}')""".format(str(user_id),
                                                                                                str(user_name)))

    def GetUser(self, user_id):
        table = self.InquiryDataBase(select=self.Inquiry("*", "userdata WHERE user_id = '{}'").format(str(user_id)))
        try:

            result = User(table[0])
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

    def GetQuestionByCardId(self, card_id):
        card_list = str(card_id.pop(0).id)
        for u in card_id:
            card_list = card_list + ", " + str(u.id)

        table = self.InquiryDataBase(select=self.Inquiry("*", "Question WHERE card_id in ({})".format(str(card_list))))
        result = []
        try:
            for row in table:
                result.append(Question(row))
        except:
            return 0
        return result

    def GetOptionsByQuestionId(self, question_id):
        # print(question_id)
        table = self.InquiryDataBase(select=self.Inquiry("*", "option WHERE question_id = {}".format(str(question_id))))
        # print(table)
        result = []
        try:
            for row in table:
                # print(row)
                result.append(Option(row))
        except:
            return 0
        return result

    def GetQuestionsByCategory(self, card_id):
        table = self.InquiryDataBase(select=self.Inquiry("*", "Question WHERE card_id = {}".format(str(card_id))))
        result = []
        try:
            for row in table:
                result.append(Question(row))
        except:
            return 0
        return result

    def GetCardsByCallback(self, category_callback):
        table = self.InquiryDataBase(
            select=self.Inquiry("*", "Card WHERE category_callback = '{}'".format(str(category_callback))))
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

        table = self.InquiryDataBase(
            select=self.Inquiry("*", "user_achievments WHERE user_id in [{}]".format(str(user_id))))
        result = []
        try:
            for row in table:
                result.append(UserAchievments(row))
        except:
            return 0
        return result

    def GetAchievmentsByUserId(self, user_id):
        table = self.InquiryDataBase(select=self.Inquiry("a.id, a.title, a.img, a.info", "user_achievments as "
                                                                                         "u RIGHT JOIN achievments AS a  "
                                                                                         "ON  u.user_id = {}  "
                                                                                         "AND a.id = u.achievment_id".format(
            str(user_id))))
        result = []
        try:
            for row in table:
                result.append(Achievments(row))
        except:
            return 0
        return result

    def GetButtonsByLevel(self, level):

        table = self.InquiryDataBase(select=self.Inquiry("*", "buttons WHERE level ={} ORDER by id".format(str(level))))
        result = []
        try:
            for row in table:
                result.append(Button(row))
        except:
            return 0
        return result

    def GetDomenByName(self, name):
        table = self.InquiryDataBase(select=self.Inquiry("*", "domens WHERE name = '{}'".format(str(name))))
        result = []

        try:
            for row in table:
                result.append(Domen(row))
        except:
            return 0
        return result

    def GetAllButtonsCallback(self):
        return self.InquiryDataBase(select=self.Inquiry("callback", "buttons"))

    def GetButtonListWithChilds(self):
        return self.InquiryDataBase(select=self.Inquiry("callback", "buttons WHERE has_child = False"))

    def GetCategoriesIDs(self):
        categories = []
        result = self.InquiryDataBase(select=self.Inquiry("DISTINCT category_callback", "category"))
        for r in result:
            categories.append(r[0])
        return categories

    def GetChildButtons(self, parent_callback):
        table = self.InquiryDataBase(
            select=self.Inquiry("*", "buttons WHERE parent_callback ='{}' ORDER BY id".format(parent_callback)))
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
