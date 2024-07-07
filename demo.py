from pyftdi.spi import SpiController

def test():

    spi = SpiController()
    spi.configure('ftdi://::/1')
    slave = spi.get_port(cs=0, freq=10E6, mode=0)
    write_buf = b'Hello'
    read_buf = slave.exchange(write_buf, duplex=True)

    foo = 1

if __name__ == '__main__':

    test()