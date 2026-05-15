"""
ЛР-6: ОБОБЩЕНИЯ И ТИПИЗАЦИЯ
ВСЁ В ОДНОМ ФАЙЛЕ
"""

from datetime import datetime
from typing import TypeVar, Generic, Callable, Optional, List, Protocol

# ============================================================
# 1. КЛАСС SERVER (как в lab1)
# ============================================================
class Server:
    total_servers: int = 0
    
    def __init__(self, name: str, ip: str, cpu: int, ram: int) -> None:
        if len(name) < 3:
            raise ValueError("Имя минимум 3 символа")
        self._name: str = name
        self._ip: str = ip
        self._cpu: int = cpu
        self._ram: int = ram
        self._status: str = 'offline'
        self._priority: str = 'medium'
        self._connections: int = 0
        Server.total_servers += 1
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def ip(self) -> str:
        return self._ip
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def priority(self) -> str:
        return self._priority
    
    @priority.setter
    def priority(self, value: str) -> None:
        if value in ['low', 'medium', 'high']:
            self._priority = value
    
    @property
    def connections(self) -> int:
        return self._connections
    
    def start(self) -> str:
        self._status = 'online'
        return f"{self._name} запущен"
    
    def stop(self) -> str:
        self._status = 'offline'
        self._connections = 0
        return f"{self._name} остановлен"
    
    def add_connection(self) -> str:
        if self._status != 'online':
            return f"{self._name} не запущен"
        self._connections += 1
        return f"{self._name}: подключений {self._connections}"
    
    def get_score(self) -> int:
        return self._cpu * self._ram
    
    def display(self) -> str:
        return f"{self._name} ({self._ip}) - {self._status}"
    
    def __str__(self) -> str:
        return f"{self._name} ({self._ip}) - {self._status}, подкл:{self._connections}"


# ============================================================
# 2. КЛАССЫ ИЗ lab3
# ============================================================
class WebServer(Server):
    def __init__(self, name: str, ip: str, cpu: int, ram: int, domain: str) -> None:
        super().__init__(name, ip, cpu, ram)
        self._domain: str = domain
        self._sites: int = 0
    
    def add_site(self) -> str:
        if self._status != 'online':
            return "Сервер не запущен"
        self._sites += 1
        return f"Сайтов: {self._sites}"
    
    def get_score(self) -> int:
        return super().get_score() + self._sites * 10
    
    def display(self) -> str:
        return f"[Web] {self._name} ({self._domain}) - {self._status}"
    
    def __str__(self) -> str:
        return f"[Web] {self._name} ({self._domain}) - {self._status}"


class DatabaseServer(Server):
    def __init__(self, name: str, ip: str, cpu: int, ram: int, db_type: str) -> None:
        super().__init__(name, ip, cpu, ram)
        self._db_type: str = db_type
        self._databases: int = 0
    
    def create_db(self) -> str:
        if self._status != 'online':
            return "Сервер не запущен"
        self._databases += 1
        return f"БД: {self._databases}"
    
    def get_score(self) -> int:
        return super().get_score() + self._databases * 50
    
    def display(self) -> str:
        return f"[DB] {self._name} ({self._db_type}) - {self._status}"
    
    def __str__(self) -> str:
        return f"[DB] {self._name} ({self._db_type}) - {self._status}"


# ============================================================
# 3. ПРОТОКОЛЫ
# ============================================================
class Displayable(Protocol):
    def display(self) -> str:
        ...

class Scorable(Protocol):
    def get_score(self) -> int:
        ...


# ============================================================
# 4. TYPEVAR
# ============================================================
T = TypeVar('T')
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
R = TypeVar('R')


# ============================================================
# 5. TYPED COLLECTION
# ============================================================
class TypedCollection(Generic[T]):
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        self._items.remove(item)
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    
    def __str__(self) -> str:
        if not self._items:
            return "Коллекция пуста"
        text: str = f"Коллекция ({len(self._items)} шт.):\n"
        for i, s in enumerate(self._items):
            text += f"  [{i}] {s}\n"
        return text


# ============================================================
# 6. ОГРАНИЧЕННЫЕ КОЛЛЕКЦИИ
# ============================================================
class DisplayableCollection(TypedCollection[D]):
    pass

class ScorableCollection(TypedCollection[S]):
    pass


# ============================================================
# 7. ДЕМОНСТРАЦИЯ
# ============================================================
print("=" * 60)
print("ЛР-6: ОБОБЩЕНИЯ И ТИПИЗАЦИЯ")
print("=" * 60)

# СОЗДАНИЕ СЕРВЕРОВ
print("\n1. СОЗДАНИЕ СЕРВЕРОВ")

w1 = WebServer("Alpha", "10.0.0.1", 4, 16, "alpha.com")
w2 = WebServer("Gamma", "10.0.0.2", 8, 32, "gamma.com")
db1 = DatabaseServer("Beta", "10.0.0.3", 16, 64, "PostgreSQL")
db2 = DatabaseServer("Delta", "10.0.0.4", 2, 8, "MySQL")

for s in [w1, w2, db1, db2]:
    s.start()

w1.add_site()
w1.add_site()
w2.add_site()
db1.create_db()
db1.create_db()
w1.add_connection()
w1.add_connection()
w2.add_connection()
db1.add_connection()
w1.priority = "high"
w2.priority = "high"

# TYPED COLLECTION
print("\n2. TYPED COLLECTION")
col: TypedCollection[WebServer] = TypedCollection()
col.add(w1)
col.add(w2)
print(col)

# FIND
print("\n3. FIND")
found = col.find(lambda s: s.name == "Alpha")
print(f"Найден сервер с именем Alpha: {found}")
not_found = col.find(lambda s: s.name == "None")
print(f"Поиск несуществующего: {not_found}")

# FILTER
print("\n4. FILTER")
high_score = col.filter(lambda s: s.get_score() > 300)
print(f"Серверы с score > 300: {[s.name for s in high_score]}")

# MAP
print("\n5. MAP")
names = col.map(lambda s: s.name)
print(f"Имена: {names}")
scores = col.map(lambda s: s.get_score())
print(f"Оценки: {scores}")

# DISPLAYABLE COLLECTION
print("\n6. DISPLAYABLE COLLECTION")
d_col: DisplayableCollection = DisplayableCollection()
d_col.add(w1)
d_col.add(w2)
d_col.add(db1)
d_col.add(db2)
for item in d_col:
    print(f"  {item.display()}")

# SCORABLE COLLECTION
print("\n7. SCORABLE COLLECTION")
s_col: ScorableCollection = ScorableCollection()
s_col.add(w1)
s_col.add(w2)
s_col.add(db1)
s_col.add(db2)
for item in s_col:
    print(f"  {item.name}: score = {item.get_score()}")
