from peewee import *

db = SqliteDatabase('dkbot.db')

class BaseModel(Model):

  class Meta:
    database = db

class ContestDownload(BaseModel):
  contest_id = IntegerField(null=False)
  downloaded = DateTimeField(null=False)
