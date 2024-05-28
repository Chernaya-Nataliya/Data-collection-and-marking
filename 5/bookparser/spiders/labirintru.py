# spiders/labirintru_spider.py
import scrapy
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = [
        "https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0"]

    def parse(self, response):
        next_page = response.xpath('//div[@class="pagination-next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            self.log('Следующих страниц больше нет')

        links = response.xpath("//a[@class='product-card__img']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response):
        item = BookparserItem()
        item['name'] = response.xpath("//h1/text()").get()  
        item['author'] = response.xpath("//a[@data-event-label='author']/text()").getall()
        item['translator'] = response.xpath("//a[@data-event-label='translator']/text()").getall()
        item['artist'] = response.xpath("//div[@class='authors']/a[not(@data-event-label='author') and "
                                        "not(@data-event-label='translator') and "
                                        "not(@data-event-label='editor')]/text()").getall()
        item['editor'] = response.xpath("//a[@data-event-label='editor']/text()").getall()
        item['publishing'] = response.xpath("//a[@data-event-label='publisher']/text()").getall()
        item['year'] = response.xpath("//div[@class='publisher']/text()").getall()
        item['series'] = response.xpath("//a[@data-event-label='series']/text()").getall()
        item['collection'] = response.xpath("//div[@class='collections']/a/text()").getall()
        item['genre'] = response.xpath("//a[@data-event-label='genre']/text()").getall()
        item['weight'] = response.xpath("//div[@class='weight']/text()").get()
        item['dimensions'] = response.xpath("//div[@class='dimensions']/text()").get()
        item['rating'] = response.xpath("//div[@id='rate']/text()").get()
        item['price'] = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        item['link'] = response.url
        
        yield item
