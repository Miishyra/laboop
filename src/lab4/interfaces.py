from abc import ABC, abstractmethod

class Startable(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

class Scorable(ABC):
    @abstractmethod
    def get_score(self):
        pass

class Informable(ABC):
    @abstractmethod
    def get_info(self):
        pass