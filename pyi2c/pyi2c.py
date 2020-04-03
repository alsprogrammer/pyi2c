"""Main module."""
# ! /usr/bin/env python
#
# python I2C
#
# (C)2020 Aleksandr Saiapin <alstutor@gmail.com>
# (C)2006 Patrick Nomblot <pyI2C@nomblot.org>
# this is distributed under a free software license, see license.txt

import time

from pyi2c.drivers import GPIOI2CBus

I2C_REGISTER_WRITE = 0
I2C_REGISTER_READ = 1


class ProtocolError:
    pass


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


class I2CBus:
    def __init__(self, protocol: I2CProtocol):
        self._bus = protocol
        self.protocolError = False

    def scan(self, i2c_start_address):
        address_ok = None
        for address in range(i2c_start_address, i2c_start_address + 0x10, 2):
            self._bus.start()
            self._bus.send(address)
            if self._bus.ack():
                address_ok = address
            self._bus.read()
            self._bus.send_nack()
            self._bus.stop()
            if address_ok:
                return address_ok
        self.error("no I2C component found !")

    def error(self, error=None):
        raise ProtocolError

    def write_register(self, address, register, value, err="I2C target register access denied !"):
        self._bus.start()
        self._bus.send(address | I2C_REGISTER_WRITE)
        self._bus.ack(err)
        self._bus.send(register)
        self._bus.ack(err)
        self._bus.send(value)
        self._bus.ack(err)
        self._bus.send(0)
        self._bus.ack(err)
        self._bus.stop()

    def read_register(self, address, register, err="cannot _read I2C target register !"):
        self._bus.start()
        self._bus.send(address | I2C_REGISTER_WRITE)
        self._bus.ack(err)
        self._bus.send(register)
        self._bus.ack(err)
        self._bus.stop()
        time.sleep(0.1)
        self._bus.start()
        self._bus.send(address | I2C_REGISTER_READ)
        self._bus.ack(err)
        data = self._bus.read()
        self._bus.send_nack()
        self._bus.stop()
        return data

    def read_register_word(self, address, register, err="cannot _read I2C target register !"):
        self._bus.start()
        self._bus.send(address | I2C_REGISTER_WRITE)
        self._bus.ack(err)
        self._bus.send(register)
        self._bus.ack(err)
        self._bus.stop()
        time.sleep(0.1)
        self._bus.start()
        self._bus.send(address | I2C_REGISTER_READ)
        self._bus.ack(err)
        data1 = self._bus.read()
        self._send_ack()
        data2 = self._bus.read()
        self._bus.send_nack()
        self._bus.stop()
        return data1, data2
