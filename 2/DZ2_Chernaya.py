# Скрейпинг одной страницы
'''import requests
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

'''
# ## Скрейпинг нескольких страниц
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

# Функция для извлечения данных о книгах с одной страницы
def scrape_books_from_page(url):
    # Пустые списки для хранения данных о книгах на странице
    names = []
    prices = []
    availability = []
    descriptions = []

    # Запрос к странице
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все ссылки на книги
    book_links = soup.find_all('h3')

    # Цикл по каждой книге на странице
    for link in book_links:
        book_url = link.find('a')['href']
        book_response = requests.get(url.rsplit('/', 1)[0] + '/' + book_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')

        # Извлекаем данные о книге
        name = book_soup.find('h1').text
        # Извлекаем цену с учетом возможного отсутствия элемента с классом 'price_color'
        price_element = book_soup.find('p', class_='price_color')
        price = float(price_element.text.split('£')[1]) if price_element else None
        stock = int(re.search(r'\d+', book_soup.find('p', class_='instock availability').text).group())
        description = book_soup.find('meta', attrs={'name': 'description'})['content']

        # Добавляем данные в соответствующие списки
        names.append(name)
        prices.append(price)
        availability.append(stock)
        descriptions.append(description)

    return names, prices, availability, descriptions

# Функция для извлечения данных о книгах со всех страниц
def scrape_all_books():
    # Ссылка на главную страницу книжного магазина для скрапинга
    base_url = 'http://books.toscrape.com/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Находим количество страниц
    page_count = int(soup.find('li', class_='current').text.strip().split()[-1])

    # Пустые списки для хранения данных о книгах
    all_names = []
    all_prices = []
    all_availability = []
    all_descriptions = []

    # Цикл по всем страницам книжного магазина
    for page in range(1, page_count + 1):
        page_url = base_url + f'catalogue/page-{page}.html'
        names, prices, availability, descriptions = scrape_books_from_page(page_url)
        all_names.extend(names)
        all_prices.extend(prices)
        all_availability.extend(availability)
        all_descriptions.extend(descriptions)

    return all_names, all_prices, all_availability, all_descriptions

# Извлекаем данные
names, prices, availability, descriptions = scrape_all_books()

# Создаем DataFrame
df = pd.DataFrame({
    'Name': names,
    'Price': prices,
    'Availability': availability,
    'Description': descriptions
})

# Фильтруем книги, у которых в наличии только 19 штук
filtered_books = df[df['Availability'] == 19]

# Сохраняем DataFrame в JSON файл
filtered_books.to_json('books_data1.json', orient='records')

print("Данные сохранены в JSON файл 'books_data1.json'")
