"""
ЛР-5: ФУНКЦИИ КАК АРГУМЕНТЫ. СТРАТЕГИИ И ДЕЛЕГАТЫ.
"""

from datetime import datetime

# ============================================================
# 1. КЛАСС SERVER (из lab1)
# ============================================================
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


# ============================================================
# 2. КЛАССЫ ИЗ lab3 (WebServer, DatabaseServer)
# ============================================================
class WebServer(Server):
    def __init__(self, name, ip, cpu, ram, domain):
        super().__init__(name, ip, cpu, ram)
        self._domain = domain
        self._sites = 0
    
    def add_site(self):
        if self._status != 'online':
            return "Сервер не запущен"
        self._sites += 1
        return f"Сайтов: {self._sites}"
    
    def get_score(self):
        return super().get_score() + self._sites * 10
    
    def __str__(self):
        return f"[Web] {self._name} ({self._domain}) - {self._status}"


class DatabaseServer(Server):
    def __init__(self, name, ip, cpu, ram, db_type):
        super().__init__(name, ip, cpu, ram)
        self._db_type = db_type
        self._databases = 0
    
    def create_db(self):
        if self._status != 'online':
            return "Сервер не запущен"
        self._databases += 1
        return f"БД: {self._databases}"
    
    def get_score(self):
        return super().get_score() + self._databases * 50
    
    def __str__(self):
        return f"[DB] {self._name} ({self._db_type}) - {self._status}"


# ============================================================
# 3. КОЛЛЕКЦИЯ (как в lab2)
# ============================================================
class ServerCollection:
    def __init__(self):
        self._items = []
    
    def add(self, server):
        self._items.append(server)
    
    def get_all(self):
        return self._items[:]
    
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def sort_by(self, key_func):
        self._items.sort(key=key_func)
        return self
    
    def filter_by(self, condition):
        new = ServerCollection()
        for s in self._items:
            if condition(s):
                new.add(s)
        return new
    
    def apply(self, func):
        return [func(s) for s in self._items]
    
    def copy(self):
        new = ServerCollection()
        for s in self._items:
            new.add(s)
        return new
    
    def __str__(self):
        if not self._items:
            return "Пустая коллекция"
        result = f"Серверов: {len(self._items)}\n"
        for i, s in enumerate(self._items):
            result += f"  [{i}] {s}\n"
        return result


# ============================================================
# 4. СТРАТЕГИИ
# ============================================================
def by_name(s):
    return s.name

def by_score(s):
    return s.get_score()

def by_connections(s):
    return s.connections

def is_online(s):
    return s.status == 'online'

def is_high_priority(s):
    return s.priority == 'high'

def min_connections_filter(min_val):
    def check(s):
        return s.connections > min_val
    return check

def add_connection(s):
    return s.add_connection()


class Counter:
    def __init__(self):
        self.count = 0
    def __call__(self, s):
        self.count += 1
        return f"{s.name}: {self.count}"


# ============================================================
# 5. ДЕМОНСТРАЦИЯ
# ============================================================
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
print("СОРТИРОВКА (3 стратегии)")
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
print("ФИЛЬТРАЦИЯ (2 фильтра)")
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
print("ФАБРИКА ФУНКЦИЙ")
print("-" * 40)

f = min_connections_filter(1)
print("Подключений > 1:")
for s in col.filter_by(f):
    print(f"  {s.name}: {s.connections}")

# СЦЕНАРИЙ 1: ЦЕПОЧКА
print("\n" + "-" * 40)
print("СЦЕНАРИЙ 1: ЦЕПОЧКА filter -> sort -> apply")
print("-" * 40)

res = (col
    .filter_by(is_online)
    .sort_by(by_score)
    .apply(add_connection))

for r in res:
    print(f"  {r}")

# СЦЕНАРИЙ 2: ЗАМЕНА СТРАТЕГИИ
print("\n" + "-" * 40)
print("СЦЕНАРИЙ 2: ЗАМЕНА СТРАТЕГИИ")
print("-" * 40)

print("Другой фильтр (подключений > 0):")
f2 = min_connections_filter(0)
for s in col.filter_by(f2):
    print(f"  {s.name}: {s.connections}")

# СЦЕНАРИЙ 3: CALLABLE
print("\n" + "-" * 40)
print("СЦЕНАРИЙ 3: CALLABLE-ОБЪЕКТ")
print("-" * 40)

c = Counter()
col.apply(c)
col.apply(c)
res = col.apply(c)
for r in res:
    print(f"  {r}")
