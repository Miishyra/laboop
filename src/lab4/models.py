from server import Server
from interfaces import Informable

class WebServer(Server, Informable):
    def __init__(self, name, ip_address, os_type, cpu_cores, ram_gb, domain):
        super().__init__(name, ip_address, os_type, cpu_cores, ram_gb)
        self._domain = domain
        self._sites = 0
    
    def add_site(self):
        if self._status != 'online':
            return "Сервер не запущен"
        self._sites += 1
        return f"Сайтов: {self._sites}"
    
    def get_score(self):
        return self._cpu_cores * self._ram_gb + self._sites * 10
    
    def get_info(self):
        info = super().get_info()
        info.append(f"Домен: {self._domain}")
        info.append(f"Сайтов: {self._sites}")
        return info
    
    def __str__(self):
        return f"[Web] {self._name} ({self._domain}) - {self._status}"


class DatabaseServer(Server, Informable):
    def __init__(self, name, ip_address, os_type, cpu_cores, ram_gb, db_type):
        super().__init__(name, ip_address, os_type, cpu_cores, ram_gb)
        self._db_type = db_type
        self._databases = 0
    
    def create_db(self):
        if self._status != 'online':
            return "Сервер не запущен"
        self._databases += 1
        return f"БД: {self._databases}"
    
    def get_score(self):
        return self._cpu_cores * self._ram_gb + self._databases * 50
    
    def get_info(self):
        info = super().get_info()
        info.append(f"Тип БД: {self._db_type}")
        info.append(f"Баз данных: {self._databases}")
        return info
    
    def __str__(self):
        return f"[DB] {self._name} ({self._db_type}) - {self._status}"