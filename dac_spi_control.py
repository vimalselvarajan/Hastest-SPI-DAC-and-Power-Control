import time
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiPort
from typing import Any, Iterable, Mapping, Optional, Set, Union

def read_register(spi_port: SpiPort, address: int, length: int = 1) -> bytes:
    """
    Read byte(s) from device register.

    Parameters:
        spi_port (SpiPort): SPI port of the device.
        address (int): Starting address of the register.
        length (int): Number of registers to read. Defaults to 1.

    Returns:
        bytes: Bytes read from the device.

    """
    # Initialize send_buf as a bytearray with the required size
    send_buf = bytearray(2 + length)  # Pre-fill with zeros is default for bytearray

    # Set the command byte and address
    send_buf[0] = 0x80 | ((address & 0x7F00) >> 8)  # Command byte with read flag
    send_buf[1] = address & 0xFF  # Lower 8 bits of the address

    # Exchange data with the device
    response_buf = spi_port.exchange(send_buf, duplex=True)

    # Extract the relevant portion from the response
    data = response_buf[-length:]

    return data

def write_register(spi_port: SpiPort, address: int, data: Union[int, bytes, bytearray, Iterable[int]]) -> None:
    """
    Write byte(s) to device register.

    Args:
        spi_port (SpiPort): SPI port of the device.
        address (int): Starting address of the register.
        data (Union[int, bytes, bytearray, Iterable[int]]): Byte(s) to write.

    Raises:
        ValueError: If data is not a valid type or empty.
    """
    # Normalize data into a list of bytes
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

    # Calculate the total size needed for send_buf: 2 bytes for address + length of data
    send_buf = bytearray(2 + len(data))

    # Set the command byte and address in send_buf
    send_buf[0] = 0x00 | ((address & 0x7F00) >> 8)  # Command byte with the most significant bits of address
    send_buf[1] = address & 0xFF  # Least significant bits of address

    # Set the data, ensuring each value fits into one byte
    for index, val in enumerate(data):
        send_buf[2 + index] = val & 0xFF  # Start from position 2

    # Send the data to the device
    spi_port.exchange(send_buf, duplex=True)

def soft_reset(spi_port: SpiPort):
    write_register(spi_port, 0x00, 0xB0) 
    time.sleep(1)

    print("Soft reset complete.")

def read_interface_config_registers(spi_port: SpiPort):
    address = 0x00
    length = 2
    data = read_register(spi_port, address, length)
    
    # Verify the values
    expected_values = [0x30, 0x00]
    for index, value in enumerate(data):
        if value == expected_values[index]:
            print(f"Interface config register: 0x{address + index:02X} Value: 0x{value:02X}")
        else:
            print(f"Value at address 0x{address + index:02X} is incorrect: 0x{value:02X}, expected: 0x{expected_values[index]:02X}")
            return

def read_device_config_register(spi_port: SpiPort):
    address = 0x02
    data = read_register(spi_port, address)

    # Verify the value
    expected_value = 0x03
    for index, value in enumerate(data):
        if value == expected_value:
            print(f"Device config register: 0x{address + index:02X} Value: 0x{value:02X}")
        else:
            print(f"Value at address 0x{address + index:02X} is incorrect: 0x{value:02X}, expected: 0x{expected_value:02X}")
            return

def turn_on_reference_voltage(spi_port: SpiPort):
    write_register(spi_port, 0xB4, 0x02)

def set_dac_range(spi_port: SpiPort, range_value: int):
    dac_range_register = 0x1E

    if range_value == 5:
        dac_range_value = 0x77
    elif range_value == 10:
        dac_range_value = 0x66
    else:
        print(f"Unsupported range value: {range_value}")
        return

    write_register(spi_port, dac_range_register, dac_range_value)

def main():
    Ftdi.show_devices()
    spi = SpiController()
    spi.configure('ftdi://ftdi:232h:FT8NUKWS/1')
    amc = spi.get_port(cs=0, freq=1E6, mode=0)

    # Perform soft reset
    soft_reset(amc)

    # Read and print interface configuration registers (0x00, 0x01) from the device.
    read_interface_config_registers(amc)

    # Read and print device configuration register (0x02) from the device.
    read_device_config_register(amc)

    #Turn on the reference voltage PREF by writing to the appropriate register.
    turn_on_reference_voltage(amc)

    #Wait 10sec
    time.sleep(10)

    # Set DAC range
    set_dac_range(amc, 5)

    
if __name__ == '__main__':
    main()
