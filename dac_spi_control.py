import time
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiPort
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

def read_chip_id(spi_port):
    chip_id_low_address = 0x04
    chip_id_high_address = 0x05

    chip_id_low = read_register(spi_port, chip_id_low_address)[0]
    chip_id_high = read_register(spi_port, chip_id_high_address)[0]

    chip_id = (chip_id_high << 8) | chip_id_low
    return chip_id

def set_dac_range(spi_port, range_value):
    dac_range_register = 0x1E

    if range_value == 5:
        dac_range_value = 0X77
    elif range_value == 10:
        dac_range_value = 0X66
    else:
        return

    write_register(spi_port, dac_range_register, dac_range_value)

def set_dac_voltage(spi_port, dac_channel, voltage):
    # Assume DAC range is 0 to 5V
    dac_range = 5
    dac_value = int((4095 / dac_range) * voltage)

    high_byte = (dac_value >> 8) & 0xFF
    low_byte = dac_value & 0xFF

    dac_base_address = 0x50 
    dac_low_address = dac_base_address + 2 * dac_channel
    dac_high_address = dac_low_address + 1

    write_register(spi_port, dac_low_address, low_byte)
    write_register(spi_port, dac_high_address, high_byte)
    enable_register_update(spi_port)

def enable_register_update(spi_port):
    register_update_address = 0x0F
    register_update_value = 0x01  

    write_register(spi_port, register_update_address, register_update_value)

if __name__ == '__main__':
    Ftdi.show_devices()
    spi = SpiController()

    spi.configure('ftdi://ftdi:232h:FT8NUKWS/1')
    amc = spi.get_port(cs=0, freq=1E6, mode=0)

    chip_id = read_chip_id(amc)

    set_dac_range(amc, range_value=5)
    set_dac_voltage(amc, dac_channel=0, voltage=2.5)
