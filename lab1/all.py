from datetime import datetime

class Server:
    available_os = ['Linux', 'Windows', 'MacOS']
    total_servers = 0
    
    def __init__(self, name, ip_address, os_type, cpu_cores, ram_gb):
        if type(name) != str:
            raise TypeError("Имя должно быть строкой")
        if len(name) < 3:
            raise ValueError("Имя должно содержать минимум 3 символа")
        
        if type(ip_address) != str:
            raise TypeError("IP-адрес должен быть строкой")
        if '.' not in ip_address:
            raise ValueError("IP-адрес должен содержать точки, например: 192.168.1.1")
        
        if os_type not in Server.available_os:
            raise ValueError(f"ОС должна быть одной из: {Server.available_os}")
        
        if type(cpu_cores) != int:
            raise TypeError("Количество ядер CPU должно быть целым числом")
        if cpu_cores <= 0:
            raise ValueError("Количество ядер CPU должно быть больше 0")
        if cpu_cores > 64:
            raise ValueError("Количество ядер CPU не может быть больше 64")
        
        if type(ram_gb) != int:
            raise TypeError("Объем RAM должен быть целым числом")
        if ram_gb <= 0:
            raise ValueError("Объем RAM должен быть больше 0")
        if ram_gb > 512:
            raise ValueError("Объем RAM не может быть больше 512 ГБ")
        
        self._name = name
        self._ip_address = ip_address
        self._os_type = os_type
        self._cpu_cores = cpu_cores
        self._ram_gb = ram_gb
        self._status = 'offline'
        self._priority = 'medium'
        self._connections = 0
        self._created_at = datetime.now()
        self._last_boot = None
        
        Server.total_servers += 1
    
    @property
    def name(self):
        return self._name
    
    @property
    def ip_address(self):
        return self._ip_address
    
    @property
    def os_type(self):
        return self._os_type
    
    @property
    def cpu_cores(self):
        return self._cpu_cores
    
    @property
    def ram_gb(self):
        return self._ram_gb
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):
        allowed_statuses = ['offline', 'online', 'maintenance']
        if new_status not in allowed_statuses:
            raise ValueError(f"Статус должен быть: {allowed_statuses}")
        
        self._status = new_status
        if new_status == 'online':
            self._last_boot = datetime.now()
        if new_status == 'offline':
            self._connections = 0
    
    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, new_priority):
        allowed_priorities = ['low', 'medium', 'high']
        if new_priority not in allowed_priorities:
            raise ValueError(f"Приоритет должен быть: {allowed_priorities}")
        self._priority = new_priority
    
    @property
    def connections(self):
        return self._connections
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def uptime(self):
        if self._status != 'online' or self._last_boot is None:
            return "Сервер не запущен"
        
        delta = datetime.now() - self._last_boot
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if delta.days > 0:
            return f"{delta.days}д {hours}ч {minutes}мин"
        else:
            return f"{hours}ч {minutes}мин"
    
    def start(self):
        if self._status == 'online':
            return f"Сервер {self._name} уже запущен"
        if self._status == 'maintenance':
            return f"Сервер {self._name} на обслуживании"
        
        self._status = 'online'
        self._last_boot = datetime.now()
        return f"Сервер {self._name} запущен"
    
    def stop(self):
        if self._status == 'offline':
            return f"Сервер {self._name} уже остановлен"
        
        self._status = 'offline'
        self._connections = 0
        return f"Сервер {self._name} остановлен"
    
    def maintenance(self):
        if self._status == 'maintenance':
            return f"Сервер {self._name} уже на обслуживании"
        
        self._status = 'maintenance'
        self._connections = 0
        return f"Сервер {self._name} переведен на обслуживание"
    
    def add_connection(self):
        if self._status != 'online':
            return f"Ошибка: сервер {self._name} не запущен"
        
        self._connections += 1
        return f"Подключение добавлено. Всего: {self._connections}"
    
    def remove_connection(self):
        if self._connections <= 0:
            return "Нет активных подключений"
        
        self._connections -= 1
        return f"Подключение удалено. Осталось: {self._connections}"
    
    def get_info(self):
        info = []
        info.append(f"Имя: {self._name}")
        info.append(f"IP: {self._ip_address}")
        info.append(f"ОС: {self._os_type}")
        info.append(f"CPU: {self._cpu_cores} ядер")
        info.append(f"RAM: {self._ram_gb} ГБ")
        info.append(f"Статус: {self._status}")
        info.append(f"Приоритет: {self._priority}")
        info.append(f"Подключения: {self._connections}")
        info.append(f"Создан: {self._created_at.strftime('%d.%m.%Y %H:%M')}")
        info.append(f"Время работы: {self.uptime}")
        return info
    
    def __str__(self):
        return f"{self._name} ({self._ip_address}) - {self._status}, подкл: {self._connections}"
    
    def __repr__(self):
        return f"Server('{self._name}', '{self._ip_address}', '{self._os_type}')"
    
    def __eq__(self, other):
        if not isinstance(other, Server):
            return False
        return self._ip_address == other._ip_address


def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)


# ========== 1. СОЗДАНИЕ ОБЪЕКТОВ И ПРОВЕРКА СВОЙСТВ ==========
print_header("1. СОЗДАНИЕ СЕРВЕРОВ")

server1 = Server("WebServer", "192.168.1.10", "Linux", 4, 16)
server2 = Server("DBServer", "192.168.1.20", "Windows", 8, 32)

print("Созданы серверы:")
print(server1)
print(server2)

print(f"\nВсего создано серверов: {Server.total_servers}")

print(f"\nИмя: {server1.name}")
print(f"IP: {server1.ip_address}")
print(f"Статус: {server1.status}")
print(f"Приоритет: {server1.priority}")
print(f"Подключения: {server1.connections}")
print(f"Создан: {server1.created_at.strftime('%d.%m.%Y %H:%M')}")

# ========== 2. ИЗМЕНЕНИЕ СОСТОЯНИЯ ЧЕРЕЗ SETTER ==========
print_header("2. ИЗМЕНЕНИЕ СТАТУСА И ПРИОРИТЕТА ЧЕРЕЗ SETTER")

print(f"Текущий статус: {server1.status}")
server1.status = 'online'
print(f"Статус после setter: {server1.status}")

print(server1.add_connection())
print(server1.add_connection())
print(f"Подключения: {server1.connections}")

print(f"\nТекущий приоритет: {server2.priority}")
server2.priority = 'high'
print(f"Приоритет после setter: {server2.priority}")

try:
    print("\nПытаемся установить неверный приоритет...")
    server2.priority = 'super'
except ValueError as e:
    print(f"Ошибка: {e}")

# ========== 3. СРАВНЕНИЕ ОБЪЕКТОВ ==========
print_header("3. СРАВНЕНИЕ СЕРВЕРОВ")

server3 = Server("NewWeb", "192.168.1.10", "Linux", 4, 16)
server4 = Server("Backup", "192.168.1.50", "Linux", 2, 8)

print(f"server1 == server3: {server1 == server3} (одинаковый IP)")
print(f"server1 == server4: {server1 == server4} (разные IP)")

# ========== 4. ОБРАБОТКА ОШИБОК ПРИ СОЗДАНИИ ==========
print_header("4. ОБРАБОТКА ОШИБОК")

try:
    print("Пытаемся создать сервер с именем 'AB'...")
    bad_server = Server("AB", "192.168.1.100", "Linux", 2, 8)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    print("\nПытаемся установить неверный статус...")
    server1.status = 'unknown'
except ValueError as e:
    print(f"Ошибка: {e}")