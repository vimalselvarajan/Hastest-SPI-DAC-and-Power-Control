import pyvisa
import time
import csv
from datetime import datetime, timedelta
from instrument_lib.daq.keysight_daq970a import KeysightDaq970a

def configure_scan(daq, interval_count: int, interval_length: int):
    # Reset the instrument
    daq.write("*RST")
    daq.write("*CLS")
    time.sleep(1)
    
    # Clear the scan list
    daq.write("ROUT:SCAN (@)")
    
    # Configure the channels for DC voltage measurement
    daq.write("CONF:VOLT:DC AUTO,DEF,(@111,112)")
    
    # Add channels to the scan list
    daq.write("ROUT:SCAN (@111,112)")

    daq.write("TRIG:COUNT " + str(interval_count))

    daq.write("TRIG:SOUR TIMER")

    daq.write("TRIG:TIMER " + str(interval_length))

    # Initiate the scan
    daq.write("INIT")

    time.sleep((interval_length * interval_count) + 5)

    results = daq.query("FETCH?")
    print("Scan Results:", results)
    return results

def retrieve_date_time(daq):
    datetime_str = daq.query("SYSTem:TIME:SCAN?")
    return datetime_str.strip()

def parse_measurements(results):
    # Parse the results into a list of measurements
    measurements = []
    for result in results.strip().split(","):
        measurements.append(float(result))
    return measurements

def save_measurements_to_csv(measurements, filename):
    # Save the measurements to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CurrentVDD2", "CurrentVDD3_C", "Interval (s)"])
        
        for timestamp, values, interval_length in measurements:
            current_vdd2, current_vdd3_c = values
            writer.writerow([timestamp, current_vdd2, current_vdd3_c, interval_length])

def main():
    rm = pyvisa.ResourceManager()
    daq = rm.open_resource("USB0::0x2A8D::0x8501::MY59000319::INSTR")

    print(daq.query("*IDN?"))

    # Retrieve start date and time
    datetime_str = retrieve_date_time(daq)
    start_datetime = datetime.strptime(datetime_str, "%Y,%m,%d,%H,%M,%S.%f")
    
    # Configuration parameters
    interval_count = 30  # Number of intervals
    interval_length = 10  # Length of each interval in seconds

    # Configure the scan and retrieve results
    raw_results = configure_scan(daq, interval_count, interval_length)

    # Process the results
    measurements = []
    for i in range(interval_count):
        # Calculate the timestamp for each interval
        timestamp = start_datetime + timedelta(seconds=interval_length * i)
        parsed_results = parse_measurements(raw_results)
        measurements.append((timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), parsed_results, interval_length * (i + 1)))

    # Save to CSV
    save_measurements_to_csv(measurements, 'measurements.csv')

    print("Measurements completed and saved to measurements.csv")

if __name__ == "__main__":
    main()
