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



## Acknowledgments

- This project uses the `pyftdi` library for SPI communication.
- This project uses the `pyvisa` library for USB communication with power supplies.
