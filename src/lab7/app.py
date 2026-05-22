import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab1.model import Server
from lab7.exceptions import DuplicateError, NotFoundError

class ServerApp:
    def __init__(self):
        self._items = []
    
    def add(self, server):
        for s in self._items:
            if s.ip == server.ip:
                raise DuplicateError(f"IP {server.ip} уже существует")
        self._items.append(server)
    
    def remove(self, ip):
        for s in self._items:
            if s.ip == ip:
                self._items.remove(s)
                return s
        raise NotFoundError(f"Сервер с IP {ip} не найден")
    
    def get_all(self):
        return self._items.copy()
    
    def find_by_ip(self, ip):
        for s in self._items:
            if s.ip == ip:
                return s
        return None
    
    def find_by_name(self, name):
        return [s for s in self._items if s.name == name]
    
    def filter_by_status(self, status):
        return [s for s in self._items if s.status == status]
    
    def sort(self, key_func):
        self._items.sort(key=key_func)
    
    def __len__(self):
        return len(self._items)