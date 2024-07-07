# SPI DAC and Power Control

## Overview

This project contains scripts to control DACs (Digital-to-Analog Converters) and power supplies via SPI (Serial Peripheral Interface) using the `pyftdi` and `pyvisa` libraries. The scripts demonstrate setting DAC ranges and voltages, as well as reading chip IDs and controlling power supplies.

## Features

- **DAC Control via SPI:**
  - Set DAC range.
  - Set DAC voltage.
  - Enable register updates.
  - Read chip ID.

- **Power Supply Control via USB:**
  - Query power supply status.
  - Set output voltage.
  - Measure output voltage and current.

## Requirements

- Python 3.x
- `pyftdi` library
- `pyvisa` library

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/SPI_DAC_and_Power_Control.git
    cd SPI_DAC_and_Power_Control
    ```

2. **Install the required Python libraries:**

    ```bash
    pip install pyftdi pyvisa
    ```

## Step-by-Step Process Guide

### Setting Up the Environment

1. **Install Python:**
    - Ensure Python 3.x is installed on your system.

2. **Set Up a Virtual Environment (optional but recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Required Libraries:**
    ```bash
    pip install pyftdi pyvisa
    ```

### Connecting the Hardware(Add photos)

1. **Connect the FTDI Chip:**
    - Connect your FTDI SPI adapter (e.g., FT232H or FT2232H) to your computer via USB.

2. **Configure Zadig:**
    - Download Zadig from [zadig.akeo.ie](https://zadig.akeo.ie/).
    - Open Zadig and select the FTDI device from the list.
    - Select `WinUSB` (or `libusb-win32` if `WinUSB` is not available) as the driver.
    - Click `Replace Driver` to install the driver. This allows the `pyftdi` library to communicate with the FTDI device.

3. **Connect the DAC:**
    - Connect the DAC to the FTDI chip according to the DAC and FTDI datasheets. Ensure SPI connections (MOSI, MISO, SCLK, CS) are correctly made.

4. **Connect the Power Supply:**
    - Connect the power supply to your computer via USB.

## Acknowledgments

- This project uses the `pyftdi` library for SPI communication.
- This project uses the `pyvisa` library for USB communication with power supplies.
