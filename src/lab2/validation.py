def validate_name(name):
    if type(name) != str:
        raise TypeError("Имя должно быть строкой")
    if len(name) < 3:
        raise ValueError("Имя должно содержать минимум 3 символа")

def validate_ip(ip_address):
    if type(ip_address) != str:
        raise TypeError("IP-адрес должен быть строкой")
    if '.' not in ip_address:
        raise ValueError("IP-адрес должен содержать точки")
    
    parts = ip_address.split('.')
    if len(parts) != 4:
        raise ValueError("IP-адрес должен содержать 4 части")
    
    for part in parts:
        if not part.isdigit():
            raise ValueError("Части IP-адреса должны быть числами")
        num = int(part)
        if num < 0 or num > 255:
            raise ValueError("Части IP-адреса должны быть от 0 до 255")

def validate_os(os_type, available_os):
    if os_type not in available_os:
        raise ValueError(f"ОС должна быть одной из: {available_os}")

def validate_cpu(cpu_cores):
    if type(cpu_cores) != int:
        raise TypeError("Количество ядер CPU должно быть целым числом")
    if cpu_cores <= 0:
        raise ValueError("Количество ядер CPU должно быть больше 0")
    if cpu_cores > 64:
        raise ValueError("Количество ядер CPU не может быть больше 64")

def validate_ram(ram_gb):
    if type(ram_gb) != int:
        raise TypeError("Объем RAM должен быть целым числом")
    if ram_gb <= 0:
        raise ValueError("Объем RAM должен быть больше 0")
    if ram_gb > 512:
        raise ValueError("Объем RAM не может быть больше 512 ГБ")