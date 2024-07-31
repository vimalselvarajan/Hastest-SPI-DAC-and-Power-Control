import time
from pyftdi.spi import SpiPort
from typing import Iterable, Union

class SPICommunication:
    def __init__(self, spi_port: SpiPort):
        self.spi_port = spi_port

    def read_register(self, address: int, length: int = 1) -> bytes:
        send_buf = bytearray(2 + length)
        send_buf[0] = 0x80 | ((address & 0x7F00) >> 8)
        send_buf[1] = address & 0xFF
        response_buf = self.spi_port.exchange(send_buf, duplex=True)
        return response_buf[-length:]

    def write_register(self, address: int, data: Union[int, bytes, bytearray, Iterable[int]]) -> None:
        if isinstance(data, int):
            data = [data]
        elif isinstance(data, (bytes, bytearray)):
            data = list(data)
        elif isinstance(data, Iterable):
            data = list(data)
        else:
            raise ValueError("Unsupported data type for SPI write operation.")
        
        if not data:
            raise ValueError("Data to write must not be empty.")

        send_buf = bytearray(2 + len(data))
        send_buf[0] = 0x00 | ((address & 0x7F00) >> 8)
        send_buf[1] = address & 0xFF
        for index, val in enumerate(data):
            send_buf[2 + index] = val & 0xFF
        self.spi_port.exchange(send_buf, duplex=True)
