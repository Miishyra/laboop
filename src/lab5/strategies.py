"""
Стратегии для сортировки, фильтрации и обработки серверов.
"""

# ===== ФУНКЦИИ ДЛЯ СОРТИРОВКИ (3 стратегии) =====
def by_name(server):
    """Сортировка по имени сервера."""
    return server.name

def by_score(server):
    """Сортировка по оценке производительности."""
    return server.get_score()

def by_connections(server):
    """Сортировка по количеству подключений."""
    return server.connections


# ===== ФУНКЦИИ ДЛЯ ФИЛЬТРАЦИИ (2 фильтра) =====
def is_online(server):
    """Фильтр: только онлайн серверы."""
    return server.status == 'online'

def is_high_priority(server):
    """Фильтр: только серверы с высоким приоритетом."""
    return server.priority == 'high'


# ===== ФАБРИКА ФУНКЦИЙ =====
def min_connections_filter(min_value):
    """
    Фабрика: создаёт фильтр для серверов с подключениями > min_value.
    
    Args:
        min_value: минимальное количество подключений
    
    Returns:
        функция-фильтр
    """
    def check(server):
        return server.connections > min_value
    return check


# ===== ФУНКЦИЯ ДЛЯ APPLY =====
def add_connection(server):
    """Добавить одно подключение к серверу."""
    return server.add_connection()


# ===== CALLABLE-ОБЪЕКТ (паттерн Стратегия) =====
class Counter:
    """
    Стратегия, которая считает количество применений.
    Хранит состояние между вызовами.
    """
    
    def __init__(self):
        self.count = 0
    
    def __call__(self, server):
        self.count += 1
        return f"{server.name}: обработан {self.count} раз"