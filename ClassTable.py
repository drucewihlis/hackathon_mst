class Button:
    def __init__(self, row):
        self.id = row[0]
        self.title = row[1]
        self.callback = row[2]
        self.level = row[3]
        self.parCallbackId = row[4]
        self.parentCallback = row[5]


class Card:
    def __init__(self, row):
        self.id = row[0]
        self.category_id = row[1]
        self.name_card = row[2]
        self.info = row[3]


class Category:
    def __init__(self, row):
        self.id = row[0]
        self.title = row[1]
        self.topic_id = row[2]
        self.description = row[3]


class Topic:
    def __init__(self, row):
        self.id = row[0]
        self.name_topic = row[1]
        self.info = row[2]


class User:
    def __init__(self, row):
        self.id = row[0]
        self.user_id = row[1]
        self.username = row[2]


class Option:
    def __init__(self, row):
        self.id = row[0]
        self.question_id = row[1]
        self.name_option = row[2]
        self.info = row[3]


class Question:
    def __init__(self, row):
        self.id = row[0]
        self.card_id = row[1]
        self.name_question = row[2]
        self.info = row[3]


class Achievments:
    def __init__(self, row):
        self.id = row[0]
        self.title = row[1]
        self.img = row[2]
        self.info = row[3]


class UserAchievments:
    def __init__(self, row):
        self.id = row[0]
        self.achievment_id = row[1]
        self.user_id = row[2]


class Domen:
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
