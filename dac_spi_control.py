from pyftdi.spi import SpiController

def set_dac_range(spi_port, range_value):
    dac_range_register = 0x1E

    if range_value == 5:
        dac_range_value = 0X77
    elif range_value == 10:
        dac_range_value = 0X66
    else:
        return

    write_len = 1
    write_buf = [0] * (2 + write_len)
    write_buf[0] = 0x00 | ((dac_range_register & 0x7F00) >> 8)
    write_buf[1] = dac_range_register & 0xFF
    write_buf[2] = dac_range_value
    spi_port.exchange(write_buf, duplex=True)

def set_dac_voltage(spi_port, dac_channel, voltage):
    dac_value = int((4095 / 5) * voltage)

    high_byte = (dac_value >> 8) & 0xFF
    low_byte = dac_value & 0xFF

    dac_base_address = 0x50 
    dac_low_address= dac_base_address + 2 * dac_channel
    dac_high_address= dac_low_address + 1

    write_len = 1
    write_buf_low = [0] * (2 + write_len)
    write_buf_low[0] = 0x00 | ((dac_low_address & 0x7F00) >> 8) 
    write_buf_low[1] = dac_low_address & 0xFF
    write_buf_low[2] = low_byte
    spi_port.exchange(write_buf_low, duplex=True)

    write_buf_high = [0] * (2 + write_len)
    write_buf_high[0] = 0x00 | ((dac_high_address & 0x7F00) >> 8)
    write_buf_high[1] = dac_high_address & 0xFF
    write_buf_high[2] = high_byte
    spi_port.exchange(write_buf_high, duplex=True)

    enable_register_update(spi_port)

def enable_register_update(spi_port):
    register_update_address = 0x0F
    register_update_value = 0x01  

    write_len = 1
    write_buf = [0] * (2 + write_len)
    write_buf[0] = 0x00 | ((register_update_address & 0x7F00) >> 8)
    write_buf[1] = register_update_address & 0xFF
    write_buf[2] = register_update_value
    spi_port.exchange(write_buf, duplex=True)

if __name__ == '__main__':
    spi = SpiController()
    spi.configure('ftdi://ftdi:232h:FT8NUKWS/1')
    amc = spi.get_port(cs=0, freq=1E6, mode=0)

    set_dac_range(amc, range_value=5)
    set_dac_voltage(amc, dac_channel=0, voltage=2.5)
    enable_register_update(amc)
