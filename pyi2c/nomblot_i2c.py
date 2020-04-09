"""Main module."""
# ! /usr/bin/env python
#
# python I2C
#
# (C)2020 Aleksandr Saiapin <alstutor@gmail.com>
# (C)2006 Patrick Nomblot <pyI2C@nomblot.org>
# this is distributed under a free software license, see license.txt

import time
from typing import List

from pyi2c.protocol import I2CProtocol

I2C_REGISTER_WRITE = 0
I2C_REGISTER_READ = 1


class ProtocolError:
    pass


class I2CBus:
    def __init__(self, protocol: I2CProtocol):
        self._bus = protocol
        self.protocolError = False

    def scan(self, i2c_start_address: int) -> List[int]:
        addresses = []
        for address in range(i2c_start_address, i2c_start_address + 0x10, 2):
            self._bus.start()
            self._bus.send(address)
            if self._bus.ack():
                addresses.append(address)
            self._bus.read()
            self._bus.send_nack()
            self._bus.stop()
            if not addresses:
                self.error("no I2C component found !")

        return addresses

    @staticmethod
    def error(error_message: str = None) -> None:
        print(error_message)
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
