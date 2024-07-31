from instruments.keysight_e36312a import KeysightE36312a
from instruments.keysight_daq970a import KeysightDaq970a
import time

def power_supply():
    resource_name = "USB0::0x0957::0x0807::US27C3730L::INSTR"
    power_supply = KeysightE36312a(resource_name)

    # Reset the power supply
    power_supply.reset()
    
    # Set output voltage on channel 1 to 5V
    power_supply.set_output_voltage(1, 5.0)
    
    # Enable output on channel 1
    power_supply.enable_output(1, True)
    
    # Measure voltage without specifying a channel
    voltage_no_channel = power_supply.measure_voltage_no_channel()
    print(f"Voltage without specifying channel: {voltage_no_channel} V")
    
    # Set output voltage on channel 1 to 0V
    power_supply.set_output_voltage(1, 0.0)
    
    # Disable output on channel 1
    power_supply.enable_output(1, False)
    
    # Close the connection
    power_supply.close()

def test_daq():
    resource_name = "USB0::0x2A8D::0x5101::MY58016887::INSTR"
    daq = KeysightDaq970a(resource_name)

    daq.get_scan_mode()

    daq.clear()
    daq.reset()

    daq.get_scan_mode()

    # Measure voltage on channel 102
    voltage = daq.measure_voltage(102)
    print(f"Channel 102 Voltage: {voltage} V")

    # Measure voltage on multiple channels
    voltages = daq.measure_voltage("101,102,103")
    print(f"Channel 101, 102, 103 Voltages: {voltages} V")

    daq.close()
    
# Usage example:
if __name__ == "__main__":
    power_supply()
    test_daq()
