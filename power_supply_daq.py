from pyvisa import ResourceManager
from pyvisa.resources import MessageBasedResource

class InstrumentBase:
    def __init__(self, resource_name: str):
        rm = ResourceManager()
        self._resource: MessageBasedResource = rm.open_resource(resource_name)

    def clear(self) -> None:
        self._resource.write("*CLS")

    def close(self) -> None:
        self._resource.close()

    def get_id(self) -> str:
        return self._resource.query("*IDN?")

    def query(self, command: str) -> str:
        return self._resource.query(command)

    def read(self) -> str:
        return self._resource.read()

    def reset(self) -> None:
        self._resource.write("*RST")

    def write(self, command: str) -> None:
        self._resource.write(command)

    def get_scan_mode(self) -> str:
        return self.query("ROUT:SCAN?")
    

class KeysightE36312a(InstrumentBase):
    def enable_output(self, ch: int, enable: bool) -> None:
        self.write(f"OUTP {int(enable)},(@{ch})")

    def set_output_current(self, ch: int, current: float) -> None:
        self.write(f"CURR {current:.3f},(@{ch})")

    def set_output_voltage(self, ch: int, voltage: float) -> None:
        self.write(f"VOLT {voltage:.3f},(@{ch})")

    def measure_current(self, ch: int) -> float:
        return float(self.query(f"MEAS:CURR?,(@{ch})"))

    def measure_voltage(self, ch: int) -> float:
        return float(self.query(f"MEAS:VOLT?,(@{ch})"))

    def measure_voltage_no_channel(self) -> float:
        return float(self.query("MEAS:VOLT?"))

    def set_voltage_range(self, ch: int, range: float) -> None:
        self.write(f"SOUR:VOLT:RANG {range:.3f},(@{ch})")

    def get_voltage_range(self, ch: int) -> float:
        return float(self.query(f"SOUR:VOLT:RANG?,(@{ch})"))

class DAQ(InstrumentBase):
    def measure_voltage(self, ch: int) -> float:
        return float(self.query(f"MEAS:VOLT? (@{ch})"))

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

def test_DAQ():
    resource_name = "USB0::0x2A8D::0x5101::MY58016887::INSTR"  
    daq = DAQ(resource_name)

    daq.get_scan_mode()

    daq.clear()
    daq.reset()

    daq.get_scan_mode()

    voltage = daq.measure_voltage("102")
    print(f"Channel 1 Voltage: {voltage} V")

    daq.close()
    
# Usage example:
if __name__ == "__main__":
    test_DAQ()
