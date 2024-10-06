# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import Column,Integer,String,Float,PickleType
from sqlalchemy.ext.declarative import declarative_base

db_url = 'mysql+pymysql://root:mm546896@localhost:3306/douban'
db = declarative_base()

class DBItem(db):
    __tablename__ = 'top250'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(55),unique=True)
    rating = Column(Float)
    poster = Column(String(255))
    director = Column(String(55))
    writer = Column(PickleType)
    actor = Column(PickleType)
    types = Column(PickleType)
    release = Column(PickleType)
    duration = Column(Integer)
    intro = Column(String(1000))


class Top250Item(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    poster = scrapy.Field()
    intro = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    actor = scrapy.Field()
    types = scrapy.Field()
    release = scrapy.Field()
    duration = scrapy.Field()

 