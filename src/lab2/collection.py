from src.lab2.model import Server

class ServerCollection:
    """Контейнер для хранения объектов Server."""
    
    def __init__(self):
        """Инициализация пустой коллекции."""
        self._items = []  # хранилище объектов
    
    # ===== УПРАВЛЕНИЕ ДОБАВЛЕНИЕМ И УДАЛЕНИЕМ =====
    
    def add(self, server):
        """Добавить объект в коллекцию."""
        # Проверка типа
        if not isinstance(server, Server):
            raise TypeError("Можно добавлять только объекты Server")
        
        # Проверка на дубликат (по IP)
        for s in self._items:
            if s.ip == server.ip:
                raise ValueError(f"Сервер с IP {server.ip} уже существует")
        
        self._items.append(server)
    
    def remove(self, server):
        """Удалить объект из коллекции."""
        if server not in self._items:
            raise ValueError("Сервер не найден в коллекции")
        self._items.remove(server)
    
    def remove_at(self, index):
        """Удалить объект по индексу."""
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items.pop(index)
    
    # ===== ДОСТУП К ОБЪЕКТАМ =====
    
    def get_all(self):
        """Получить список всех объектов."""
        return self._items.copy()
    
    def get_by_index(self, index):
        """Получить объект по индексу."""
        return self._items[index]
    
    # ===== ПОИСК =====
    
    def find_by_name(self, name):
        """Найти серверы по имени."""
        result = []
        for s in self._items:
            if s.name == name:
                result.append(s)
        return result
    
    def find_by_ip(self, ip):
        """Найти сервер по IP."""
        for s in self._items:
            if s.ip == ip:
                return s
        return None
    
    def find_by_status(self, status):
        """Найти серверы по статусу."""
        result = []
        for s in self._items:
            if s.status == status:
                result.append(s)
        return result
    
    # ===== СОРТИРОВКА =====
    
    def sort_by_name(self):
        """Сортировка по имени."""
        self._items.sort(key=lambda s: s.name)
    
    def sort_by_connections(self):
        """Сортировка по количеству подключений."""
        self._items.sort(key=lambda s: s.connections)
    
    # ===== ФИЛЬТРАЦИЯ (возвращает новую коллекцию) =====
    
    def get_online(self):
        """Получить новую коллекцию только с онлайн серверами."""
        new_collection = ServerCollection()
        for s in self._items:
            if s.status == 'online':
                new_collection.add(s)
        return new_collection
    
    # ===== МАГИЧЕСКИЕ МЕТОДЫ ДЛЯ ИТЕРАЦИИ =====
    
    def __len__(self):
        """Возвращает количество объектов в коллекции."""
        return len(self._items)
    
    def __iter__(self):
        """Позволяет итерироваться по коллекции."""
        return iter(self._items)
    
    def __getitem__(self, index):
        """Позволяет обращаться по индексу collection[index]."""
        return self._items[index]
    
    def __str__(self):
        """Строковое представление коллекции."""
        if not self._items:
            return "Коллекция пуста"
        
        text = f"Коллекция серверов ({len(self._items)} шт.):\n"
        for i, s in enumerate(self._items):
            text += f"  [{i}] {s}\n"
        return text