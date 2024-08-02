import time
from instrument_lib.daq.keysight_daq970a import KeysightDaq970a

def measure_channels(daq):
    channels = [111, 112]

    time.sleep(1)  

    measurements = {}
    for channel in channels:
        voltage = daq.measure_voltage(channel)
        measurements[channel] = voltage
        print(f"Channel {channel} Voltage = {voltage:.5f} V")
    
    return measurements

def main():
    daq = KeysightDaq970a("USB0::0x2A8D::0x5101::MY58016887::INSTR")
    print(daq.query("*IDN?"))

    measurements = measure_channels(daq)
    print("Measurements:", measurements)

if __name__ == "__main__":
    main()
