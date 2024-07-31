import time
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiPort
from typing import Any, Iterable, Union

class SPICommunication:
    def __init__(self, spi_port: SpiPort):
        self.spi_port = spi_port

    def read_register(self, address: int, length: int = 1) -> bytes:
        """
        Read byte(s) from device register.

        Parameters:
            address (int): Starting address of the register.
            length (int): Number of registers to read. Defaults to 1.

        Returns:
            bytes: Bytes read from the device.
        """
        send_buf = bytearray(2 + length)
        send_buf[0] = 0x80 | ((address & 0x7F00) >> 8)
        send_buf[1] = address & 0xFF
        response_buf = self.spi_port.exchange(send_buf, duplex=True)
        return response_buf[-length:]

    def write_register(self, address: int, data: Union[int, bytes, bytearray, Iterable[int]]) -> None:
        """
        Write byte(s) to device register.

        Args:
            address (int): Starting address of the register.
            data (Union[int, bytes, bytearray, Iterable[int]]): Byte(s) to write.

        Raises:
            ValueError: If data is not a valid type or empty.
        """
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


class AMC7836:
    def __init__(self, spi_communication: SPICommunication):
        self.spi_communication = spi_communication

    def soft_reset(self):
        self.spi_communication.write_register(0x00, 0xB0)
        print("Soft reset complete.")

    def read_interface_config_registers(self):
        address = 0x00
        length = 2
        data = self.spi_communication.read_register(address, length)
        expected_values = [0x30, 0x00]
        for index, value in enumerate(data):
            if value == expected_values[index]:
                print(f"Interface config register: 0x{address + index:02X} Value: 0x{value:02X}")
            else:
                print(f"Value at address 0x{address + index:02X} is incorrect: 0x{value:02X}, expected: 0x{expected_values[index]:02X}")
                return

    def read_device_config_register(self):
        address = 0x02
        data = self.spi_communication.read_register(address)
        expected_value = 0x03
        for index, value in enumerate(data):
            if value == expected_value:
                print(f"Device config register: 0x{address + index:02X} Value: 0x{value:02X}")
            else:
                print(f"Value at address 0x{address + index:02X} is incorrect: 0x{value:02X}, expected: 0x{expected_value:02X}")
                return

    def turn_on_reference_voltage(self):
        self.spi_communication.write_register(0xB4, 0x02)

    def set_dac_range(self, range_value: int):
        dac_range_register = 0x1E
        if range_value == 5:
            dac_range_value = 0x77
        elif range_value == 10:
            dac_range_value = 0x66
        else:
            print(f"Unsupported range value: {range_value}")
            return
        self.spi_communication.write_register(dac_range_register, dac_range_value)

    def enable_dac(self):
        self.spi_communication.write_register(0xB2, 0XFF)

    def set_voltage(self, voltage: float):
        equation = (voltage * 4095) / 5
        digital_value = int(equation) << 4
        high_byte = (digital_value >> 8) & 0xFF
        low_byte = digital_value & 0xFF
        data = [high_byte, low_byte]
        self.spi_communication.write_register(0x50, data)

    def dac_register_update(self):
        self.spi_communication.write_register(0X0F, 0X01)
        time.sleep(10)

    def disable_dac(self):
        self.spi_communication.write_register(0xB2, 0x00)


def main():
    Ftdi.show_devices()
    spi = SpiController()
    spi.configure('ftdi://ftdi:232h:FT8NUKWS/1')
    amc_spi_port = spi.get_port(cs=0, freq=1E6, mode=0)

    spi_communication = SPICommunication(amc_spi_port)
    amc = AMC7836(spi_communication)

    amc.soft_reset()
    time.sleep(1)
    amc.read_interface_config_registers()
    amc.read_device_config_register()
    amc.turn_on_reference_voltage()
    amc.set_dac_range(5)
    amc.enable_dac()
    amc.set_voltage(5)
    amc.dac_register_update()
    time.sleep(10)
    amc.set_voltage(0)
    amc.dac_register_update()

if __name__ == '__main__':
    main()
