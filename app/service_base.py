"""Service Abstract Base Class"""

from abc import ABC, abstractmethod


class ServiceBase(ABC):
    """ABC for Service base class"""

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
