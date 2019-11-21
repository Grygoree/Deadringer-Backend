from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('deadringer.sqlite')

class User(Model, UserMixin):
    #username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE

class Message(Model):
    author = ForeignKeyField(User, backref='messages')
    body = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    trigger_time = DateTimeField()
    class Meta:
        database = DATABASE

class Receipt(Model):
    message = ForeignKeyField(Message, backref='recipients')
    to_user = ForeignKeyField(User, backref='received_messages')
    #status = enum/bool? unread, read, archived
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Message, User, Receipt], safe=True)
    print('Safely created database models "Message", "User", and "Receipt"')
    DATABASE.close()
