from peewee import *

import datetime

DATABASE = SqliteDatabase('deadringer.sqlite')

class Message(Model):
    #author = ForeignKeyField(User, backref='messages')
    body = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    trigger_time = DateTimeField()

    class Meta():
        database = DATABASE

def initialize():
    DATABASE.connect()
    print('Safely created database table "Messages"')
    DATABASE.create_tables([Message], safe=True)
    DATABASE.close()
