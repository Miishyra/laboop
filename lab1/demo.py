from model import Server

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

# ========== 1: СОЗДАНИЕ ОБЪЕКТОВ И ПРОВЕРКА СВОЙСТВ ==========
print_header("1: СОЗДАНИЕ СЕРВЕРОВ")

server1 = Server("WebServer", "192.168.1.10", "Linux", 4, 16)
server2 = Server("DBServer", "192.168.1.20", "Windows", 8, 32)

print("Созданы серверы:")
print(server1)
print(server2)

print(f"\nВсего создано серверов: {Server.total_servers}")

print(f"\nИмя: {server1.name}")
print(f"IP: {server1.ip_address}")
print(f"Статус: {server1.status}")
print(f"Приоритет: {server1.priority}")
print(f"Подключения: {server1.connections}")
print(f"Создан: {server1.created_at.strftime('%d.%m.%Y %H:%M')}")

# ========== 2: ИЗМЕНЕНИЕ СОСТОЯНИЯ ЧЕРЕЗ SETTER ==========
print_header("2: ИЗМЕНЕНИЕ СТАТУСА И ПРИОРИТЕТА ЧЕРЕЗ SETTER")

print(f"Текущий статус: {server1.status}")
server1.status = 'online'
print(f"Статус после setter: {server1.status}")

print(server1.add_connection())
print(server1.add_connection())
print(f"Подключения: {server1.connections}")

print(f"\nТекущий приоритет: {server2.priority}")
server2.priority = 'high'
print(f"Приоритет после setter: {server2.priority}")

try:
    print("\nПытаемся установить неверный приоритет...")
    server2.priority = 'super'
except ValueError as e:
    print(f"Ошибка: {e}")

# ========== 3: СРАВНЕНИЕ ОБЪЕКТОВ ==========
print_header("3: СРАВНЕНИЕ СЕРВЕРОВ")

server3 = Server("NewWeb", "192.168.1.10", "Linux", 4, 16)
server4 = Server("Backup", "192.168.1.50", "Linux", 2, 8)

print(f"server1 == server3: {server1 == server3} (одинаковый IP)")
print(f"server1 == server4: {server1 == server4} (разные IP)")

# ========== 4: ОБРАБОТКА ОШИБОК ПРИ СОЗДАНИИ ==========
print_header("4: ОБРАБОТКА ОШИБОК")

try:
    print("Пытаемся создать сервер с именем 'AB'...")
    bad_server = Server("AB", "192.168.1.100", "Linux", 2, 8)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    print("\nПытаемся установить неверный статус...")
    server1.status = 'unknown'
except ValueError as e:
    print(f"Ошибка: {e}")