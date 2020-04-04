import digitalio
from pyi2c.drivers.GPIOI2CBus import GPIOI2CBus
from adafruit_mcp230xx.mcp23017 import MCP23017


class MCP23017I2C(GPIOI2CBus):
    def __init__(self, mcp: MCP23017, sda_pin_num: int, scl_pin_num: int):
        assert mcp is not None, "You have to provide MCP23017"
        assert 0 <= sda_pin_num <= 15, "The sda pin number must be between 0 and 15"
        assert 0 <= scl_pin_num <= 15, "The scl pin number must be between 0 and 15"

        self._mcp = mcp
        self._sda_pin = self._mcp.get_pin(sda_pin_num)
        self._scl_pin = self._mcp.get_pin(scl_pin_num)

    def write(self, sda: int, scl: int) -> None:
        if sda:
            self._pin_high(self._sda_pin)
        else:
            self._pin_low(self._sda_pin)

        if scl:
            self._pin_high(self._scl_pin)
        else:
            self._pin_low(self._scl_pin)

    def read(self) -> int:
        self._pin_high(self._sda_pin)
        return self._sda_pin.value

    @staticmethod
    def _pin_low(pin):
        pin.direction = digitalio.Direction.OUTPUT
        pin.value = False

    @staticmethod
    def _pin_high(pin):
        pin.pull = digitalio.Pull.UP
        pin.direction = digitalio.Direction.INPUT
