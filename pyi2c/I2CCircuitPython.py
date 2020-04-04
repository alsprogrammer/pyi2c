from pyi2c.protocol import I2CProtocol

I2C_REGISTER_WRITE = 0
I2C_REGISTER_READ = 1


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
        end = end if end else len(buffer)

        self._protocol.start()
        self._protocol.send((address & 0x7F) << 1 | I2C_REGISTER_READ)
        self._protocol.ack()
        for index in range(start, end - 2):
            buffer[index] = self._protocol.read()
            self._protocol.send_ack()
        buffer[end - 1] = self._protocol.read()
        self._protocol.send_nack()

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        if isinstance(buffer, str):
            buffer = bytes([ord(x) for x in buffer])

        end = end if end else len(buffer)
        
        self._protocol.start()
        self._protocol.send((address & 0x7F) << 1 | I2C_REGISTER_WRITE)
        self._protocol.ack()
        for value in buffer[start:end]:
            self._protocol.send(value)
            self._protocol.ack()
        if stop:
            self._protocol.stop()

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *, out_start=0, out_end=None,
                              in_start=0, in_end=None, stop=False):
        self.writeto(address, buffer_out, start=out_start, end=out_end,stop=False)
        self.readfrom_into(address, buffer_in, start=in_start, end=in_end)
