import json
import os

# ===== КЛАСС SERVER (прямо здесь) =====
class Server:
    total_servers = 0
    
    def __init__(self, name, ip, cpu, ram):
        if len(name) < 3:
            raise ValueError("Имя минимум 3 символа")
        self._name = name
        self._ip = ip
        self._cpu = cpu
        self._ram = ram
        self._status = 'offline'
        self._priority = 'medium'
        self._connections = 0
        Server.total_servers += 1
    
    @property
    def name(self):
        return self._name
    
    @property
    def ip(self):
        return self._ip
    
    @property
    def status(self):
        return self._status
    
    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, value):
        if value in ['low', 'medium', 'high']:
            self._priority = value
    
    @property
    def connections(self):
        return self._connections
    
    def start(self):
        self._status = 'online'
        return f"{self._name} запущен"
    
    def stop(self):
        self._status = 'offline'
        self._connections = 0
        return f"{self._name} остановлен"
    
    def add_connection(self):
        if self._status != 'online':
            return f"{self._name} не запущен"
        self._connections += 1
        return f"{self._name}: подключений {self._connections}"
    
    def get_score(self):
        return self._cpu * self._ram
    
    def __str__(self):
        return f"{self._name} ({self._ip}) - {self._status}, подкл:{self._connections}"


# ===== ИСКЛЮЧЕНИЯ =====
class DuplicateError(Exception):
    pass

class NotFoundError(Exception):
    pass


# ===== STORAGE =====
FILE = "data.json"

def save(servers):
    data = []
    for s in servers:
        data.append({
            "name": s.name,
            "ip": s.ip,
            "cpu": s._cpu,
            "ram": s._ram,
            "status": s.status,
            "priority": s.priority,
            "connections": s.connections
        })
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ===== APP =====
class ServerApp:
    def __init__(self):
        self._items = []
    
    def add(self, server):
        for s in self._items:
            if s.ip == server.ip:
                raise DuplicateError(f"IP {server.ip} уже существует")
        self._items.append(server)
    
    def remove(self, ip):
        for s in self._items:
            if s.ip == ip:
                self._items.remove(s)
                return s
        raise NotFoundError(f"Сервер с IP {ip} не найден")
    
    def get_all(self):
        return self._items.copy()
    
    def find_by_ip(self, ip):
        for s in self._items:
            if s.ip == ip:
                return s
        return None
    
    def find_by_name(self, name):
        return [s for s in self._items if s.name == name]
    
    def filter_by_status(self, status):
        return [s for s in self._items if s.status == status]
    
    def sort(self, key_func):
        self._items.sort(key=key_func)
    
    def __len__(self):
        return len(self._items)


# ===== CLI =====
class CLI:
    def __init__(self, app):
        self._app = app
    
    def run(self):
        while True:
            self._show_menu()
            choice = input("Выберите пункт: ")
            
            if choice == "0":
                print("До свидания!")
                break
            elif choice == "1":
                self._add()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._find()
            elif choice == "4":
                self._filter()
            elif choice == "5":
                self._sort()
            elif choice == "6":
                self._remove()
            else:
                print("Ошибка: неверный пункт")
    
    def _show_menu(self):
        print("\n" + "=" * 40)
        print("МЕНЮ")
        print("=" * 40)
        print("1. Добавить сервер")
        print("2. Показать все")
        print("3. Найти сервер")
        print("4. Фильтровать")
        print("5. Сортировать")
        print("6. Удалить сервер")
        print("0. Выход")
        print("-" * 40)
    
    def _add(self):
        print("\n--- ДОБАВЛЕНИЕ ---")
        try:
            name = input("Имя: ")
            ip = input("IP: ")
            cpu = int(input("CPU: "))
            ram = int(input("RAM: "))
            
            server = Server(name, ip, cpu, ram)
            self._app.add(server)
            print(f"✅ Сервер {name} добавлен")
        except DuplicateError as e:
            print(f"❌ {e}")
        except ValueError:
            print("❌ Ошибка: введите число")
    
    def _show_all(self):
        print("\n--- ВСЕ СЕРВЕРЫ ---")
        servers = self._app.get_all()
        if not servers:
            print("Пусто")
            return
        
        print("\n" + "-" * 60)
        print(f"{'Имя':<15} {'IP':<15} {'Статус':<10} {'Подкл':<6}")
        print("-" * 60)
        for s in servers:
            print(f"{s.name:<15} {s.ip:<15} {s.status:<10} {s.connections:<6}")
        print("-" * 60)
    
    def _find(self):
        print("\n--- ПОИСК ---")
        print("1. По IP")
        print("2. По имени")
        choice = input("Выберите: ")
        
        if choice == "1":
            ip = input("IP: ")
            s = self._app.find_by_ip(ip)
            if s:
                print(f"Найден: {s.name} ({s.ip})")
            else:
                print("Не найден")
        elif choice == "2":
            name = input("Имя: ")
            found = self._app.find_by_name(name)
            if found:
                for s in found:
                    print(f"  {s.name} ({s.ip})")
            else:
                print("Не найдены")
    
    def _filter(self):
        print("\n--- ФИЛЬТРАЦИЯ ---")
        status = input("Статус (online/offline/maintenance): ")
        filtered = self._app.filter_by_status(status)
        if filtered:
            for s in filtered:
                print(f"  {s.name} ({s.ip})")
        else:
            print("Серверов с таким статусом нет")
    
    def _sort(self):
        print("\n--- СОРТИРОВКА ---")
        print("1. По имени")
        print("2. По оценке")
        print("3. По подключениям")
        choice = input("Выберите: ")
        
        if choice == "1":
            self._app.sort(lambda s: s.name)
            print("✅ Отсортировано по имени")
        elif choice == "2":
            self._app.sort(lambda s: s.get_score())
            print("✅ Отсортировано по оценке")
        elif choice == "3":
            self._app.sort(lambda s: s.connections)
            print("✅ Отсортировано по подключениям")
        else:
            print("Неверный выбор")
            return
        self._show_all()
    
    def _remove(self):
        print("\n--- УДАЛЕНИЕ ---")
        ip = input("IP сервера: ")
        s = self._app.find_by_ip(ip)
        if not s:
            print("Сервер не найден")
            return
        
        print(f"Сервер: {s.name} ({s.ip})")
        confirm = input("Удалить? (y/n): ")
        if confirm.lower() == "y":
            try:
                self._app.remove(ip)
                print("✅ Удалён")
            except NotFoundError as e:
                print(f"❌ {e}")
        else:
            print("Отменено")


# ===== MAIN =====
def main():
    print("=" * 40)
    print("ЗАГРУЗКА...")
    print("=" * 40)
    
    app = ServerApp()
    
    data = load()
    for item in data:
        try:
            s = Server(item["name"], item["ip"], item["cpu"], item["ram"])
            s._status = item["status"]
            s._priority = item["priority"]
            s._connections = item["connections"]
            app.add(s)
        except:
            pass
    
    print(f"Загружено {len(app)} серверов")
    
    cli = CLI(app)
    try:
        cli.run()
    finally:
        save(app.get_all())
        print(f"\nСохранено {len(app)} серверов")

if __name__ == "__main__":
    main()