"""
Base Agent module to define common functionalities for all agents.
"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def run(self):
        pass
