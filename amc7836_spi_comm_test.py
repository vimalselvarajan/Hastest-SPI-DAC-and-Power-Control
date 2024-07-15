import time
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController
from pyftdi.spi import SpiPort
from typing import Any, Iterable, Mapping, Optional, Set, Union


def read_register(spi_port: SpiPort, address: int, length: int = 1) -> bytes:
    """Read byte(s) from device register

        :param spi_port: SPI port of the device
        :param address: starting address of the register 
        :param length: number of registers to read 
        :return: bytes read from the device
    """
    send_buf = [0] * (2 + length)
    send_buf[0] = 0x80 | ((address & 0x7F00) >> 8)
    send_buf[1] = address & 0xFF
    response_buf = spi_port.exchange(send_buf,  duplex=True)
    data = response_buf[-length:]
    return data


def write_register(spi_port: SpiPort, address: int,  data: Union[int, bytes, bytearray, Iterable[int]]) -> None:
    """Write byte(s) to device register

        :param spi_port: SPI port of the device
        :param address: starting address of the register 
        :param data: byte(s) to write
    """
    if isinstance(data, int):
        data = [data]
    length = len(data)
    send_buf = [0] * (2 + length)
    send_buf[0] = 0x00 | ((address & 0x7F00) >> 8)
    send_buf[1] = address & 0xFF
    for index, value in enumerate(data):
        send_buf[2 + index] = value & 0xFF
    spi_port.exchange(send_buf, duplex=True)


def test_232h():
    Ftdi.show_devices()

    spi = SpiController()
    spi.configure('ftdi://ftdi:232h:FT8NUKWS/1')
    spi_port = spi.get_port(cs=0, freq=1E6, mode=0)

    # Perform soft reset
    write_register(spi_port, 0x00, 0xB0)
    # Wait for reset to complete
    time.sleep(1)

    # Read interface configuration registers (0x00, 0X01)
    address = 0x00
    data = read_register(spi_port, address, 2)
    for index, value in enumerate(data):
        print('Interface config register: 0x{:02X} Value: 0x{:02X}'.format(address + index, value))

    # Read device configuration register
    address = 0x02
    data = read_register(spi_port, address)
    for index, value in enumerate(data):
        print('Device config register: 0x{:02X} Value: 0x{:02X}'.format(address + index, value))

    # Turn on reference voltage PREF
    write_register(spi_port, 0xB4, 0x02)

    # Set DAC A and B range to 0 to +5VDC
    address = 0x1E 
    write_register(spi_port, address, 0x77)
    # Read DAC A and B range
    data = read_register(spi_port, address)
    for index, value in enumerate(data):
        print('DAC range register: 0x{:02X} Value: 0x{:02X}'.format(address + index, value))

   # Enable DAC A and B
    write_register(spi_port, 0xB2, 0XFF)

    # Set DAC A1 to 2048 (0x0800,~+2.5VDC)
    address = 0x50
    data = [0x00, 0x08]
    write_register(spi_port, address, data)

    # Set DAC Register Update
    write_register(spi_port, 0X0F, 0X01)

    time.sleep(10)

    # Set DAC A1 to 0 (0x0000, 0VDC)
    address = 0x50
    data = [0x00, 0x00]
    write_register(spi_port, address, data)

    # Set DAC Register Update
    write_register(spi_port, 0X0F, 0X01)

    # Disable DAC A, B
    write_register(spi_port, 0xB2, 0x00)

    ssd = 1


def test_2232h():
    # Renesas FT2232 SPI comm does not work with pyftdi
    spi = SpiController()
    spi.configure('ftdi://::/1')

    amc = spi.get_port(cs=0, freq=1E6, mode=0)
    # spi.ftdi.set_latency_timer(8)
    # spi.ftdi.enable_adaptive_clock(False)
    # spi.ftdi.enable_3phase_clock(False)
    # spi.ftdi.set_frequency(1E6)
    # spi.ftdi.purge_buffers()

    w_data = [0x0A]
    read_len = 2

    spi.ftdi.write_data(bytes(w_data))
    dd = spi.ftdi.read_data_bytes(read_len, 10)

    spi.ftdi.purge_buffers()

    # reg_addr = 0x00
    # read_len = 1
    # write_buf = [0] * (2 + read_len)
    # write_buf[0] = 0x80 | ((reg_addr & 0x7F00) >> 8)
    # write_buf[1] = reg_addr & 0xFF
    # read_buf = amc.exchange(write_buf,  duplex=True)
    # out_buf = read_buf[-read_len:]
    # for a in out_buf:
    #     print('0x{:02x}'.format(a))

    # reg_addr = 0x1E
    # write_val = 0X77
    # write_len = 1
    # write_buf = [0] * (2 + write_len)
    # write_buf[0] = 0x00 | ((reg_addr & 0x7F00) >> 8)
    # write_buf[1] = reg_addr & 0xFF
    # write_buf[2] = write_val & 0xFF
    # read_buf = amc.exchange(write_buf, duplex=True)
    #
    # reg_addr = 0x1E
    # read_len = 1
    # write_buf = [0] * (2 + read_len)
    # write_buf[0] = (0x80 | (reg_addr & 0x7F00) >> 8)
    # write_buf[1] = reg_addr & 0xFF
    # read_buf = amc.exchange(write_buf, duplex=True)
    # out_buf = read_buf[-read_len:]
    # for a in out_buf:
    #     print('0x{:02x}'.format(a))

    ssd = 1


if __name__ == '__main__':
    test_232h()
    # test_2232h()