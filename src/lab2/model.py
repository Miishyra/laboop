from datetime import datetime
from src.lab2.validation import validate_name, validate_ip, validate_os, validate_cpu, validate_ram

class Server:
    available_os = ['Linux', 'Windows', 'MacOS']
    total_servers = 0
    
    def __init__(self, name, ip, os_type, cpu, ram):
        validate_name(name)
        validate_ip(ip)
        validate_os(os_type, Server.available_os)
        validate_cpu(cpu)
        validate_ram(ram)
        
        self._name = name
        self._ip = ip
        self._os = os_type
        self._cpu = cpu
        self._ram = ram
        self._status = 'offline'
        self._priority = 'medium'
        self._connections = 0
        self._created_at = datetime.now()
        
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
    
    @property
    def connections(self):
        return self._connections
    
    @status.setter
    def status(self, value):
        if value not in ['offline', 'online', 'maintenance']:
            raise ValueError("Статус должен быть: offline, online, maintenance")
        self._status = value
    
    @priority.setter
    def priority(self, value):
        if value not in ['low', 'medium', 'high']:
            raise ValueError("Приоритет должен быть: low, medium, high")
        self._priority = value
    
    def start(self):
        if self._status == 'online':
            return "Уже запущен"
        self._status = 'online'
        return "Запущен"
    
    def stop(self):
        if self._status == 'offline':
            return "Уже остановлен"
        self._status = 'offline'
        self._connections = 0
        return "Остановлен"
    
    def add_connection(self):
        if self._status != 'online':
            return "Сервер не запущен"
        self._connections += 1
        return f"Подключений: {self._connections}"
    
    def __str__(self):
        return f"{self._name} ({self._ip}) - {self._status}, подкл:{self._connections}"
    
    def __eq__(self, other):
        if not isinstance(other, Server):
            return False
        return self._ip == other._ip