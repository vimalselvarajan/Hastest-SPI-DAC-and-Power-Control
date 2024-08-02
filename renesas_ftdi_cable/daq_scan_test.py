import pyvisa
import time

def configure_scan(daq):
    # Reset the instrument
    daq.write("*RST")
    time.sleep(1)
    
    # Clear the scan list
    daq.write("ROUT:SCAN (@)")
    
    # Configure the channels for DC voltage measurement
    daq.write("CONF:VOLT:DC AUTO,DEF,(@111,112)")
    
    # Add channels to the scan list
    daq.write("ROUT:SCAN (@111,112)")
    
    # Set scan trigger source to immediate
    daq.write("TRIG:SOUR IMM")
    
    # Set the number of scans
    daq.write("SAMP:COUN 10")  # Set to 10 scans, adjust as needed

def start_scan(daq):
    # Initiate the scan
    daq.write("INIT")
    
    # Wait for the scan to complete
    time.sleep(2)  # Adjust the sleep time based on the number of scans and sample rate
    
    # Fetch the results
    results = daq.query("FETCH?")
    print("Scan Results:", results)

def main():
    rm = pyvisa.ResourceManager()
    daq = rm.open_resource("USB0::0x2A8D::0x5101::MY58016887::INSTR")
    
    print(daq.query("*IDN?"))
    
    configure_scan(daq)
    start_scan(daq)

if __name__ == "__main__":
    main()
