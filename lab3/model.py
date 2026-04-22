import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab3.base import Server

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