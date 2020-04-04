from pyi2c.drivers import GPIOI2CBus


class I2CProtocol:
    def __init__(self, bus: GPIOI2CBus):
        self.bus = bus
        self._error_happened = False
        self.error_message = None

    def error(self, message: str):
        self._error_happened = True
        self.error_message = message

    def error_reset(self):
        self._error_happened = False
        self.error_message = None

    def start(self):
        self.bus.write(sda=1, scl=1)
        self.bus.write(sda=0, scl=1)
        self.bus.write(sda=0, scl=0)

    def send(self, value: int) -> None:
        x = 0x80
        while x:
            sending_bit = ((x & value) and 1)
            self.bus.write(sda=sending_bit, scl=0)
            self.bus.write(sda=sending_bit, scl=1)
            self.bus.write(sda=sending_bit, scl=0)
            x = x >> 1

    def read(self) -> int:
        x = 0x80
        value = 0
        while x:
            self.bus.write(sda=1, scl=1)
            if self.bus.read():
                value += x
            self.bus.write(sda=1, scl=0)
            x = x >> 1
        return value

    def ack(self, error: str = None) -> int:
        self.bus.write(sda=1, scl=0)
        self.bus.write(sda=1, scl=1)
        sda = self.bus.read()
        self.bus.write(sda=1, scl=0)

        if sda and error:
            self.error("I2C NACK: %s" % error)
        else:
            self.error_reset()  # cancel any previous error
        return not sda

    def send_ack(self):
        self.bus.write(sda=0, scl=0)
        self.bus.write(sda=0, scl=1)
        self.bus.write(sda=0, scl=0)

    def send_nack(self):
        self.bus.write(sda=1, scl=0)
        self.bus.write(sda=1, scl=1)
        self.bus.write(sda=1, scl=0)
        self.bus.write(sda=0, scl=0)

    def stop(self):
        self.bus.write(sda=0, scl=0)
        self.bus.write(sda=0, scl=1)
        self.bus.write(sda=1, scl=1)