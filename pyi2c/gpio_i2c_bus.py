from abc import ABC, abstractmethod


class GPIOPin(ABC):
    @abstractmethod
    def pull_up(self) -> None:
        pass

    @abstractmethod
    def set_low(self) -> None:
        pass

    @abstractmethod
    def read(self) -> bool:
        pass


class GPIOI2CBus:
    def __init__(self, sda_pin: GPIOPin, scl_pin: GPIOPin):
        assert isinstance(sda_pin, GPIOPin), "The sda pin has to be an IOPin"
        assert isinstance(scl_pin, GPIOPin), "The sda pin has to be an IOPin"

        self._sda_pin = sda_pin
        self._scl_pin = scl_pin

    def write(self, sda: int, scl: int) -> None:
        if sda:
            self._sda_pin.pull_up()
        else:
            self._sda_pin.set_low()

        if scl:
            self._scl_pin.pull_up()
        else:
            self._scl_pin.set_low()

    def read(self) -> int:
        self._sda_pin.pull_up()
        return self._sda_pin.read()

    def wait_for_scl(self) -> None:
        while not self._scl_pin.read():
            pass
