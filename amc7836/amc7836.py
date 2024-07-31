import time
from .spi_communication import SPICommunication

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
