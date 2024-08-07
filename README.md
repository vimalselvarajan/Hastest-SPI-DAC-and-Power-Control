# Hastest DAC, DAQ, and Power Supply Control Suite

A Python project for controlling and testing devices under test (DUTs) using various instruments and interfaces.

## Table of Contets:

### Software
1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Hardware Requirements](#hardware-requirements)
5. [Installation](#installation)
### Hardware 
6. [Project Diagram](#project-diagram)
7. [Electrical Characteristics](#electrical-characteristics)
8. [DAQ Equipment](#daq-equipment)


## Overview

This repository contains a series of Python scripts designed to automate various instrumentation tests using DAC, DAQ, and power supply hardware. These scripts demonstrate initialization, configuration, data acquisition, and control of various electronic components and circuits, aiming to facilitate automated testing and data logging. One of the key features of this project is the adjust_gate_voltage algorithm, which uses a simple iterative approach to adjust the gate voltage of the DUT to reach a target drain current. The algorithm uses a predefined set of DAC step values to incrementally adjust the gate voltage, ensuring that the target current is reached quickly and accurately. Overall this project provides a simple and intuitive way to interact with DUTs, allowing users to focus on testing and validation rather than low-level instrument control. It currently supports the following instruments:

- AMC7836 DAC
- Keysight DAQ970A
- Keysight E36234A power supply
- Keysight E36312A power supply
- Keysight N5748A power supply

## Features

- Automatic DAC voltage adjustment for target drain current using the adjust_gate_voltage algorithm
- Interval-based scanning for DAQ970A
- Power supply control for Keysight E36234A, E36312A, and N5748A

## Project Structure

- `datasheets/:` Contains the data sheets for required hardware
- `pyftdi_cable/:` Contains code to control the AMC7836 board using the pyftdi driver. These files are not relevant to the main project but are included as a proof of concept to demonstrate the functionality of the AMC7836 board.
  - `amc7836.py:` Contains the AMC7836 class provides methods to control the AMC7836 board via SPI communication
  - `demo.py:` A short demo which tests out the SpiController
  - `main.py:` Initializes the SPI controller and the AMC7836 board, performs a series of configuration steps, sets DAC ranges and voltages, and updates the DAC registers using the pyftdi and custom SPI communication classes.
  - `spi_communications.py:` Facilitates reading from and writing to SPI registers 
- `renasas_Ftdi_cable/:` Main Project
  - `instrument_lib/:` Facilitates reading from and writing to the AMC7836 DAC, Keysight DAQ970A, and the three power supplies
    - `dac/:` Contains the AMC7836 class which provides methods to control the AMC7836 board via SPI communication
    - `daq/:` Contains the KeysightDaq970a class which provides methods to measure voltage on specified channels
    - `power_supply/:` Contains three classes, each representing a different power supply, with methods to set and measure output voltage and current.
    - `instrument_base.py:` Provides a foundational interface for interacting with the DAQ and Power supplies
- `main.py:` Contains code that executes the main project as described in the overview section

## Prerequisites

- Python 3.x
- NI Max
- Zadig
- `numpy`
- `pyvisa` 
- `pandas` 
- `pyftdi` 

### Hardware Requirements

- AMC7836 DAC
- BPR-58 1 Ohm shunt resistor
- Keysight DAQ970A
- Keysight E36234A power supply
- Keysight E36312A power supply
- Keysight N5748A power supply
- Renesas ft2232

## Installation

Clone the repository:

```bash
git clone https://github.com/vimalselvarajan/Hastest-SPI-DAC-and-Power-Control.git
```

Installing 'venv'

If you don't already have venv installed, you can install it using pip:
```bash
python -m venv myenv
```

Activating the Virtual Environment
```bash
# On Windows
myenv\Scripts\activate

# On Linux or macOS
source myenv/bin/activate
```

Install the required python libraries:
```bash
pip install pyvisa
pip install pandas
pip install pyftdi
```

## Project Diagram
![HTOL Test Setup](https://github.com/user-attachments/assets/7921ea29-ac1d-499d-9e5b-d731a49abcca)

## Electrical Characteristics

### DUT Power Supplies: 

| Voltage Input | Description                     | Specification      |
|---------------|---------------------------------|--------------------|
| VDD1          | Keysight E36234A – Output 1     | 60V, 10A, 200W     |
| VGG3_P        | Keysight E36234A – Output 2     | 60V, 10A, 200W     |
| VDD2          | Keysight N5748A                 | 80V, 9.5A, 760W    |
| VDD3_C, VDD3_P| Keysight N5748A                 | 80V, 9.5A, 760W    |

### DAC AMC7836/Current Sense Power Supplies

| Voltage Input | Description                    | Specification   |
|---------------|--------------------------------|-----------------|
| VCC           | Keysight E36312A – Output 1    | 6V, 5A, 30W     |
| VEE           | Keysight E36312A – Output 2    | 25V, 1A, 25W    |
| 3.3V          | Powered by FT2232/USB port     | -               |

### DAQ Equipment

| Current Output | Description                       | 
|----------------|-----------------------------------|
| IDD1           | Keysight DAQ970A with 3x DAQM900A | 
| IDD2           | Keysight DAQ970A with 3x DAQM900A | 
| IDD3           | Keysight DAQ970A with 3x DAQM900A | 

