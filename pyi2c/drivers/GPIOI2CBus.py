from abc import ABC, abstractmethod


class GPIOI2CBus(ABC):
    @abstractmethod
    def write(self, sda: int, scl: int) -> None:
        pass

    @abstractmethod
    def read(self) -> int:
        pass
