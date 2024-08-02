# Hastest DAC, DAQ, and Power Supply Control Suite

This repository contains a series of Python scripts designed to automate various instrumentation tests using DAC and DAQ hardware. The primary devices interfaced in these scripts are Keysight's DAQ970A Data Acquisition System and the AMC7836 Digital-to-Analog Converter. These scripts demonstrate initialization, configuration, data acquisition, and control of various electronic components and circuits, aiming to facilitate automated testing and data logging.

## Overview

The `renesas_ftdi_cable` folder includes multiple Python scripts, each tailored for specific test setups:

1. **AMC7836 Test (`amc7836_test.py`)**: This script configures and tests the AMC7836 DAC by performing various register operations, including writing to and reading from them. Specifically, it sets the DAC channels to output -6.5V, demonstrating precise voltage control.
2. **DAQ Measurement Test (`daq_measure_test.py`)**: This script measures voltage across specified channels using the Keysight DAQ970A. It utilizes the MEASure subsystem, which simplifies programming measurements by using default parameters. With the MEASure queries, you can set the function, range, and resolution in one command. The results are then directly sent to the instrument’s output buffer, making this method the easiest way to perform measurements with predefined settings.
3. **DAQ Scan Test (`daq_scan_test.py`)**: This script configures and performs a scan for voltage measurements on specified channels using the Keysight DAQ970A. The scanning feature is advantageous as it allows for asynchronous operation; measurements are conducted in the background, enabling other tasks to be performed concurrently without immediate return of values.
4. **F84010 Test (`f84010_test.py`)**: This script includes the `sdac_vgg` function, which dynamically adjusts the gate voltage using an AMC7836 DAC to achieve a target bias current in a hardware testing scenario. The algorithm starts by setting an initial DAC value and iteratively adjusting the voltage using a binary step method (BSM). Each step modifies the DAC value based on the difference between the target and the measured bias current, refining the gate voltage until the target current is approached without exceeding a specified DAC limit (3072). This method allows precise control of the device under test, ensuring optimal operation.

## Prerequisites

- Python 3.x
- `numpy`
- `pyvisa` (For handling communication with instruments via VISA interface)
- `pandas` (For data manipulation and analysis)
- `pyftdi` (For FTDI device communication)

### Hardware

- Keysight DAQ970A Data Acquisition System
- AMC7836 Digital-to-Analog Converter
- Appropriate cabling and connections for communication and power supply

## Installation

Clone the repository:

```bash
git clone <repository-url>
