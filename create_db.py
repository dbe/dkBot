from peewee import *
from models import ContestDownload

if __name__ == "__main__":
  print "Connecting to dkbot.db"
  db = SqliteDatabase('dkbot.db')

  print "Creating tables"
  db.create_tables([ContestDownload])

  print "Done"
