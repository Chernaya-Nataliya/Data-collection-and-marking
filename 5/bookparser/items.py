# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookparserItem(scrapy.Item):
    name = scrapy.Field()        # название
    author = scrapy.Field()      # автор
    translator = scrapy.Field()  # переводчик
    artist = scrapy.Field()      # художник
    editor = scrapy.Field()      # редактор
    publishing = scrapy.Field()  # издательство
    year = scrapy.Field()        # год
    series = scrapy.Field()      # серия
    collection = scrapy.Field()  # коллекция
    genre = scrapy.Field()       # жанр
    weight = scrapy.Field()      # масса
    dimensions = scrapy.Field()  # размеры
    rating = scrapy.Field()      # рейтинг
    price = scrapy.Field()       # цена
    link = scrapy.Field()        # url
    _id = scrapy.Field()         # id в базе mongodb