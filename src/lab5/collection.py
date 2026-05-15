import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab3.model import WebServer, DatabaseServer
from lab5.collection import ServerCollection
from lab5.strategies import *

print("=" * 60)
print("ЛР-5: ФУНКЦИИ КАК АРГУМЕНТЫ")
print("=" * 60)

# СОЗДАНИЕ 5 СЕРВЕРОВ
s1 = WebServer("Alpha", "10.0.0.1", 4, 16, "alpha.com")
s2 = WebServer("Gamma", "10.0.0.2", 8, 32, "gamma.com")
s3 = DatabaseServer("Beta", "10.0.0.3", 16, 64, "PG")
s4 = WebServer("Delta", "10.0.0.4", 2, 8, "delta.com")
s5 = DatabaseServer("Epsilon", "10.0.0.5", 8, 32, "MY")

for s in [s1, s2, s3, s4, s5]:
    s.start()

s1.add_site()
s1.add_site()
s2.add_site()
s3.create_db()
s3.create_db()
s1.add_connection()
s1.add_connection()
s2.add_connection()
s3.add_connection()
s1.priority = "high"
s2.priority = "high"
s3.priority = "high"

col = ServerCollection()
for s in [s1, s2, s3, s4, s5]:
    col.add(s)

print(f"\nСоздано {len(col)} серверов\n")

# СОРТИРОВКА
print("-" * 40)
print("СОРТИРОВКА")
print("-" * 40)

print("По имени:")
for s in col.copy().sort_by(by_name):
    print(f"  {s.name}")

print("\nПо оценке:")
for s in col.copy().sort_by(by_score):
    print(f"  {s.name}: {s.get_score()}")

print("\nПо подключениям:")
for s in col.copy().sort_by(by_connections):
    print(f"  {s.name}: {s.connections}")

# ФИЛЬТРАЦИЯ
print("\n" + "-" * 40)
print("ФИЛЬТРАЦИЯ")
print("-" * 40)

print("Онлайн серверы:")
for s in col.filter_by(is_online):
    print(f"  {s.name}")

print("\nHigh priority:")
for s in col.filter_by(is_high_priority):
    print(f"  {s.name}")

# MAP
print("\n" + "-" * 40)
print("MAP")
print("-" * 40)

names = list(map(lambda s: s.name, col.get_all()))
print(f"Имена: {names}")

# ФАБРИКА
print("\n" + "-" * 40)
print("ФАБРИКА")
print("-" * 40)

f = min_connections_filter(1)
print("Подключений > 1:")
for s in col.filter_by(f):
    print(f"  {s.name}: {s.connections}")

# ЦЕПОЧКА (СЦЕНАРИЙ 1)
print("\n" + "-" * 40)
print("СЦЕНАРИЙ 1: ЦЕПОЧКА")
print("-" * 40)

res = (col
    .filter_by(is_online)
    .sort_by(by_score)
    .apply(add_connection))

for r in res:
    print(f"  {r}")

# ЗАМЕНА СТРАТЕГИИ (СЦЕНАРИЙ 2)
print("\n" + "-" * 40)
print("СЦЕНАРИЙ 2: ЗАМЕНА СТРАТЕГИИ")
print("-" * 40)

f2 = min_connections_filter(0)
print("Другой фильтр (подключений > 0):")
for s in col.filter_by(f2):
    print(f"  {s.name}: {s.connections}")

# CALLABLE (СЦЕНАРИЙ 3)
print("\n" + "-" * 40)
print("СЦЕНАРИЙ 3: CALLABLE-ОБЪЕКТ")
print("-" * 40)

c = Counter()
col.apply(c)
col.apply(c)
res = col.apply(c)
for r in res:
    print(f"  {r}")

print("\n" + "=" * 60)
print("ГОТОВО")
print("=" * 60)