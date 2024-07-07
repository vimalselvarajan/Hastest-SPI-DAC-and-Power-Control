from pyftdi.spi import SpiController


def test_232h():
    spi = SpiController()
    spi.configure('ftdi://ftdi:232h:FT8NUKWS/1')

    amc = spi.get_port(cs=0, freq=1E6, mode=0)

    # reg_addr = 0x00
    # read_len = 3
    # write_buf = [0] * (2 + read_len)
    # write_buf[0] = 0x80 | ((reg_addr & 0x7F00) >> 8)
    # write_buf[1] = reg_addr & 0xFF
    # read_buf = amc.exchange(write_buf,  duplex=True)
    # out_buf = read_buf[-read_len:]
    # for a in out_buf:
    #     print('0x{:02x}'.format(a))

    reg_addr = 0x1E
    write_val = 0X77
    write_len = 1
    write_buf = [0] * (2 + write_len)
    write_buf[0] = 0x00 | ((reg_addr & 0x7F00) >> 8)
    write_buf[1] = reg_addr & 0xFF
    write_buf[2] = write_val & 0xFF
    read_buf = amc.exchange(write_buf, duplex=True)

    reg_addr = 0x1E
    read_len = 1
    write_buf = [0] * (2 + read_len)
    write_buf[0] = (0x80 | (reg_addr & 0x7F00) >> 8)
    write_buf[1] = reg_addr & 0xFF
    read_buf = amc.exchange(write_buf, duplex=True)
    out_buf = read_buf[-read_len:]
    for a in out_buf:
        print('0x{:02x}'.format(a))

    ssd = 1


def test_2232h():
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

    w_data = [128, 0, 11, 128, 0, 11, 128, 0, 11,
              49, 3, 0,
              128, 0, 0,
              128, 0, 11, 128, 0, 11, 128, 0, 11, 128, 0, 11, 128, 0, 11,
              128, 8, 11,
              135]

    # w_data = [128, 0, 11, 135]
    read_len = 3
    kk = spi.ftdi.write_data(bytes(w_data))
    dd = spi.ftdi.read_data_bytes(read_len, 10)

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
    #test_232h()
    test_2232h()