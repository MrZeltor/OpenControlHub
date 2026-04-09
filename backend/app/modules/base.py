from abc import ABC, abstractmethod

class BaseModule(ABC):
    """
    Abstract Base Class for all OpenControlHub modules.
    All modules should inherit from this and implement handle_command.
    """
    @abstractmethod
    def handle_command(self, action: str, data: any):
        pass
