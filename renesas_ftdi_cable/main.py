import math
import csv
import time
from datetime import datetime, timedelta
from typing import Union

from instrument_lib.dac.amc7836 import Amc7836
from instrument_lib.dac.amc7836_init import Amc7836Init
from instrument_lib.daq.keysight_daq970a import KeysightDaq970a
from instrument_lib.power_supply.keysight_e36234a import KeysightE36234a
from instrument_lib.power_supply.keysight_e36312a import KeysightE36312a
from instrument_lib.power_supply.keysight_n5748a import KeysightN5748a

'''
TODO: Get the device ID fro KeysightE36234a and KeysightE36312a
'''

class DeviceUnderTest:

    def __init__(self):
        self._amc7836: Union[None, Amc7836] = None
        self._daq970a: Union[None, KeysightDaq970a] = None
        self._keysight_e36234a: Union[None, KeysightE36234a] = None 
        self._keysight_e36312a: Union[None, KeysightE36312a] = None 
        self._keysight_n5748a: Union[None, KeysightN5748a] = None 
        self._delay_sec = 5
        self._daq_current_vdd2_channel = 111
        self._daq_current_vdd3_c_channel = 112
    
    def power_up_keysight_e36234a(self) -> None:
        self._keysight_e36234a = KeysightE36234a('Todo')

        self._keysight_e36234a.set_output_voltage('1,2', 60)
        # Channel 1 and 2: 6V

        self._keysight_e36234a.set_output_current('1,2', 10)
        # Set the output current for channels 1 and 2 to 10A

        self._keysight_e36234a.enable_output('1,2', True)
        # Enable output

    def power_up_keysight_e36312a(self) -> None:
        self._keysight_e36312a = KeysightE36312a('Todo')

        self._keysight_e36312a.set_output_voltage(1, 5)
        self._keysight_e36234a.set_output_current(2, 5)
        # Channel 1: 6V, 5A

        self._keysight_e36312a.set_output_voltage(2, 25)
        self._keysight_e36234a.set_output_current(2, 1)
        # Channel 2: 25V, 1A

        self._keysight_e36312a.set_output_voltage(3, 25)
        self._keysight_e36234a.set_output_current(3, 1)
        # Channel 3: 25V, 1A

        self._keysight_e36234a.enable_output('1,2,3', True)
        # Enable output
    
    def power_up_keysight_n5748a(self) -> None:
        self._keysight_n5748a = KeysightN5748a('USB0::0x0957::0x0807::US27C3730L')

        self._keysight_n5748a.set_output_voltage(1, 80)
        self._keysight_n5748a.set_output_current(2, 9.5)
        # Channel 1: 80V, 9.5A

        self._keysight_e36234a.enable_output(1, True)
        # Enable output

    
    def configure_amc7836(self) -> None:
        self._amc7836 = Amc7836Init.init()
        # Initialize Amc7836 assuming it is plugged in with USB

        interface_configuration = self._amc7836.read_register(self._amc7836.REGISTER_ADDRESSES['ITFC_CFG0'], 2)
        # Software reset

        expected_values = [0x30, 0x00]
        for index, value in enumerate(interface_configuration):
            if value == expected_values[index]:
                print(f"Interface config register {index} Value: 0x{value:02X}")
            else:
                print(f"Value at address 0x{index} is incorrect: 0x{value:02X}, expected: 0x{expected_values[index]:02X}")
                return
        # Checks if the returned values are the same as the expected values
        
        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['ADC_PD2'], 0x02)
         # Enable PREF for DAC operation

        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['DAC_RNG0'], [0x44, 0x44])
        # set DAC range for -10 ~ 0V

        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['DAC_PD0'], [0xFF, 0xFF])
        # enable DAC A,B,C,D

        dac_range = self._amc7836.read_register(self._amc7836.REGISTER_ADDRESSES['DAC_RNG0'], 2)
        # check DAC A,B,C,D

        print(f'DAC Range A 0b{(dac_range[0] & 7)}')
        print(f'DAC Range B 0b{((dac_range[0] >> 4) & 7)}')
        print(f'DAC Range C 0b{(dac_range[1] & 7)}')
        print(f'DAC Range D 0b{((dac_range[1] >> 4) & 7)}')
        # print the DAC Range

    def configure_daq970a(self) -> None:
        self._daq970a = KeysightDaq970a('USB0::0x2A8D::0x5101::MY58016887::INSTR')

        idn = self._daq970a.get_id()
        print(f'DAQ ID:{idn}')

        self._daq970a.clear()
        self._daq970a.reset()

        time.sleep(1)
    
    def power_up_sequence(self) -> None:
        print('Turning on VDD1 +5V Pre Driver Drain Voltage')
        self.power_up_keysight_e36312a()
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        print('Turning on VGG2, VGG3_C, VGG3_P -6.5V Gate Voltages')
        dac_value = [0x99, 0x05, 0x99, 0x05, 0x99, 0x05]
        self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES['DACA0_DATA_LO'], dac_value)
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        # input('Turn on VDD2, VDD3_C, VDD3_P +50V Drain Voltage')
        # print(f'Sleeping for {self._delay_sec} seconds...')
        # time.sleep(self._delay_sec)

    def set_dac_voltage(self, address: int, value: list[int]) -> None:
        self._amc7836.write_register(address, value)
        self._amc7836.write_register(self._amc7836.REGISTER_ADDRESSES['REG_UPDATE'], 0x01)
    
    def adjust_gate_voltage(self, dac_address_key: str, dac_init_value: int, daq_ch: int, target: float) -> None:
        """
        Adjust the gate voltage to reach a target drain current.

        Args:
        - dac_address_key (str): The key for the DAC address.
        - dac_init_value (int): The initial DAC value.
        - daq_ch (int): The DAQ channel.
        - target (float): The target drain current.

        Returns:
        - None
        """

        dac_step = [64, 32, 16, 8, 4, 2]
        # Define the DAC step values

        dac_value = [dac_init_value & 0xFF, dac_init_value >> 8]
        # Initialize the DAC value
        
        self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES[dac_address_key], dac_value)
        # Set the initial DAC voltage
        
        time.sleep(0.1)
        # Wait for 0.1 seconds
        
        drain_current = self._daq970a.measure_voltage(daq_ch)
        print(f'Drain current: {drain_current:.5f}')
        # Measure the start drain current
        
        dac_curr_value = dac_init_value
        # Initialize the current DAC value
        
        for index, val in enumerate(dac_step):
            dac_new_value = dac_curr_value + int(math.copysign(val, target - drain_current))
            # Calculate the new DAC value

            if dac_new_value < 3072:
            # Limit the DAC voltage to less than -2.5V (3072)

                dac_value = [dac_new_value & 0xFF, dac_new_value >> 8]
                # Update the DAC value

                self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES[dac_address_key], dac_value)
                # Set the new DAC voltage

                
                time.sleep(0.1)
                # Wait for 0.1 seconds

                drain_current = self._daq970a.measure_voltage(daq_ch)
                print(f'Iteration: {index} Drain current: {drain_current:.5f}')
                # Measure the drain current

            dac_curr_value = dac_init_value
            # Update the current DAC value


    def configure_scan(self, interval_count: int, interval_length: int) -> None:
        # Clear the scan list
        self._daq970a.write("ROUT:SCAN (@)")

        # Configure the channels for DC voltage measurement
        self._daq970a.write("CONF:VOLT:DC AUTO,DEF,(@111,112)")

        # Add channels to the scan list
        self._daq970a.write("ROUT:SCAN (@111,112)")

        self._daq970a.write("TRIG:COUNT " + str(interval_count))

        self._daq970a.write("TRIG:SOUR TIMER")

        self._daq970a.write("TRIG:TIMER " + str(interval_length))

        # Initiate the scan
        self._daq970a.write("INIT")

        time.sleep((interval_length * interval_count) + 5)

        results = self._daq970a.query("FETCH?")
        print("Scan Results:", results)

        measurements = []

        for result in results.strip().split(","):
            measurements.append(float(result))

        return measurements
    
    def scan_start_time(self):
        datetime_str = self.query("SYSTem:TIME:SCAN?")
        start_datetime = datetime.strptime(datetime_str, "%Y,%m,%d,%H,%M,%S.%f")
        return start_datetime

    def save_measurements_to_csv(self, measurements: list, timestamp: datetime, filename: str) -> None:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "CurrentVDD2", "CurrentVDD3_C"])

            for timestamp, values, in measurements:
                current_vdd2, current_vdd3_c = values
                writer.writerow([timestamp, current_vdd2, current_vdd3_c])

        print(f"Measurements saved to {filename}")
    
    '''
    TODO:
    1. Include channel names when saving to CSV.
    2. Ensure scan results are ordered from the earliest to the latest recorded.
    '''

    def power_down_keysight_e36234a(self) -> None:
        self._keysight_e36234a.set_output_voltage('1,2', 0)
        # Channel 1 and 2: 0V

        self._keysight_e36234a.set_output_current('1,2', 0)
        # Set the output current for channels 1 and 2 to 0A

        self._keysight_e36234a.enable_output('1,2', True)
    
    def power_down_keysight_e36312a(self) -> None:

        self._keysight_e36312a.set_output_voltage(1, 5)
        self._keysight_e36234a.set_output_current(2, 5)
        # Channel 1: 0V, 0A

        self._keysight_e36312a.set_output_voltage(2, 25)
        self._keysight_e36234a.set_output_current(2, 1)
        # Channel 2: 0V, 0A

        self._keysight_e36312a.set_output_voltage(3, 25)
        self._keysight_e36234a.set_output_current(3, 1)
        # Channel 3: 0V, 0A

        self._keysight_e36234a.enable_output('1,2,3', True)
        # Enable output

    def power_down_keysight_n5748a(self) -> None:
        self._keysight_n5748a.set_output_voltage(1, 0)
        # Channel 1: 0V, 0A

        self._keysight_n5748a.set_output_current(2, 0)
        # Channel 2: 0V, 0A

        self._keysight_e36234a.enable_output(1, True)
        # Enable output

    def power_down_sequence(self) -> None:
        print('Powering down VDD1 to 0V')
        self.power_down_keysight_e36312a()
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

        print('Powering down VGG2, VGG3_C, VGG3_P')
        dac_value = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.set_dac_voltage(self._amc7836.REGISTER_ADDRESSES['DACA0_DATA_LO'], dac_value)
        print(f'Sleeping for {self._delay_sec} seconds...')
        time.sleep(self._delay_sec)

    def close_daq(self):
        self._daq970a.close()

def interval_based_scan():
    test = DeviceUnderTest()

    print(f'Configuring DAQ970A...')
    test.configure_daq970a()

    print('Turn on AMC7836 Voltage')
    print(f'Configuring AMC7836...')
    test.configure_amc7836()

    print(f'Powering up DUT...')
    test.power_up_sequence()

    print(f'Start VGG2 Bias Search for 20mA"')
    test.adjust_gate_voltage('DACA0_DATA_LO', 2990, 104, 0.02)
    print(f'Start VGG2 Bias Search for 100mA"')
    test.adjust_gate_voltage('DACA0_DATA_LO', 2990, 104, 0.1)
    # IMPORTANT: I am only adjusting gate voltage once for this example, for practical use call the function inside of a for loop

    interval_count = 30  
    interval_length = 10  

    print(f'Configuring DAQ970A to perform 30 scans at 10-second intervals')
    data = test.configure_scan(interval_count, interval_length)
    start_time = test.scan_start_time()

    parsed_measurements = []

    for i in range(interval_count):
        timestamp = start_time + timedelta( seconds = interval_length * i)
        parsed_measurements.append((timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), data[i]))
    
    test.save_measurements_to_csv(parsed_measurements, timestamp, 'measurements.csv')
    

if __name__ == '__main__':
    interval_based_scan()
