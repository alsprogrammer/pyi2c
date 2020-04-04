from pyi2c.protocol import I2CProtocol


class I2CCircuitPython:
    def __init__(self, protocol: I2CProtocol):
        self._protocol = protocol

    def deinit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def scan(self):
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        pass

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        pass

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *, out_start=0, out_end=None, in_start=0,
                              in_end=None, stop=False):
        pass
