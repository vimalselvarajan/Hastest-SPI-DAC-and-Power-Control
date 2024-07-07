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

### Setting Up the Environment

1. **Install Python:**
    - Ensure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Set Up a Virtual Environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Libraries:**
    ```bash
    pip install pyftdi pyvisa
    ```

## Acknowledgments

- This project uses the `pyftdi` library for SPI communication.
- This project uses the `pyvisa` library for USB communication with power supplies.
