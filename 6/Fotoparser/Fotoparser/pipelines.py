# Для скачивания картинок устанавливаем модуль pillow
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from pymongo import MongoClient
import os
from Fotoparser.settings import IMAGES_STORE, BOT_NAME
import csv
from Fotoparser.items import FotoparserItem
from scrapy.exceptions import DropItem

class FotoparserPipeline:
    def __init__(self):
        # Настраиваем клиент MongoDB (IP, порт)
        client = MongoClient('localhost', 27017)
        # Задаём название базы данных ('books')
        self.mongo_base = client.images

    def process_item(self, item, spider):
        """
        Функция записывает данные в БД MongoDB

        :param item: данные пришедшие из парсера
        :param spider:
        :return: запись в БД
        """

        # Создаём коллекцию в БД (имя нашего паука)
        collection = self.mongo_base[spider.name]
        if item.get('path'):
            # Добавляем запись в базу данных
            collection.insert_one(item)

        return item


class PhotosPipeline(ImagesPipeline):
    count_img = 0

    def get_media_requests(self, item, info):
        try:
            # Выводим информацию о состоянии процесса
            self.count_img += 1
            print(f'Обработано {self.count_img} ссылок')
            yield scrapy.Request(item['url'])
        except Exception as e:
            print(f"Ошибка обработки изображения {item['url']}: {e}")

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        file_name = f"{item['name']}-{image_guid}.jpg"
        basedir = str(os.path.abspath(os.path.dirname(__file__))).replace(BOT_NAME, '')
        file_path = os.path.join(basedir + IMAGES_STORE, file_name)
        item['path'] = f'{file_path}'
        item['_id'] = f'{image_guid}'
        return file_name

    def item_completed(self, results, item, info):
        for success, file_info in results:
            if success:
                image_path = file_info['path']
                item['path'] = image_path
                return item
        raise DropItem(f"Элемент {item['url']} не удалось загрузить")

class CsvPipeline:
    def __init__(self):
        self.csv_file = open('images_info.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['URL', 'Path', 'Name', 'Category'])

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter.get('url')
        path = adapter.get('path')
        name = adapter.get('name')
        category = adapter.get('category')

        if not url or not path:
            raise DropItem("Отсутствует URL путь в %s" % item)

        self.csv_writer.writerow([url, path, name, category])

        return item

    def close_spider(self, spider):
        self.csv_file.close()