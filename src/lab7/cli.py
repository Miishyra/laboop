import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab1.model import Server
from lab7.exceptions import DuplicateError, NotFoundError

class CLI:
    def __init__(self, app):
        self._app = app
    
    def run(self):
        while True:
            self._show_menu()
            choice = input("Выберите пункт: ")
            
            if choice == "0":
                print("До свидания!")
                break
            elif choice == "1":
                self._add()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._find()
            elif choice == "4":
                self._filter()
            elif choice == "5":
                self._sort()
            elif choice == "6":
                self._remove()
            else:
                print("Ошибка: неверный пункт")
    
    def _show_menu(self):
        print("\n" + "=" * 40)
        print("МЕНЮ")
        print("=" * 40)
        print("1. Добавить сервер")
        print("2. Показать все")
        print("3. Найти сервер")
        print("4. Фильтровать")
        print("5. Сортировать")
        print("6. Удалить сервер")
        print("0. Выход")
        print("-" * 40)
    
    def _add(self):
        print("\n--- ДОБАВЛЕНИЕ ---")
        try:
            name = input("Имя: ")
            ip = input("IP: ")
            cpu = int(input("CPU: "))
            ram = int(input("RAM: "))
            
            server = Server(name, ip, cpu, ram)
            self._app.add(server)
            print(f"✅ Сервер {name} добавлен")
        except DuplicateError as e:
            print(f"❌ {e}")
        except ValueError:
            print("❌ Ошибка: введите число")
    
    def _show_all(self):
        print("\n--- ВСЕ СЕРВЕРЫ ---")
        servers = self._app.get_all()
        if not servers:
            print("Пусто")
            return
        
        print("\n" + "-" * 60)
        print(f"{'Имя':<15} {'IP':<15} {'Статус':<10} {'Подкл':<6}")
        print("-" * 60)
        for s in servers:
            print(f"{s.name:<15} {s.ip:<15} {s.status:<10} {s.connections:<6}")
        print("-" * 60)
    
    def _find(self):
        print("\n--- ПОИСК ---")
        print("1. По IP")
        print("2. По имени")
        choice = input("Выберите: ")
        
        if choice == "1":
            ip = input("IP: ")
            s = self._app.find_by_ip(ip)
            if s:
                print(f"Найден: {s.name} ({s.ip})")
            else:
                print("Не найден")
        elif choice == "2":
            name = input("Имя: ")
            found = self._app.find_by_name(name)
            if found:
                for s in found:
                    print(f"  {s.name} ({s.ip})")
            else:
                print("Не найдены")
    
    def _filter(self):
        print("\n--- ФИЛЬТРАЦИЯ ---")
        status = input("Статус (online/offline/maintenance): ")
        filtered = self._app.filter_by_status(status)
        if filtered:
            for s in filtered:
                print(f"  {s.name} ({s.ip})")
        else:
            print("Серверов с таким статусом нет")
    
    def _sort(self):
        print("\n--- СОРТИРОВКА ---")
        print("1. По имени")
        print("2. По оценке")
        print("3. По подключениям")
        choice = input("Выберите: ")
        
        if choice == "1":
            self._app.sort(lambda s: s.name)
            print("✅ Отсортировано по имени")
        elif choice == "2":
            self._app.sort(lambda s: s.get_score())
            print("✅ Отсортировано по оценке")
        elif choice == "3":
            self._app.sort(lambda s: s.connections)
            print("✅ Отсортировано по подключениям")
        else:
            print("Неверный выбор")
            return
        self._show_all()
    
    def _remove(self):
        print("\n--- УДАЛЕНИЕ ---")
        ip = input("IP сервера: ")
        s = self._app.find_by_ip(ip)
        if not s:
            print("Сервер не найден")
            return
        
        print(f"Сервер: {s.name} ({s.ip})")
        confirm = input("Удалить? (y/n): ")
        if confirm.lower() == "y":
            try:
                self._app.remove(ip)
                print("✅ Удалён")
            except NotFoundError as e:
                print(f"❌ {e}")
        else:
            print("Отменено")