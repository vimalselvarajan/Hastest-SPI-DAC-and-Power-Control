import math
import time
from typing import Union

from instrument_lib.dac.amc7836 import Amc7836
from instrument_lib.dac.amc7836_init import Amc7836Init
from instrument_lib.daq.keysight_daq970a import KeysightDaq970a


class F84010Test:
    """F84010 Test."""

    def __init__(self):
        self._amc7836: Union[None, Amc7836] = None
        self._daq970a: Union[None, KeysightDaq970a] = None
        self._delay_sec = 5
        self._daq_current_vdd2_channel = 111
        self._daq_current_vdd3_c_channel = 112

    def adjust_gate_voltage(self, dac_address_key: str, dac_init_value: int, daq_ch: int, target: float) -> None:
        """Adjust gate voltage to attain desired target drain current."""

        dac_step = [64, 32, 16, 8, 4, 2]
        dac_value = [dac_init_value & 0xFF, dac_init_value >> 8]
        self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES[dac_address_key], dac_value)
        time.sleep(0.1)
        drain_current = self._daq970a.measure_voltage(daq_ch)
        print(f'Drain current: {drain_current:.5f}')
        dac_curr_value = dac_init_value
        for index, val in enumerate(dac_step):
            dac_new_value = dac_curr_value + int(math.copysign(val, target - drain_current))
            # Limit DAC voltage to less than -2.5V (3072)
            if dac_new_value < 3072:
                dac_value = [dac_new_value & 0xFF, dac_new_value >> 8]
                self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES[dac_address_key], dac_value)
                time.sleep(0.1)
                drain_current = self._daq970a.measure_voltage(daq_ch)
                print(f'Iteration: {index} Drain current: {drain_current:.5f}')
            dac_curr_value = dac_init_value

    def configure_amc7836(self) -> None:
        """Create Amc7836 object and configures the DAC channels."""

        self._amc7836 = Amc7836Init.init()
        interface_cfg = self._amc7836.read_register(self._amc7836.REGISTER_ADDRESSES['ITFC_CFG0'], 2)
        print(f'Interface Configuration 0 0x{interface_cfg[0]:02X}')
        print(f'Interface Configuration 1 0x{interface_cfg[1]:02X}')

        # enable PREF for DAC operation
        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['ADC_PD2'], 0x02)

        # set DAC range for -10 ~ 0V
        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['DAC_RNG0'], [0x44, 0x44])
        # enable DAC A,B,C,D
        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['DAC_PD0'], [0xFF, 0xFF])
        # check DAC A,B,C,D
        dac_range = self._amc7836.read_register(self._amc7836.REGISTER_ADDRESSES['DAC_RNG0'], 2)
        print(f'DAC Range A 0b{(dac_range[0] & 7):03b}')
        print(f'DAC Range B 0b{((dac_range[0] >> 4) & 7):03b}')
        print(f'DAC Range C 0b{(dac_range[1] & 7):03b}')
        print(f'DAC Range D 0b{((dac_range[1] >> 4) & 7):03b}')

    def configure_daq970a(self) -> None:
        """Create KeysightDaq970a object, clear the status register and reset."""

        self._daq970a = KeysightDaq970a('USB0::0x2A8D::0x5101::MY58016887::INSTR')
        idn = self._daq970a.get_id()
        print(f'DAQ ID:{idn}')
        self._daq970a.clear()
        self._daq970a.reset()

    def cleanup(self) -> None:
        """Close instrument sessions."""

        self._daq970a.close()

    def power_down_sequence(self) -> None:
        """Power down sequence of amplifiers."""

        input('Turn off VDD2, VDD3_C, VDD3_P +50V Drain Voltage')
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        input('Turn off AMC7836 Voltage')
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        input('Turn off VDD1 +5V Pre Driver Drain Voltage')
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

    def power_up_sequence(self) -> None:
        """Power up sequence of amplifiers."""

        input('Turn on VDD1 +5V Pre Driver Drain Voltage')
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        print('Turning on VGG2, VGG3_C, VGG3_P -6.5V Gate Voltages')
        # Set DAC A1, A2, A3 to -6.5V (1433 = 0x599)
        dac_value = [0x99, 0x05, 0x99, 0x05, 0x99, 0x05]
        self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES['DACA0_DATA_LO'], dac_value)
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        input('Turn on VDD2, VDD3_C, VDD3_P +50V Drain Voltage')
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

    def set_dac_voltage(self, address: int, value: list[int]) -> None:
        """Set DAC voltage."""

        self._amc7836.write_register(address, value)
        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['REG_UPDATE'], 0x01)


def main():
    test = F84010Test()
    print(f'Configuring DAQ970A...')
    test.configure_daq970a()

    input('Turn on AMC7836 Voltage')
    print(f'Configuring AMC7836...')
    test.configure_amc7836()

    print(f'Powering up F84010...')
    test.power_up_sequence()

    # TODO: Read drain current VDD2, VDD3_C and print to file 

    print(f'Powering down F84010...')
    test.power_down_sequence()

    test.cleanup()


if __name__ == '__main__':
    main()
