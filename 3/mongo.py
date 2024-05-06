import json
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Создание базы данных и коллекции
db = client['books_buautiful_soup']  
collection = db['books_collection']  

# Чтение данных из JSON файла
with open('3/books_data3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Вставка данных в коллекцию
collection.insert_many(data)

print("Данные успешно загружены в MongoDB.")

# Эксперименты
# Книги, у которых цена меньше 50
cheap_books = collection.find({"Price": {"$lt": 50}})

# Нахождние книги по названию
book = collection.find_one({"Name": "A Light in the Attic"})

# Обновить цену книги с определенным названием
collection.update_one({"Name": "A Light in the Attic"}, {"$set": {"Price": 49.00}})

# Удалили книги с ценой больше 50
book_price100 = collection.delete_many({"Price": {"$gt": 50}})

# Подсчет книг с количеством меньше 10
count_books_10 = collection.count_documents({"Availability": {"$lt": 10}})
print("Количество книг с количеством меньше 10:", count_books_10)