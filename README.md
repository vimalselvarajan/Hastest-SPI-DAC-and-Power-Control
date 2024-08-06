# Hastest DAC, DAQ, and Power Supply Control Suite

A Python project for controlling and testing devices under test (DUTs) using various instruments and interfaces.

## Table of Contets:

## Software
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

- Simple and intuitive way to control DUTs
- Support for multiple instruments and interfaces
- Automatic DAC voltage adjustment for target drain current using the adjust_gate_voltage algorithm
- Interval-based scanning for DAQ970A
- Power supply control for Keysight E36234A, E36312A, and N5748A

## Prerequisites

- Python 3.x
- `numpy`
- `pyvisa` 
- `pandas` 
- `pyftdi` 

### Hardware Requirements

- AMC7836 DAC
- Keysight DAQ970A
- Keysight E36234A power supply
- Keysight E36312A power supply
- Keysight N5748A power supply
- C232HM_MPSSE_CABLE USB 2.0 HI-SPEED TO MPSSE CABLE

## Installation

Clone the repository:

```bash
git clone https://github.com/vimalselvarajan/Hastest-SPI-DAC-and-Power-Control.git
```

# Project Diagram
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

