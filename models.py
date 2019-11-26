from peewee import *
from flask_login import UserMixin
import datetime

#DATABASE = SqliteDatabase('deadringer.sqlite')
DATABASE = PostgresqlDatabase(
    'deadringer'
)

class User(Model, UserMixin):
    #username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE
        table_name = 'account'

class Message(Model):
    author = ForeignKeyField(User, backref='messages')
    body = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    trigger_time = DateTimeField()
    class Meta:
        database = DATABASE

class Receipt(Model):
    message = ForeignKeyField(Message, backref='recipients', on_delete='CASCADE')
    to_user = ForeignKeyField(User, backref='received_messages', on_delete='CASCADE')
    is_read = BooleanField(default=False)
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Message, User, Receipt], safe=True)
    print('Safely created database models')
    DATABASE.close()
