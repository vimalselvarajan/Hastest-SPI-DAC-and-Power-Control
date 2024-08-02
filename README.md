# Hastest DAC, DAQ, and power supply control suite

This repository contains a series of Python scripts designed to automate various instrumentation tests using DAC and DAQ hardware. The primary devices interfaced in these scripts are Keysight's DAQ970A Data Acquisition System and the AMC7836 Digital-to-Analog Converter. These scripts demonstrate initialization, configuration, data acquisition, and control of various electronic components and circuits, aiming to facilitate automated testing and data logging.

## Overview

The `renesas_ftdi_cable` folder includes multiple Python scripts, each tailored for specific test setups:

1. **AMC7836 Test (`amc7836_test.py`)**: Configures and tests the AMC7836 DAC, including writing to and reading from registers.
2. **DAQ Measurement Test (`daq_measure_test.py`)**: This script measures voltage across specified channels using the Keysight DAQ970A. It utilizes the MEASure subsystem, which simplifies programming measurements by using default parameters. With the MEASure queries, you can set the function, range, and resolution in a single command. The results are then directly sent to the instrument’s output buffer, making this method the easiest way to perform measurements with predefined settings.
3. **DAQ Scan Test (`daq_scan_test.py`)**: Configures and performs a scan for voltage measurements on specified channels using the DAQ970A.
4. **F84010 Test (`f84010_test.py`)**: Comprehensive test script that configures both the DAC and DAQ for a specific hardware testing scenario, including a power-up and power-down sequence.

## Prerequisites

- Python 3.x
- `numpy`
- `pyvisa` (For handling communication with instruments via VISA interface)

### Hardware

- Keysight DAQ970A Data Acquisition System
- AMC7836 Digital-to-Analog Converter
- Appropriate cabling and connections for communication and power supply

## Installation

Clone the repository:

```bash
git clone <repository-url>
