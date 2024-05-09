import requests
from lxml import html
import csv
from pymongo import MongoClient

def save_to_mongodb(data):
    # Подключаемся к MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['news_database']
    collection = db['news_collection']
    # Вставляем данные в коллекцию
    collection.insert_many(data)

url = "https://news.mail.ru/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent}

# Отправляем GET-запрос на сайт
response = requests.get(url, headers=headers)

# Проверяем успешность запроса
if response.status_code == 200:
    # Получаем HTML-контент страницы
    html_content = response.content
    # Создаем объект для парсинга HTML
    tree = html.fromstring(html_content)
    
    # Извлекаем данные из блока "daynews__MainTopNews"
    articles = []
    main_news = tree.xpath("//div[@data-logger='news__MainTopNews']")[0]
    for item in main_news.xpath(".//div[contains(@class, 'daynews__item')]"):
        title = item.xpath(".//span[contains(@class, 'photo__title')]/text()")
        link = item.xpath(".//a[contains(@class, 'photo__inner')]/@href")
        if title and link:
            articles.append({'title': title[0].strip(), 'link': link[0]})

    # Извлекаем данные из блока "block"
    block = tree.xpath('//div[@class="block"]')[0]
    articles_block = block.xpath('.//li[contains(@class, "list__item")]') 
    for article in articles_block:
        title = article.xpath('.//a[@class="list__text"]/text()')[0]
        link = article.xpath('.//a[@class="list__text"]/@href')[0]
        articles.append({'title': title.strip(), 'link': link})

    # Убираем повторяющиеся заголовки и ссылки
    articles = list({(article['title'], article['link']) for article in articles})

    # Сохраняем данные в CSV-файл
    with open('articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Заголовок', 'Ссылка'])
        writer.writerows(articles)
        
    # Сохраняем данные в MongoDB
    save_to_mongodb([{'title': article[0], 'link': article[1]} for article in articles])
        
    print("Данные успешно сохранены в файл 'articles.csv' и в MongoDB")
else:
    print("Ошибка при выполнении запроса:", response.status_code)
