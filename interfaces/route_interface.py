from abc import ABC, abstractmethod

# Pattern interface
class RouteInterface(ABC):
    router = None
    session = None
    service = None
    
    @abstractmethod
    def setup_routes(self):
        pass
    
    def default_error_response(self, message):
        return {
            "status": 500,
            "message": message
        }