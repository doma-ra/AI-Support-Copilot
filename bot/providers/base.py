from abc import ABC, abstractmethod
from typing import Dict

class AbstractProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, profile: str) -> Dict:
        """Gibt ein schema-valides Dict für BotResponse zurück."""
        raise NotImplementedError
