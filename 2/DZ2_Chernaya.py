import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

# Ссылка на главную страницу книжного магазина для скрапинга
url = 'http://books.toscrape.com/'

# Функция для извлечения данных о книгах
def scrape_books(url):
    # Пустые списки для хранения данных о книгах
    names = []
    prices = []
    availability = []
    descriptions = []

    # Запрос к странице
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все ссылки на книги
    book_links = soup.find_all('h3')

    # Цикл по каждой книге
    for link in book_links:
        book_url = link.find('a')['href']
        book_response = requests.get(url + book_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')

        # Извлекаем данные о книге
        name = book_soup.find('h1').text
        price = float(book_soup.find('p', class_='price_color').text.split('£')[1])
        stock = int(re.search(r'\d+', book_soup.find('p', class_='instock availability').text).group())
        description = book_soup.find('meta', attrs={'name': 'description'})['content']

        # Добавляем данные в соответствующие списки
        names.append(name)
        prices.append(price)
        availability.append(stock)
        descriptions.append(description)

    return names, prices, availability, descriptions

# Извлекаем данные
names, prices, availability, descriptions = scrape_books(url)

# Создаем DataFrame
df = pd.DataFrame({
    'Name': names,
    'Price': prices,
    'Availability': availability,
    'Description': descriptions
})

# Сохраняем DataFrame в JSON файл
df.to_json('books_data.json', orient='records')

print("Данные сохранены в JSON файл 'books_data.json'")