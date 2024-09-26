from abc import ABC, abstractmethod


class Script(ABC):
    @abstractmethod
    async def run(self) -> None:
        pass
