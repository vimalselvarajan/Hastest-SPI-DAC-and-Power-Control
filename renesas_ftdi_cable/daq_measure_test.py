import time
from datetime import datetime
import csv
from instrument_lib.daq.keysight_daq970a import KeysightDaq970a

def measure_channels(daq, channels):
    measurements = {}
    for channel in channels:
        voltage = daq.measure_voltage(channel)
        measurements[channel] = voltage
        print(f"Channel {channel} Voltage = {voltage:.5f} V")
    return measurements

def main():
    daq = KeysightDaq970a("USB0::0x2A8D::0x5101::MY58016887::INSTR")
    print(daq.query("*IDN?"))

    channels = [111, 112]
    duration = 5 * 60  # 5 minutes in seconds
    interval = 10  # 10 seconds interval

    # Open a CSV file to store the results
    with open('measurements.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CurrentVDD2", "CurrentVDD3_C"])

        start_time = time.time()
        while (time.time() - start_time) < duration:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            measurements = measure_channels(daq, channels)
            writer.writerow([timestamp, measurements[111], measurements[112]])
            time.sleep(interval)

    print("Measurements completed and saved to measurements.csv")

if __name__ == "__main__":
    main()
