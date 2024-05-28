# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# pipelines.py
# pipelines.py
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books
        self.count_page = 0

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        # id
        try:
            *_, id, _ = item['link'].split('/')
            item['_id'] = id
        except ValueError:
            item['_id'] = None

        # Обработка названия книги
        try:
            _, name = item.get('name').split(':')
            item['name'] = name.strip()
        except ValueError:
            item['name'] = item.get('name', '').strip()

        # Обработка авторов книги
        item['author'] = ', '.join(item['author'])

        # Обработка переводчиков книги
        item['translator'] = ', '.join(item['translator'])

        # Обработка художников книги
        item['artist'] = ', '.join(item['artist'])

        # Обработка рецензентов
        item['editor'] = ', '.join(item['editor'])

        # Обработка издательств
        item['publishing'] = ', '.join(item['publishing'])

        # Обработка года издания книги
        try:
            *_, year, _ = item['year'][1].split(' ')
            item['year'] = int(year)
        except (ValueError, IndexError):
            item['year'] = None

        # Обработка серии
        item['series'] = ', '.join(item['series'])

        # Обработка коллекции
        item['collection'] = ', '.join(item['collection'])

        # Обработка жанра книги
        item['genre'] = ', '.join(item['genre'])

        # Обработка массы книги
        try:
            *_, weight, _ = item['weight'].split(' ')
            item['weight'] = int(weight)
        except (ValueError, IndexError):
            item['weight'] = None

        # Обработка размеров книги
        try:
            *_, dimensions, _ = item['dimensions'].split(' ')
            length, width, height = dimensions.split('x')
            item['dimensions'] = {'length': int(length), 'width': int(width), 'height': int(height)}
        except (ValueError, IndexError):
            item['dimensions'] = {'length': None, 'width': None, 'height': None}

        # Обработка рейтинга книги
        try:
            item['rating'] = float(item['rating'])
        except ValueError:
            item['rating'] = None

        # Обработка цены книги
        try:
            item['price'] = float(item['price'])
        except ValueError:
            item['price'] = None

        try:
            # Добавляем или обновляем запись в базе данных
            collection.update_one({'_id': item['_id']}, {'$set': item}, upsert=True)
        except Exception as e:
            print(f'Ошибка добавления или обновления документа: {e}')

        # Выводим информацию о состоянии процесса
        self.count_page += 1
        print(f'Обработано {self.count_page} книг')

        return item
