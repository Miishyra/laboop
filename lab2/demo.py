from model import Server
from collection import ServerCollection

# СОЗДАНИЕ ОБЪЕКТОВ
s1 = Server("Web", "192.168.1.1", "Linux", 4, 16)
s2 = Server("Database", "192.168.1.2", "Windows", 8, 32)
s3 = Server("Mail", "192.168.1.3", "Linux", 2, 8)

s1.start()
s2.start()
s1.add_connection()
s1.add_connection()
s2.add_connection()
s1.priority = "high"

col = ServerCollection()
col.add(s1)
col.add(s2)
col.add(s3)

# ===== СЦЕНАРИЙ 1: Просмотр серверов =====
print("=== СЦЕНАРИЙ 1: Просмотр всех серверов ===")
print(col)  # показывает __str__ коллекции
print(f"Всего серверов: {len(col)}")  # показывает __len__

# ===== СЦЕНАРИЙ 2: Поиск серверов =====
print("\n=== СЦЕНАРИЙ 2: Поиск серверов ===")
print(f"Поиск по имени 'Web': {col.find_by_name('Web')[0]}")  # поиск
print(f"Поиск по IP '192.168.1.2': {col.find_by_ip('192.168.1.2')}")  # поиск

print("Серверы с высоким приоритетом:")
for s in col:  # итерация
    if s.priority == "high":
        print(f"  {s.name}")

# ===== СЦЕНАРИЙ 3: Управление серверами =====
print("\n=== СЦЕНАРИЙ 3: Управление серверами ===")
print(f"col[0] = {col[0]}")  # индексация

col.sort_by_name()  # сортировка
print("После сортировки по имени:")
print(col)

print("Онлайн серверы:")  # фильтрация
for s in col.get_online():
    print(f"  {s.name} - {s.connections} подключений")
    s.stop()  # действие

print("\nРезультат:")
for s in col.get_all():
    print(f"  {s.name} - {s.status}")