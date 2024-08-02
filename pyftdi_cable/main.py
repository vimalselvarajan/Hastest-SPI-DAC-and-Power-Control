import time
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController
from pyftdi_cable.spi_communication import SPICommunication
from pyftdi_cable.amc7836 import AMC7836

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
    amc.set_dac_range(-10)
    amc.enable_dac()
    amc.set_voltage_negtagive(-6.5, 0x50)
    amc.set_voltage_negtagive(-6.5, 0x52)
    amc.set_voltage_negtagive(-6.5, 0x54)
    amc.dac_register_update()
    time.sleep(10)
    amc.set_voltage_negtagive(-10, 0x50)
    amc.set_voltage_negtagive(-10, 0x52)
    amc.set_voltage_negtagive(-10, 0x54)
    amc.dac_register_update()

if __name__ == '__main__':
    main()
