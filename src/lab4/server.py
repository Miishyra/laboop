from datetime import datetime

class Server:
    total_servers = 0
    
    def __init__(self, name, ip_address, os_type, cpu_cores, ram_gb):
        if len(name) < 3:
            raise ValueError("Имя минимум 3 символа")
        self._name = name
        self._ip_address = ip_address
        self._os_type = os_type
        self._cpu_cores = cpu_cores
        self._ram_gb = ram_gb
        self._status = 'offline'
        self._connections = 0
        Server.total_servers += 1
    
    @property
    def name(self):
        return self._name
    
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
    
    def get_info(self):
        return [f"Имя: {self._name}", f"IP: {self._ip_address}", f"Статус: {self._status}"]
    
    def __str__(self):
        return f"{self._name} ({self._ip_address}) - {self._status}"