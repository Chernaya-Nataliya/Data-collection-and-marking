import scrapy
from scrapy.loader import ItemLoader
from Fotoparser.items import FotoparserItem


class UnsplashcomSpider(scrapy.Spider):
    """
    Класс UnsplashcomSpider, парсит категории рисунков, название и ссылки на рисунки

     Атрибуты:
    - name: название паука,
    - allowed_domains: разрешенные домены,
    - start_urls: стартовая страница.

     Методы:
    - parse(self, response): Функция парсит категории рисунков,
    - img_parse(self, response): Функция парсит рисунки в категории.
    """

    name = "unsplashcom"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        # С помощью Xpath выражения загружаем ссылки на категорию изображений
        categories = response.xpath("(//ul)[last()]//a[not(text()='Unsplash+') and not(text()='Editorial')]/@href")

        for category in categories:
            # Посылаем запросы на страницу категории
            yield response.follow(url=category, callback=self.foto_parse)

    def foto_parse(self, response):
        # Вычисляем обЩее количество картинок в категории
        list_url = response.xpath("//img[@data-test]")
        for item in list_url:
            # Создаем элемент loader
            loader = ItemLoader(item=FotoparserItem(), response=response)
            # Записываем в loader имя категории
            loader.add_xpath('category', '//h1/text()')
            # Записываем в переменные название и ссылку на картинку
            url = item.xpath('./@src').get()
            name = item.xpath('./@alt').get()
            # Записываем в loader ссылку на картинку и название
            loader.add_value('url', url)
            loader.add_value('name', name)
            # Посылаем loader в Pipeline
            yield loader.load_item()