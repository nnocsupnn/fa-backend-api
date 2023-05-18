from abc import ABC, abstractmethod

# Pattern interface
class RouteInterface(ABC):
    router = None
    session = None
    service = None
    
    @abstractmethod
    def setup_routes(self):
        pass
    
    def default_error_response(self, message, statusCode: int = 500):
        return {
            "status": statusCode,
            "message": message
        }