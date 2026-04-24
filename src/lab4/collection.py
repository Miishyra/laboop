class ServerCollection:
    def __init__(self):
        self._items = []
    
    def add(self, server):
        self._items.append(server)
    
    def get_all(self):
        return self._items[:]
    
    def __iter__(self):
        return iter(self._items)
    
    def __str__(self):
        if not self._items:
            return "Пустая коллекция"
        result = f"Серверов: {len(self._items)}\n"
        for i, s in enumerate(self._items):
            result += f"  [{i}] {s}\n"
        return result