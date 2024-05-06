from clickhouse_driver import Client
import json

# Подключение к ClickHouse
client = Client(host='localhost', port=9000)

# Создание таблицы для хранения книг
client.execute('''
    CREATE TABLE IF NOT EXISTS books (
        Name String,
        Price Float64,
        Availability UInt32,
        Description String
    ) ENGINE = MergeTree()
    ORDER BY Name
''')

# Чтение данных из JSON файла
with open('3/books_data3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Вставка данных в таблицу ClickHouse
client.execute('INSERT INTO books VALUES', data)

print("Данные успешно загружены в ClickHouse.")
