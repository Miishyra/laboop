from typing import TypeVar, Generic, Callable, Optional, List
from typing import Protocol

# ===== ПРОТОКОЛЫ =====

class Displayable(Protocol):
    def display(self) -> str:
        ...

class Scorable(Protocol):
    def get_score(self) -> int:
        ...

# ===== TYPEVAR =====

T = TypeVar('T')
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
R = TypeVar('R')

# ===== TYPED COLLECTION =====

class TypedCollection(Generic[T]):
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        self._items.remove(item)
    
    def remove_at(self, index: int) -> T:
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items.pop(index)
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def get_by_index(self, index: int) -> T:
        return self._items[index]
    
    def find_by_name(self, name: str) -> List[T]:
        result: List[T] = []
        for s in self._items:
            if hasattr(s, 'name') and s.name == name:
                result.append(s)
        return result
    
    def find_by_ip(self, ip: str) -> Optional[T]:
        for s in self._items:
            if hasattr(s, 'ip') and s.ip == ip:
                return s
        return None
    
    def find_by_status(self, status: str) -> List[T]:
        result: List[T] = []
        for s in self._items:
            if hasattr(s, 'status') and s.status == status:
                result.append(s)
        return result
    
    def sort_by_name(self) -> None:
        self._items.sort(key=lambda s: s.name)
    
    def sort_by_connections(self) -> None:
        self._items.sort(key=lambda s: s.connections)
    
    def get_online(self) -> 'TypedCollection[T]':
        new_collection: TypedCollection[T] = TypedCollection()
        for s in self._items:
            if hasattr(s, 'status') and s.status == 'online':
                new_collection.add(s)
        return new_collection
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    
    def __str__(self) -> str:
        if not self._items:
            return "Коллекция пуста"
        text: str = f"Коллекция ({len(self._items)} шт.):\n"
        for i, s in enumerate(self._items):
            text += f"  [{i}] {s}\n"
        return text


# ===== ОГРАНИЧЕННЫЕ КОЛЛЕКЦИИ =====

class DisplayableCollection(TypedCollection[D]):
    pass

class ScorableCollection(TypedCollection[S]):
    pass