import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lab3.model import WebServer, DatabaseServer
from src.lab3.base import Server
from src.lab2.collection import ServerCollection

print("ЛР-3: НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ")

# СОЗДАНИЕ ОБЪЕКТОВ
web = WebServer("WebServer", "10.0.0.1", 8, 32, "example.com")
db = DatabaseServer("DatabaseServer", "10.0.0.2", 16, 64, "PostgreSQL")

web.start()
db.start()
web.add_site()
web.add_site()
db.create_db()

col = ServerCollection()
col.add(web)
col.add(db)

print("\n" + "=" * 60)
print("СЦЕНАРИЙ 1: РАЗНЫЕ ТИПЫ В ОДНОЙ КОЛЛЕКЦИИ")
print("=" * 60)

print("1. Созданы объекты разных типов:")
print(f"   {web}")
print(f"   {db}")

print("\n2. Проверка типов через isinstance():")
print(f"   web - WebServer: {isinstance(web, WebServer)}")
print(f"   web - Server: {isinstance(web, Server)}")
print(f"   db - DatabaseServer: {isinstance(db, DatabaseServer)}")
print(f"   db - Server: {isinstance(db, Server)}")

print("\n3. Все объекты добавлены в одну коллекцию:")
for server in col:
    print(f"   {server}")

print(f"\n4. Всего серверов в коллекции: {len(col)}")

print("\n" + "=" * 60)
print("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ - ОДИН МЕТОД, РАЗНОЕ ПОВЕДЕНИЕ")
print("=" * 60)

print("1. Базовый метод get_score() из класса Server:")
for server in col:
    base_score = server._cpu * server._ram
    print(f"   {server.name}: {server._cpu} * {server._ram} = {base_score}")

print("\n2. Переопределенный метод get_score() в дочерних классах:")
for server in col:
    print(f"   {server.name}: {server.get_score()}")

print("\n3. Разница между базовым и переопределенным методом:")
for server in col:
    diff = server.get_score() - (server._cpu * server._ram)
    print(f"   {server.name}: +{diff} (доп. бонус от дочернего класса)")

print("\n" + "=" * 60)
print("СЦЕНАРИЙ 3: ФИЛЬТРАЦИЯ И УПРАВЛЕНИЕ")
print("=" * 60)

print("1. Фильтрация по типу (только веб-серверы):")
webs = [s for s in col.get_all() if isinstance(s, WebServer)]
for s in webs:
    print(f"   {s.name} - домен: {s._domain}, сайтов: {s._sites}")

print("\n2. Фильтрация по типу (только БД-серверы):")
dbs = [s for s in col.get_all() if isinstance(s, DatabaseServer)]
for s in dbs:
    print(f"   {s.name} - тип БД: {s._db_type}, БД: {s._databases}")

print("\n3. Управление серверами (запуск/остановка):")
for server in col:
    print(f"   {server.name}: {server.stop()}")
    print(f"   {server.name}: {server.start()}")

print("\n4. Добавление подключений к серверам:")
for server in col:
    print(f"   {server.name}: {server.add_connection()}")
    print(f"   {server.name}: {server.add_connection()}")

print("\n" + "=" * 60)
