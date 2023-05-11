from abc import ABC, abstractmethod

# Pattern interface
class RouteInterface(ABC):
    router = None
    session = None
    
    @abstractmethod
    def setup_routes(self):
        pass