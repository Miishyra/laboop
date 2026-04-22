class Server:
    """Базовый класс для всех серверов."""
    
    total_servers = 0
    
    def __init__(self, name, ip, cpu, ram):
        if len(name) < 3:
            raise ValueError("Имя минимум 3 символа")
        self._name = name
        self._ip = ip
        self._cpu = cpu
        self._ram = ram
        self._status = 'offline'
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
            return "Сервер не запущен"
        self._connections += 1
        return f"Подключений: {self._connections}"
    
    def get_score(self):
        """Базовый метод для расчета производительности."""
        return self._cpu * self._ram
    
    def __str__(self):
        return f"{self._name} ({self._ip}) - {self._status}"
    
    def __eq__(self, other):
        if not isinstance(other, Server):
            return False
        return self._ip == other._ip