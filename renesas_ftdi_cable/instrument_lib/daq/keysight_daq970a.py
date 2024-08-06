import pyvisa
import time
import csv
from datetime import datetime, timedelta
from typing import Union, List
from instrument_lib.instrument_base import InstrumentBase

class KeysightDaq970a(InstrumentBase):

    def measure_voltage(self, ch: Union[int, str], v_range: Union[None, float] = None,
                        resolution: Union[None, float] = None) -> Union[float, List[float]]:
        command = "MEAS:VOLT:DC?"
        if v_range is not None:
            if resolution is not None:
                command = f"{command} {v_range},{resolution},(@{ch})"
            else:
                command = f"{command} {v_range},(@{ch})"
        else:
            command = f"{command} (@{ch})"

        response = self.query(command)
        if isinstance(ch, int):
            return float(response)
        else:
            values = response.split(',')
            return [float(value) for value in values]

    def configure_scan(self, interval_count: int, interval_length: int):
        # Reset the instrument
        self.write("*RST")
        self.write("*CLS")
        time.sleep(1)

        # Clear the scan list
        self.write("ROUT:SCAN (@)")

        # Configure the channels for DC voltage measurement
        self.write("CONF:VOLT:DC AUTO,DEF,(@111,112)")

        # Add channels to the scan list
        self.write("ROUT:SCAN (@111,112)")

        self.write("TRIG:COUNT " + str(interval_count))

        self.write("TRIG:SOUR TIMER")

        self.write("TRIG:TIMER " + str(interval_length))

        # Initiate the scan
        self.write("INIT")

        time.sleep((interval_length * interval_count) + 5)

        results = self.query("FETCH?")
        print("Scan Results:", results)
        return results

    def retrieve_date_time(self):
        datetime_str = self.query("SYSTem:TIME:SCAN?")
        return datetime_str.strip()

    def parse_measurements(self, results):
        # Parse the results into a list of measurements
        measurements = []
        for result in results.strip().split(","):
            measurements.append(float(result))
        return measurements

    def save_measurements_to_csv(self, measurements, filename):
        # Save the measurements to a CSV file
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "CurrentVDD2", "CurrentVDD3_C", "Interval (s)"])

            for timestamp, values, interval_length in measurements:
                current_vdd2, current_vdd3_c = values
                writer.writerow([timestamp, current_vdd2, current_vdd3_c, interval_length])

def main():
    rm = pyvisa.ResourceManager()
    daq = KeysightDaq970a(rm.open_resource("USB0::0x2A8D::0x8501::MY59000319::INSTR"))

    print(daq.query("*IDN?"))

    # Retrieve start date and time
    datetime_str = daq.retrieve_date_time()
    start_datetime = datetime.strptime(datetime_str, "%Y,%m,%d,%H,%M,%S.%f")

    # Configuration parameters
    interval_count = 30  # Number of intervals
    interval_length = 10  # Length of each interval in seconds

    # Configure the scan and retrieve results
    raw_results = daq.configure_scan(interval_count, interval_length)

    # Process the results
    measurements = []
    for i in range(interval_count):
        # Calculate the timestamp for each interval
        timestamp = start_datetime + timedelta(seconds=interval_length * i)
        parsed_results = daq.parse_measurements(raw_results)
        measurements.append((timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), parsed_results, interval_length * (i + 1)))

    # Save to CSV
    daq.save_measurements_to_csv(measurements, 'measurements.csv')

    print("Measurements completed and saved to measurements.csv")

if __name__ == "__main__":
    main()
