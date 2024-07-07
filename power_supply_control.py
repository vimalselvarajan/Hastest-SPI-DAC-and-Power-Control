import time

from pyvisa import ResourceManager
from pyvisa.resources import USBInstrument


def main():
    rm = ResourceManager()
    print(f'Resources: {rm.list_resources()}')
    ps = USBInstrument(rm, 'USB0::0x0957::0x0807::US27C3730L::INSTR')
    ps.open()
    print(f'Power Supply ID:{ps.query("*IDN?").strip()}')
    print(f'Output State:{ps.query("OUTP:STAT?")}')

    print('Setting output on')
    ps.write("OUTP ON")
    print('Setting voltage')
    ps.write("VOLT 1.2")
    time.sleep(2)
    print(f'Output voltage setting:{ps.query("VOLT?").strip()}')
    print(f'Measured voltage:{ps.query("MEAS:VOLT?").strip()}')

    print(f'Output current setting:{ps.query("CURR?").strip()}')
    print(f'Measured current:{ps.query("MEAS:CURR?").strip()}')
    #time.sleep(10)

    print('Setting output off')
    ps.write("OUTP OFF")
    ps.close()


if __name__ == '__main__':
    main()
