from models import WebServer, DatabaseServer
from interfaces import Startable, Scorable, Informable
from collection import ServerCollection

print("=" * 60)
print("ЛР-4: ИНТЕРФЕЙСЫ")
print("=" * 60)

web = WebServer("Web", "192.168.1.10", "Linux", 8, 32, "example.com")
db = DatabaseServer("Database", "192.168.1.20", "Windows", 16, 64, "PostgreSQL")  # DB -> Database

web.start()
db.start()
web.add_site()
web.add_site()
db.create_db()

print("\n1. ПРОВЕРКА ИНТЕРФЕЙСОВ")
print(f"  WebServer -> Startable: {isinstance(web, Startable)}")
print(f"  WebServer -> Scorable: {isinstance(web, Scorable)}")
print(f"  WebServer -> Informable: {isinstance(web, Informable)}")

print("\n2. РАБОТА ЧЕРЕЗ ИНТЕРФЕЙСЫ")

def show_info(obj: Informable):
    info = obj.get_info()
    for line in info[:4]:
        print(f"    {line}")

print("  Информация о WebServer:")
show_info(web)

print("\n  Информация о DatabaseServer:")
show_info(db)

print("\n3. ОЦЕНКИ ПРОИЗВОДИТЕЛЬНОСТИ")
for s in [web, db]:
    print(f"    {s.name}: {s.get_score()}")

print("\n4. КОЛЛЕКЦИЯ")
col = ServerCollection()
col.add(web)
col.add(db)

for s in col:
    print(f"    {s}")

print("\n5. ФИЛЬТРАЦИЯ ПО ИНТЕРФЕЙСУ")
informable_objects = [s for s in col.get_all() if isinstance(s, Informable)]
print(f"  Объектов с Informable: {len(informable_objects)}")

print("=" * 60)